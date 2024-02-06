import datetime
import json
import os
import warnings

import numpy as np
import pandas as pd

__telemetry_headers = [
    'capture',
    'p.x',
    'p.y',
    'p.z',
    'o.x',
    'o.y',
    'o.z',
    'l_vel.x',
    'l_vel.y',
    'l_vel.z',
    'a_vel.x',
    'a_vel.y',
    'a_vel.z',
    'l_acc.x',
    'l_acc.y',
    'l_acc.z',
    'a_acc.x',
    'a_acc.y',
    'a_acc.z',
    'scale'
]


def get_data(path: str, include_static_frames: bool = True, include_night_frames: bool = True):
    """
    Get the telemetry data from the dataset
    """
    sessions = get_sessions(path)
    data = get_telemetry_data(path, sessions)

    if not include_static_frames:
        data = data[data['movement_delta'] > 0]

    if not include_night_frames:
        data = data[data['moment'] != 'noche']

    return data


def get_sessions(path: str):
    if not os.path.isdir(path):
        warnings.warn(f"Path: {path} is not a valid path", RuntimeWarning)
        return []

    sessions = []
    dataset_dirs = sorted([f.path for f in os.scandir(path) if f.is_dir()])
    for d in dataset_dirs:
        if os.path.isfile(f"{d}/session.json"):
            session_string = open(f"{d}/session.json", "r").read()
            sessions.append(json.loads(session_string))
    return sessions


def get_telemetry_data(path: str, sessions: list):
    telemetry_data = []
    for i, s in enumerate(sessions):
        session_folder = os.path.join(path, f"{s['date']}-{s['session']}")
        tfd = pd.read_csv(os.path.join(session_folder, "telemetry.txt"),
                          header=None,
                          index_col=False,
                          names=__telemetry_headers,
                          # dtype=[('capture', str), ('pos', float, 3)],
                          sep=';')
        tfd['session'] = f"{s['date']}-{s['session']}"
        tfd['environment'] = s['environment'].split("/")[0]
        tfd['traffic'] = s['traffic']
        d = datetime.datetime.strptime(f"{s['date']} {s['gametime']}", "%Y%m%d %H:%M:%S")
        tfd['time'] = d
        tfd['moment'] = "mañana" if d.strftime("%H") in ["06", "07", "08", "09", "10", "11", "12", "13", "14", "15"] \
            else "tarde" if d.strftime("%H") in ["16", "17", "18", "19", "20"] else "noche"
        tfd['weather'] = s.get('weather', 'Not specified')
        tfd['position'] = tfd[['p.x', 'p.y', 'p.z']].values.tolist()
        tfd['orientation'] = tfd[['o.x', 'o.y', 'o.z']].values.tolist()
        tfd['vel_l'] = tfd[['l_vel.x', 'l_vel.y', 'l_vel.z']].values.tolist()
        tfd['vel_a'] = tfd[['a_vel.x', 'a_vel.y', 'a_vel.z']].values.tolist()
        tfd['acc_l'] = tfd[['l_acc.x', 'l_acc.y', 'l_acc.z']].values.tolist()
        tfd['acc_a'] = tfd[['a_acc.x', 'a_acc.y', 'a_acc.z']].values.tolist()

        v = tfd.tail(1).index[0]
        tfd['corner'] = np.logical_or(tfd.index == v, tfd.index == 0)

        # tfd['min_depth'], tfd['max_depth'] = np.vectorize(self.get_depth_stats)(tfd['session'], tfd['capture'])

        telemetry_data.append(tfd)

    telemetry_data = pd.concat(telemetry_data)
    telemetry_data['movement_delta'] = vector_diff(telemetry_data['position'],
                                                   telemetry_data['position'].shift(1, fill_value=0))
    return telemetry_data


def vector_diff(a, b):
    b[0] = b[1]
    data = np.linalg.norm(np.subtract(b.tolist(), a.tolist()), axis=1)
    return data

import pytest

from capo_tools.datasets.ETS2.ets2_tools import get_sessions, get_telemetry_data


def test_get_sessions():
    sessions = get_sessions("resources/ets2_dataset/train")
    assert len(sessions) == 2
    assert sessions[0]["date"] == "20210721"
    assert sessions[0]["session"] == "000004"
    assert sessions[0]["location"] == "Szcezin, Poland"
    assert sessions[0]["environment"] == "urban"
    assert sessions[0]["traffic"] == "1"
    assert sessions[0]["gametime"] == "20:00:00"
    assert sessions[1]["date"] == "20210722"
    assert sessions[1]["session"] == "000003"
    assert sessions[1]["location"] == "Paris, France"
    assert sessions[1]["environment"] == "urban/highway"
    assert sessions[1]["traffic"] == "9"
    assert sessions[1]["weather"] == "0"
    assert sessions[1]["gametime"] == "14:30:00"


def test_get_sessions_error():
    with pytest.warns(RuntimeWarning):
        sessions = get_sessions("not/a/real/path")
    assert len(sessions) == 0


def test_get_sessions_emtpy():
    sessions = get_sessions("resources/ets2_dataset/test")
    assert len(sessions) == 0


def test_get_telemetry():
    """
    This test is not too much but still a starting point
    """
    sessions = get_sessions("resources/ets2_dataset/train")
    telemetry = get_telemetry_data("resources/ets2_dataset/train", sessions)
    assert len(telemetry) == 10
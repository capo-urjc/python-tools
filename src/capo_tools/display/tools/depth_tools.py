from matplotlib import cm
import numpy as np


def normalize(data):
    max = float(data.max())
    min = float(data.min())
    range = max - min if max != min else 1e10
    return (data - min) / range


def colorize(data, colormap_name='magma', normalize_data=True, invert=False):
    if normalize_data or invert:
        data = normalize(data)

        if invert:
            data = 1 - data

    colormap = cm.get_cmap(colormap_name)
    imdata = colormap(data)
    imdata = np.uint8(imdata * 255)
    return imdata

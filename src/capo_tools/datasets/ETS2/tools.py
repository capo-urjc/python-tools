import numpy as np
from PIL import Image


def is_pil_image(img):
    """
    Given an object, checks if it is a PIL image.
    img (object): object to check if it is a PIL image
    """
    return isinstance(img, Image.Image)


def is_numpy_image(img):
    """
    Given an object, checks if it is a numpy image.
    Be careful there is no way to check if a numpy array is an image, this function checks if the input is a numpy array
    and if it has 2 or 3 dimensions.
    img (object): object to check if it is a numpy image
    """
    return isinstance(img, np.ndarray) and (img.ndim in {2, 3})


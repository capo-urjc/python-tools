import numpy as np
from matplotlib import pyplot as plt

def extract_random_patch(image, size):
    """
    Extracts a random patch of size 'size' from the input image.
    Zero padding is applied if the patch exceeds the image boundaries.

    Parameters:
    - image: NumPy array representing the input image.
    - size: Tuple (height, width) specifying the size of the patch.

    Returns:
    - patch: NumPy array representing the extracted patch.
    """

    # Get image dimensions
    img_height, img_width = image.shape[:2]
    patch_height, patch_width = size

    # Choose random starting coordinates for the patch
    start_row = np.random.randint(0, img_height - patch_height + 1)
    start_col = np.random.randint(0, img_width - patch_width + 1)

    # Extract the patch
    patch = image[start_row:start_row + patch_height, start_col:start_col + patch_width]

    return patch


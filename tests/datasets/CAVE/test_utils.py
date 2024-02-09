import numpy as np
import torch
from capo_tools.datasets.CAVE.utils.extract_random_patch import extract_random_patch
from capo_tools.datasets.CAVE.utils.downsampling import DownSampling_LossChannels

def test_extract_random_patch():
    # Generate a random image
    image = np.random.randint(low=0, high=255, size=(128, 128, 35))

    # Extract a random patch from the image
    patch = extract_random_patch(image, (32, 32))
    assert patch.shape == (32, 32, 35)

def test_DownSampling_LossChannels():
    # Generate a random image
    image = torch.randn(31, 128, 128).abs()

    # Extract a random patch from the image
    sample = DownSampling_LossChannels()(image)
    x, y = sample['x'], sample['y']
    assert x.shape == (31, 128, 128)
    assert y.shape == (31, 128, 128)

    # Check if the sum of the first channel is greater than 0 and second channel is exactly 0 for input
    # and greater than 0 for output
    assert x[0, ...].sum() > 0 and y[0, ...].sum() > 0
    assert x[1, ...].sum() == 0 and y[1, ...].sum() > 0
import pytest
from torchvision import transforms
from capo_tools.datasets.CAVE.dataset import CAVEDataset
from capo_tools.datasets.CAVE.utils.downsampling import DownSampling_LossChannels


@pytest.fixture
def dataset_test_path():
    return "resources/cave_dataset"


def test_frame_dataset(dataset_test_path):
    # Define transformation pipeline for training data
    train_composed = transforms.Compose([
        transforms.ToTensor(),
        DownSampling_LossChannels(),
    ])

    # Load dataset
    dataset = CAVEDataset(dataset_test_path, patch_size=(128, 128), transform=train_composed, mode='train')

    # Assertions
    assert len(dataset) == 1

    # Check shapes of input and output tensors
    x, y = dataset[0]['x'], dataset[0]['y']
    assert x.shape == (31, 128, 128)
    assert y.shape == (31, 128, 128)

    # Check if the sum of the first channel is greater than 0 and second channel is exactly 0 for input
    # and greater than 0 for output
    assert x[0, ...].sum() > 0 and y[0, ...].sum() > 0
    assert x[1, ...].sum() == 0 and y[1, ...].sum() > 0



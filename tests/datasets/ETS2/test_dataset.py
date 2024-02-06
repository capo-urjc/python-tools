import math
import os

import numpy as np
import pytest

from PIL import Image

from capo_tools.datasets.ETS2.dataset import ToTensor, ETS2Dataset


@pytest.fixture
def dataset_frame():
    from capo_tools.datasets.ETS2.ets2_tools.depth_file import read_depth_file
    image = Image.open('resources/ets2_dataset/train/20210721-000004/capture-0000000001.jpg')
    depth_file = read_depth_file('resources/ets2_dataset/train/20210721-000004/capture-0000000001.depth.raw')
    header = depth_file.header
    depth = -depth_file.get_data()
    depth_shape = (header.height, header.width, 1)
    depth = np.reshape(depth, depth_shape)
    return {'image': image, 'depth': depth}


@pytest.fixture
def dataset_mock_frame():
    image = np.random.rand(816, 1440, 3)
    image = Image.fromarray((image * 255).astype(np.uint8))
    depth = np.random.rand(816, 1440, 1)
    return {'image': image, 'depth': depth}


@pytest.fixture
def dataset_test_path():
    return "resources/ets2_dataset/train"


def test_to_tensor(dataset_frame):
    to_tensor = ToTensor()
    sample = to_tensor(dataset_frame)

    assert sample['image'].shape == np.array(dataset_frame['image']).transpose(2, 0, 1).shape
    assert sample['depth'].shape == dataset_frame['depth'].transpose(2, 0, 1).shape
    assert sample['image'].numpy().sum() == pytest.approx(np.array(dataset_frame['image'], np.float32).sum())
    assert sample['depth'].numpy().sum() == pytest.approx(dataset_frame['depth'].sum())


def test_frame_dataset(dataset_test_path):
    dataset = ETS2Dataset(dataset_test_path, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    assert len(dataset) == 10

    image, depth, metadata = dataset[0]
    assert image.shape == (3, 816, 1440)
    assert depth.shape == (1, 816, 1440)
    assert os.path.normpath(metadata['path']) == os.path.normpath("resources/ets2_dataset/train/20210721-000004/capture-0000000001")
    assert metadata['session'] == "20210721-000004"
    assert metadata['capture'] == "capture-0000000001"

    image, depth, metadata = dataset[1]
    assert image.shape == (3, 816, 1440)
    assert depth.shape == (1, 816, 1440)
    assert os.path.normpath(metadata['path']) == os.path.normpath("resources/ets2_dataset/train/20210721-000004/capture-0000000002")
    assert metadata['session'] == "20210721-000004"
    assert metadata['capture'] == "capture-0000000002"

    image, depth, metadata = dataset[2]
    assert image.shape == (3, 816, 1440)
    assert depth.shape == (1, 816, 1440)
    assert os.path.normpath(metadata['path']) == os.path.normpath("resources/ets2_dataset/train/20210721-000004/capture-0000000003")
    assert metadata['session'] == "20210721-000004"
    assert metadata['capture'] == "capture-0000000003"

    image, depth, metadata = dataset[3]
    assert image.shape == (3, 816, 1440)
    assert depth.shape == (1, 816, 1440)
    assert os.path.normpath(metadata['path']) == os.path.normpath("resources/ets2_dataset/train/20210721-000004/capture-0000000004")
    assert metadata['session'] == "20210721-000004"
    assert metadata['capture'] == "capture-0000000004"

    image, depth, metadata = dataset[4]
    assert image.shape == (3, 816, 1440)
    assert depth.shape == (1, 816, 1440)
    assert os.path.normpath(metadata['path']) == os.path.normpath("resources/ets2_dataset/train/20210721-000004/capture-0000000005")
    assert metadata['session'] == "20210721-000004"
    assert metadata['capture'] == "capture-0000000005"

    image, depth, metadata = dataset[5]
    assert image.shape == (3, 816, 1440)
    assert depth.shape == (1, 816, 1440)
    assert os.path.normpath(metadata['path']) == os.path.normpath("resources/ets2_dataset/train/20210722-000003/capture-0000000001")
    assert metadata['session'] == "20210722-000003"
    assert metadata['capture'] == "capture-0000000001"

    image, depth, metadata = dataset[6]
    assert image.shape == (3, 816, 1440)
    assert depth.shape == (1, 816, 1440)
    assert os.path.normpath(metadata['path']) == os.path.normpath("resources/ets2_dataset/train/20210722-000003/capture-0000000002")
    assert metadata['session'] == "20210722-000003"
    assert metadata['capture'] == "capture-0000000002"

    image, depth, metadata = dataset[7]
    assert image.shape == (3, 816, 1440)
    assert depth.shape == (1, 816, 1440)
    assert os.path.normpath(metadata['path']) == os.path.normpath("resources/ets2_dataset/train/20210722-000003/capture-0000000003")
    assert metadata['session'] == "20210722-000003"
    assert metadata['capture'] == "capture-0000000003"

    image, depth, metadata = dataset[8]
    assert image.shape == (3, 816, 1440)
    assert depth.shape == (1, 816, 1440)
    assert os.path.normpath(metadata['path']) == os.path.normpath("resources/ets2_dataset/train/20210722-000003/capture-0000000004")
    assert metadata['session'] == "20210722-000003"
    assert metadata['capture'] == "capture-0000000004"

    image, depth, metadata = dataset[9]
    assert image.shape == (3, 816, 1440)
    assert depth.shape == (1, 816, 1440)
    assert os.path.normpath(metadata['path']) == os.path.normpath("resources/ets2_dataset/train/20210722-000003/capture-0000000005")
    assert metadata['session'] == "20210722-000003"
    assert metadata['capture'] == "capture-0000000005"

import os

import numpy as np
import pandas as pd
import pytest

from PIL import Image

from capo_tools.datasets.ETS2.dataset import ToTensor, ETS2Dataset


@pytest.fixture(params=['jpg', 'bmp'])
def dataset_frame(request):
    from capo_tools.datasets.ETS2.ets2_tools.depth_file import read_depth_file
    image = Image.open(f'resources/ets2_dataset/train/20210721-000004/capture-0000000001.{request.param}')
    depth_file = read_depth_file('resources/ets2_dataset/train/20210721-000004/capture-0000000001.depth.raw')
    header = depth_file.header
    depth = depth_file.get_data()
    depth_shape = (header.height, header.width, 1)
    depth = np.reshape(depth, depth_shape)
    yield {'image': image, 'depth': depth, 'frame': 'resources/ets2_dataset/train/20210721-000004/capture-0000000001',
            'metadata': pd.DataFrame([{'session': '20210721-000004', 'capture': 'capture-0000000001'}])}


@pytest.fixture
def dataset_mock_frame():
    image = np.random.rand(816, 1440, 3)
    image = Image.fromarray((image * 255).astype(np.uint8))
    depth = np.random.rand(816, 1440, 1)
    return {'image': image, 'depth': depth}


@pytest.fixture
def dataset_test_path():
    return "resources/ets2_dataset/train"


@pytest.fixture(params=['jpg', 'bmp'])
def pytorch_dataset_frame(request, dataset_test_path):
    dataset = ETS2Dataset(dataset_test_path, range(10), image_type=request.param)
    yield dataset, request.param


@pytest.fixture
def dataset_test_all_frames():
    frames = [
        {'session': '20210721-000004', 'capture': 'capture-0000000001'},
        {'session': '20210721-000004', 'capture': 'capture-0000000002'},
        {'session': '20210721-000004', 'capture': 'capture-0000000003'},
        {'session': '20210721-000004', 'capture': 'capture-0000000004'},
        {'session': '20210721-000004', 'capture': 'capture-0000000005'},
        {'session': '20210722-000003', 'capture': 'capture-0000000001'},
        {'session': '20210722-000003', 'capture': 'capture-0000000002'},
        {'session': '20210722-000003', 'capture': 'capture-0000000003'},
        {'session': '20210722-000003', 'capture': 'capture-0000000004'},
        {'session': '20210722-000003', 'capture': 'capture-0000000005'}
    ]
    yield frames


def test_to_tensor(dataset_frame):
    frame = dataset_frame
    to_tensor = ToTensor()
    sample = to_tensor(frame)

    assert sample['image'].shape == np.array(frame['image']).transpose(2, 0, 1).shape
    assert sample['depth'].shape == frame['depth'].transpose(2, 0, 1).shape
    assert sample['image'].numpy().sum() == pytest.approx(np.array(frame['image'], np.float32).sum())
    assert sample['depth'].numpy().sum() == pytest.approx(frame['depth'].sum())
    assert sample['depth'].min() >= 0
    assert sample['frame'] == frame['frame']
    assert sample['metadata'].equals(frame['metadata'])


def test_pytorch_dataset_frame(pytorch_dataset_frame, dataset_test_all_frames, dataset_test_path):
    dataset, data_type = pytorch_dataset_frame
    assert len(dataset) == 10

    for i, test_frame in enumerate(dataset_test_all_frames):
        frame = dataset[i]
        path = os.path.join(dataset_test_path, test_frame['session'], test_frame['capture'])
        image = Image.open(f"{path}.{data_type}")

        assert frame['image'].shape == (3, 816, 1440)
        assert frame['depth'].shape == (1, 816, 1440)
        assert os.path.normpath(frame['frame']) == os.path.normpath(path)
        assert frame['metadata']['session'] == test_frame['session']
        assert frame['metadata']['capture'] == test_frame['capture']
        assert frame['image'].numpy().sum() == pytest.approx(np.array(image, np.float32).sum())
        assert frame['depth'].numpy().sum() == pytest.approx(frame['depth'].sum())

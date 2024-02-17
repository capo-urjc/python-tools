import os

import numpy as np
import torch
from PIL import Image
from torch.utils.data import Dataset
from torchvision.transforms.functional import pil_to_tensor

from capo_tools.datasets.ETS2.ets2_tools import get_data
from capo_tools.datasets.ETS2.ets2_tools.depth_file import read_depth_file


class ETS2Dataset(Dataset):
    """
    Pytorch Dataset for ETS2 dataset, single frame

    The ETS2 Dataset, Synthetic Data from Video Games for Monocular Depth Estimation
    https://link.springer.com/chapter/10.1007/978-3-031-36616-1_30
    """
    def __init__(self, data_path, indexes, image_type: str = 'bmp', is_train: bool = False, transform=None):
        super(ETS2Dataset, self).__init__()
        self.data_path = data_path
        self.image_type = image_type
        self.is_train = is_train
        self.data = get_data(self.data_path)
        self.indexes = indexes if indexes is not None else list(range(len(self.data)))
        self.transform = transform if transform is not None else ToTensor()

    def __getitem__(self, item):
        """
        Get a single frame from the dataset
        Returns a tuple with the image and the depth map and a dictionary with the metadata
        """
        index = self.indexes[item]
        row = self.data.iloc[index]
        file_path = os.path.join(self.data_path, row['session'], row['capture'])
        image = Image.open(f"{file_path}.{self.image_type}")

        depth_file = read_depth_file(f"{file_path}.depth.raw")
        header = depth_file.header
        depth = depth_file.get_data()
        depth_shape = (header.height, header.width, 1)
        depth = np.reshape(depth, depth_shape)

        sample = {'image': image, 'depth': depth, 'frame': file_path, 'metadata': row}

        if self.transform:
            sample = self.transform(sample)

        return sample

    def __len__(self):
        """
        Get the number of frames in the dataset
        """
        return len(self.indexes)


class ETS2DatasetVideo(Dataset):
    """
    Pytorch Dataset for ETS2 dataset, video sequence

    The ETS2 Dataset, Synthetic Data from Video Games for Monocular Depth Estimation
    https://link.springer.com/chapter/10.1007/978-3-031-36616-1_30
    """
    def __init__(self, indexes, data_path, is_train=False, transform=None, max_depth: float = 80.0):
        super(ETS2DatasetVideo, self).__init__()
        self.data_path = data_path
        self.is_train = is_train
        self.data_indexes = indexes
        self.data = get_data(data_path)
        self.transform = transform
        self.maxDepth = max_depth

    def __getitem__(self, item):
        sequence_start_index = self.data_indexes[item]

        # TODO: parametrize number of frames in sequence
        sequence_end_index = sequence_start_index + 10

        data_rows = self.data.iloc[sequence_start_index:sequence_end_index, :]
        files = [os.path.join(self.data_path, x) for x in (data_rows['session'] + "/" + data_rows['capture']).tolist()]

        x = []
        y = []
        metadata = []

        for index, file in enumerate(files):
            file_path = f"{file}.jpg"
            image = Image.open(file_path)

            depth_file = read_depth_file(f"{file}.depth.raw")
            header = depth_file['header']
            depth = -depth_file['data']
            depth_shape = (header['height'], header['width'], 1)
            depth = np.reshape(depth, depth_shape)

            sample = {'image': image, 'depth': depth, 'frame': file}
            sample = self.transform(sample)
            x.append(sample['image'])
            y.append(sample['depth'])

            data_row = data_rows.iloc[index]
            metadata.append({"path": file_path, "session": data_row['session'], "capture": data_row['capture']})

        x = torch.stack((x))
        y = torch.stack((y))

        return x, y, metadata

    def __len__(self):
        return len(self.data_indexes)


class ToTensor(object):
    """
    Convert ETS2 sample to Tensors
    Returns a dictionary with two elements, image and depth, both as Tensors
    This class doesn't perform any transformation on the data, it just converts the data to Tensors
    """
    def __call__(self, sample):
        image, depth = sample['image'], sample['depth']
        image = pil_to_tensor(image).float()
        depth = torch.from_numpy(depth).float().permute(2, 0, 1)

        metadata = sample['metadata']
        frame = sample['frame']

        return {'image': image, 'depth': depth, 'frame': frame, 'metadata': metadata}

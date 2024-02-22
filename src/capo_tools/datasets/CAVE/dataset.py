import numpy as np
import os
import torch
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
import shutil
from matplotlib import pyplot as plt  # Added this line

from capo_tools.datasets.CAVE.utils.extract_random_patch import extract_random_patch
from capo_tools.datasets.CAVE.utils.downsampling import DownSampling_LossChannels
from capo_tools.datasets.CAVE.tools import download_CAVE


class CAVEDataset(Dataset):
    """
    Dataset class for loading Hyperspectral images dataset (CAVE).
    """

    def __init__(self, root_dir: str, patch_size: tuple, transform=None, download=False, mode='train'):
        """
        Initializes the dataset by loading the data.

        Args:
            root_dir (str): Root directory where the dataset is stored.
            patch_size (tuple): Size of the patch to be extracted from the images.
            transform (callable, optional): Optional transform to be applied on the samples.
            download (bool, optional): If True, downloads the dataset from the internet if it's not already downloaded.
            mode (str, optional): Mode of the dataset ('train', 'valid', 'test'.).
        """

        if not os.path.exists(root_dir):
            print('Downloading CAVE dataset:')
            download_CAVE(path_to_save=root_dir)

        if download:
            if not os.path.exists(root_dir):
                print('Downloading CAVE dataset:')
                download_CAVE(path_to_save=root_dir)
            else:
                print('Downloading and restoring CAVE dataset:')
                shutil.rmtree(root_dir)
                download_CAVE(path_to_save=root_dir)

        self.root_dir = os.path.join(root_dir, mode)
        self.patch_size = patch_size
        self.transform = transform

        self.images: list = []

        images_paths: list = sorted(os.listdir(self.root_dir))

        for path in images_paths:
            numpy_image: np.ndarray = np.load(os.path.join(self.root_dir, path))
            padded_image: np.ndarray = np.pad(numpy_image, (self.patch_size, self.patch_size, (0, 0)), 'constant',
                                              constant_values=0)
            self.images.append(padded_image)
        print('CAVE dataset loaded.')

    def __len__(self):
        """
        Get the total number of images in the dataset.

        Returns:
            int: Total number of images.
        """
        return len(self.images)

    def __getitem__(self, idx):
        """
        Get a sample from the dataset at the specified index.

        Args:
            idx (int): Index of the sample to retrieve.

        Returns:
            torch.Tensor: Transformed sample.
        """
        if torch.is_tensor(idx):
            idx = idx.tolist()

        idx = idx % len(self.images)

        image = self.images[idx]

        image: np.ndarray = extract_random_patch(image, self.patch_size)

        image = image.astype(np.float32)

        if self.transform:
            sample = self.transform(image)
        else:
            sample = transforms.ToTensor()(image)

        return sample
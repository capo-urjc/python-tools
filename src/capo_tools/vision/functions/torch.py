from typing import List

import torch
from torch import Tensor
from torchvision.transforms.functional import normalize


def denormalize(tensor: Tensor, mean: List[float], std: List[float], inplace: bool = False):
    """
    Denormalize a tensor

    Args:
        tensor: Tensor to denormalize
        mean: Mean values used for normalization
        std: Standard deviation values used for normalization
        inplace: If True, the tensor will be denormalize in place

    Returns:
        Unnormalized tensor
    """
    if not inplace:
        tensor = tensor.clone()

    mean: List = [-m / s for m, s in zip(mean, std)]
    std: List = [1 / s for s in std]

    return normalize(tensor, mean, std)

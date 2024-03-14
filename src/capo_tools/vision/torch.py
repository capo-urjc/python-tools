from typing import List

import torch

from capo_tools.vision.functions.torch import denormalize


class Denormalize(torch.nn.Module):
    def __init__(self, mean: List[float], std: List[float], inplace: bool = False):
        super().__init__()
        self.mean = mean
        self.std = std
        self.inplace = inplace

    def forward(self, tensor: torch.Tensor) -> torch.Tensor:
        """
        Denormalize a tensor
        """
        return denormalize(tensor, self.mean, self.std, self.inplace)
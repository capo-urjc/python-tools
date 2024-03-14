import pytest
import torch
from _pytest.fixtures import fixture
from torchvision.transforms import Normalize
from torchvision.transforms.functional import normalize

from capo_tools.vision.functions.torch import denormalize
from capo_tools.vision.torch import Denormalize


@fixture
def image_tensor():
    return torch.rand((3, 100, 100))


@fixture
def mean():
    return [0.485, 0.456, 0.406]


@fixture
def std():
    return [0.229, 0.224, 0.225]


def test_denormalize(image_tensor, mean, std):
    normalized_tensor = normalize(image_tensor, mean, std)
    denormalized_tensor = denormalize(normalized_tensor, mean, std)
    assert denormalized_tensor.sum() == pytest.approx(image_tensor.sum())


def test_denormalize_class(image_tensor, mean, std):
    norm = Normalize(mean, std)
    denorm = Denormalize(mean, std)
    assert denorm(norm(image_tensor)).sum() == pytest.approx(image_tensor.sum())

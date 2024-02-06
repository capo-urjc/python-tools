from capo_tools.datasets.ETS2.tools import is_pil_image, is_numpy_image


def test_pil_image():
    from PIL import Image
    img = Image.new('RGB', (100, 100))
    assert is_pil_image(img)


def test_not_pil_image():
    img = 'not an image'
    assert not is_pil_image(img)


def test_numpy_not_image():
    import numpy as np
    img = np.zeros((100, 100, 3))
    assert not is_pil_image(img)


def test_numpy_image():
    import numpy as np
    img = np.zeros((100, 100, 3))
    assert not is_pil_image(img)
    assert is_numpy_image(img)

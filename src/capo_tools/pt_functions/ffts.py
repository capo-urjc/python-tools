import torch
import torch.nn.functional as F


def psf2otf3d(kernel, input_shape, n=1):
    """
    Convert PSF (Point Spread Function) to OTF (Optical Transfer Function) in the frequency domain.

    Args:
        kernel (torch.Tensor): The PSF kernel.
        input_shape (tuple): Shape of the input tensor (channels, height, width).
        n (int): Number of samples. Defaults to 1.

    Returns:
        torch.Tensor: OTF of the kernel.
    """
    kc, kh, kw = kernel.size()
    c, h, w = input_shape
    pad_c, pad_h, pad_w = kc // 2, kh // 2, kw // 2

    # Pad the kernel and roll it
    kernel_pad = F.pad(kernel, (0, w - kw, 0, h - kh, 0, c - kc), "constant", 0)
    kernel_pad_roll = torch.roll(kernel_pad, shifts=(-pad_c, -pad_h, -pad_w), dims=(0, 1, 2))

    # Compute the OTF using FFT
    kernel_otf = torch.fft.fftn(kernel_pad_roll, s=(c, h, w))
    return kernel_otf


def ffp3d(tensor, kernel):
    """
    Perform 3D Fast Fourier Transform and Convolution in the frequency domain.

    Args:
        tensor (torch.Tensor): Input tensor.
        kernel (torch.Tensor): Convolution kernel.

    Returns:
        torch.Tensor: Convolved tensor.
    """
    c_org, h_org, w_org = tensor.size()
    kc, kh, kw = kernel.size()
    pad_c, pad_h, pad_w = kc // 2, kh // 2, kw // 2

    # Pad the input tensor
    tensor_pad = F.pad(tensor, (pad_w, pad_w, pad_h, pad_h, pad_c, pad_c))
    c, h, w = tensor_pad.size()

    # Compute FFT of kernel and input tensor
    kernel_fft = psf2otf3d(kernel, tensor_pad.size())
    tensor_fft = torch.fft.fftn(tensor_pad, s=(c, h, w))

    # Compute inverse FFT and extract the valid part
    k_conv_t = torch.fft.ifftn(kernel_fft * tensor_fft)[pad_c:pad_c + c_org, pad_h:pad_h + h_org, pad_w:pad_w + w_org]
    return k_conv_t

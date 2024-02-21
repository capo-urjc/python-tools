from capo_tools.pt_functions.ffts import ffp3d
import torch
import numpy as np
from PIL import Image
import torch.nn.functional as F

def test_ffp3d():
    # Defining 3D kernels in x, y, and z directions
    k_x = torch.tensor([[[0.0, 0.0, 0.0],
                        [0.0,  0.0, 0.0],
                        [0.0,  0.0, 0.0]],
                        [[0.0, -1.0, 0.0],
                        [0.0,  0.0, 0.0],
                        [0.0,  1.0, 0.0]],
                        [[0.0, 0.0, 0.0],
                        [0.0,  0.0, 0.0],
                        [0.0,  0.0, 0.0]]])

    k_y = torch.tensor([[[0.0, 0.0, 0.0],
                        [0.0,  0.0, 0.0],
                        [0.0,  0.0, 0.0]],
                        [[0.0, 0.0, 0.0],
                        [-1.0,  0.0, 1.0],
                        [0.0,  0.0, 0.0]],
                        [[0.0, 0.0, 0.0],
                        [0.0,  0.0, 0.0],
                        [0.0,  0.0, 0.0]]])

    k_z = torch.tensor([[[0.0, 0.0, 0.0],
                        [0.0,  -1.0, 0.0],
                        [0.0,  0.0, 0.0]],
                        [[0.0, 0.0, 0.0],
                        [0.0,  0.0, 0.0],
                        [0.0,  0.0, 0.0]],
                        [[0.0, 0.0, 0.0],
                        [0.0,  1.0, 0.0],
                        [0.0,  0.0, 0.0]]])

    # Fetching image from URL and converting it to tensor
    im = Image.open('resources/test_image.jpg')
    im = np.array(im)
    im = torch.tensor(im).permute(2, 0, 1)/255

    # Flipping kernels
    k_x_flipped = torch.flip(k_x, [0, 1, 2])
    k_y_flipped = torch.flip(k_y, [0, 1, 2])
    k_z_flipped = torch.flip(k_z, [0, 1, 2])

    # Applying convolution with flipped kernels
    kx_conv_im = F.conv3d(im[None, None, ...], k_x_flipped[None, None, ...], groups=1, padding='same')[0, 0, ...]
    ky_conv_im = F.conv3d(im[None, None, ...], k_y_flipped[None, None, ...], groups=1, padding='same')[0, 0, ...]
    kz_conv_im = F.conv3d(im[None, None, ...], k_z_flipped[None, None, ...], groups=1, padding='same')[0, 0, ...]

    # Applying 3D Fast Fourier Transform on image with original kernels
    kx_conv_im_fft = torch.real(ffp3d(im, k_x))
    ky_conv_im_fft = torch.real(ffp3d(im, k_y))
    kz_conv_im_fft = torch.real(ffp3d(im, k_z))

    assert torch.allclose(kx_conv_im, kx_conv_im_fft, atol=1e-05)
    assert torch.allclose(ky_conv_im, ky_conv_im_fft, atol=1e-05)
    assert torch.allclose(kz_conv_im, kz_conv_im_fft, atol=1e-05)


    # print('Max absolute difference for kx {}'.format(torch.abs(kx_conv_im - kx_conv_im_fft).max()))
    # print('Max absolute difference for ky {}'.format(torch.abs(ky_conv_im - ky_conv_im_fft).max()))
    # print('Max absolute difference for kz {}'.format(torch.abs(kz_conv_im - kz_conv_im_fft).max()))
    # # Create subplots with 3 rows and 3 columns
    # fig, axs = plt.subplots(3, 3, figsize=(15, 15))
    #
    # # Define the pairs of images and their titles
    # image_pairs = [
    #     (kx_conv_im, kx_conv_im_fft, 'kx_conv_im', 'kx_conv_im_fft'),
    #     (ky_conv_im, ky_conv_im_fft, 'ky_conv_im', 'ky_conv_im_fft'),
    #     (kz_conv_im, kz_conv_im_fft, 'kz_conv_im', 'kz_conv_im_fft')
    # ]
    #
    # # Plot each pair along with their absolute difference
    # for i, (im, im_fft, title_im, title_im_fft) in enumerate(image_pairs):
    #     # Plot the first image
    #     axs[i, 0].imshow(im.permute(1, 2, 0).numpy())
    #     axs[i, 0].set_title(title_im)
    #     axs[i, 0].axis('off')
    #
    #     # Plot the second image
    #     axs[i, 1].imshow(im_fft.permute(1, 2, 0).numpy())
    #     axs[i, 1].set_title(title_im_fft)
    #     axs[i, 1].axis('off')
    #
    #     # Plot the absolute difference
    #     axs[i, 2].imshow((im - im_fft).abs().permute(1, 2, 0).numpy())
    #     axs[i, 2].set_title('|{} - {}|'.format(title_im, title_im_fft))
    #     axs[i, 2].axis('off')
    #
    # # Adjust layout
    # plt.tight_layout()
    #
    # # Show the plots
    # plt.show()
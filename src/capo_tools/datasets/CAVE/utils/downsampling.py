import torch

class DownSampling_LossChannels(torch.nn.Module):
    """
    Crop the given image at a random location.
    """
    def __init__(self, loss_ch=None):
        super().__init__()
        self.loss_ch = loss_ch or list(range(1, 31, 2))

    def forward(self, y):
        """
        Args:
            y (Tensor): Image to be downsampled channel-wise. [ch, height, width]

        Returns:
            Dict of Tensors: {'x': Downsampled image with lost channels set to 0, 'y': y}
        """
        x = y.clone()
        x[self.loss_ch, ...] = 0

        return {'x': x, 'y': y}

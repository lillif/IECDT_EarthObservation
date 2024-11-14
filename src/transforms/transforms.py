
import json
import numpy as np
import torch


class ToTensorTransform:
    """
    Convert numpy array to PyTorch tensor
    """

    def __init__(self, dtype=torch.float32):
        self.dtype = dtype

    def __call__(self, data, **kwargs):
        # Convert to tensor
        tensor = torch.as_tensor(data, dtype=self.dtype)
        return tensor


class MeanStdNormaliseTransform:
    def __init__(self, mean: float, std: float):
        self.mean = mean
        self.std = std

    def __call__(self, data):
        # Convert to tensor
        data = (data - self.mean) / self.std
        return data


class NanMeanFillTransform:
    """
    Replaces NaN values in a numpy array with the mean of the non-NaN values of that image
    """

    def __init__(self, key="data"):
        self.key = key

    def __call__(self, data):
        # replace NaN values
        data = np.nan_to_num(data, nan=np.nanmean(data))
        return data

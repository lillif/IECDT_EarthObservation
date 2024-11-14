import autoroot # required for imports from src
from src.transforms import MeanStdNormaliseTransform, NanMeanFillTransform, ToTensorTransform
from torchvision.transforms import Compose


class SunnyOxfordModisTransform:

    """Transform pipeline for MODIS files."""

    def __init__(
        self,
        mean: float,
        std: float,
        fill_nan: bool = True,
    ):
        transforms_list = [
            MeanStdNormaliseTransform(
                mean=mean,
                std=std,
            )
        ]

        if fill_nan:
            transforms_list.append(NanMeanFillTransform())

        transforms_list.append(ToTensorTransform())

        self.transform = Compose(transforms_list)

    def __call__(self, sample):
        s = self.transform(sample)
        return s
    
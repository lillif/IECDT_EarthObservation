import pandas as pd
import numpy as np
from loguru import logger
from datetime import datetime
from torch.utils.data import Dataset
from typing import Callable
import torch


class SunnyOxfordDataset(Dataset):
    def _get_date_from_filename(self, filename: str) -> datetime:
        """
        Extract the date from a MODIS filename.
        """
        return datetime.strptime(filename.split("/")[-1].split(".")[0], "%Y-%m-%d")
    
    def _match_aopp_observation(self, modis_filename: str) -> dict:
        """
        Return the AOPP observation that matches the MODIS image date.
        """
        modis_date = self._get_date_from_filename(modis_filename)
        aopp_row = self.aopp_dataframe[self.aopp_dataframe["date"] == modis_date]
        if len(aopp_row) == 0:
            logger.warning(f"No AOPP observation found for {modis_date}")
            return None
        else:
            return aopp_row.to_dict(orient="records")[0]
        
    def __init__(
        self,
        modis_filenames: list[str],
        aopp_dataframe: pd.DataFrame,
        transforms: Callable | None = None,
    ):
        self.modis_filenames = modis_filenames
        self.aopp_dataframe = aopp_dataframe
        self.transforms = transforms

    def setup(self, stage):
        pass

    def prepare_data(self):
        pass

    def __getitem__(self, ind) -> np.ndarray:
        item = {}
        x = np.load(self.patches_filenames[ind])["arr_0"]
        if self.transforms is not None:
            # transforms takes a numpy array and returns a torch array
            x = self.transforms(x)
        if not isinstance(x, torch.Tensor):
            logger.error(f"Transforms did not return a torch tensor, but {type(x)}")
        item["modis_image"] = x
        item["aopp_observation"] = self._match_aopp_observation(self.modis_filenames[ind])
        return item

    def __len__(self):
        return len(self.modis_filenames)
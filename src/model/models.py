import os
import pickle
from abc import abstractmethod

import imageio
import imageio.core.util
import nibabel as nib


# remove imageio warnings
def silence_imageio_warning(*args, **kwargs):
    pass


imageio.core.util._precision_warn = silence_imageio_warning


class BaseWidgetModel:
    def __init__(self):
        return

    @abstractmethod
    def compute(self, view_input_dict: dict):
        pass


class LoadWidgetModel:
    def compute(self, view_input_dict: dict):
        output = self.load(view_input_dict.get("path"))
        return output

    def load(self, path: str):
        """
        this method has a vocation to load any type of file
        """
        _, ext = os.path.splitext(path)
        if ext == ".txt":
            with open(path, "r") as f:
                data = f.read()
        elif ext == ".pkl":
            with open(path, "rb") as f:
                data = pickle.load(f)
        elif ext == ".nii" or path.endswith(".nii.gz"):
            data = nib.load(path).get_fdata()
        elif ext in [".png", ".jpg"]:
            data = imageio.imread(path)
            if data.ndim == 3:
                # remove alpha channel
                if data.shape[2] == 4:
                    data = data[:, :, :3]
                # convert to gray if same value everywhere
                # in each r, g, b canal
                if (
                    data.shape[2] == 3
                    and (data[:, :, 0] == data[:, :, 1]).all()
                    and (data[:, :, 1] == data[:, :, 2]).all()
                ):
                    data = data[:, :, 0]
        else:
            raise TypeError("{} not handle yet".format(ext))
        return data

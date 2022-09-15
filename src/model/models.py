import os
import sys
from abc import abstractmethod

import nibabel as nib
import numpy as np
from PIL import Image
from skimage import morphology
from src.metadata.metadata import OPERATION_DICT
from src.model.mixin import OutputImageMixin


class WidgetModel:
    @abstractmethod
    def compute(self, *args, **kwargs):
        pass


class LoadFileWM(WidgetModel):
    accepted_extensions = []

    def compute(self, file_path: str):
        exception = self.check_path(file_path)
        if exception is not None:
            return exception
        return self.load(file_path)

    def check_path(self, file_path: str) -> Exception or None:
        _, ext = os.path.splitext(file_path)
        if not os.path.isfile(file_path):
            return Exception(f"'{file_path}' is not a file")
        for ext in self.accepted_extensions:
            if file_path.lower().endswith(ext):
                return
        return Exception("Accepted files are " + ", ".join(self.accepted_extensions))

    @abstractmethod
    def load(self, file_path: str):
        pass


class Load2dImageWM(OutputImageMixin, LoadFileWM):
    accepted_extensions = [".png", ".jpg", ".jpeg"]

    def load(self, file_path: str) -> np.ndarray:
        im = Image.open(file_path)
        arr = np.array(im)
        return self.downsize_raw_array(arr)


class Load3dImageWM(OutputImageMixin, LoadFileWM):
    accepted_extensions = [".nii", ".nii.gz"]

    def load(self, file_path: str) -> np.ndarray:
        print("compute3d")
        im = nib.load(file_path)
        arr = im.get_fdata()
        return self.downsize_raw_array(arr)


class LoadTextWM(LoadFileWM):
    accepted_extensions = [".txt"]

    def load(self, file_path: str) -> str:
        with open(file_path, "rb") as f:
            text_bytes = f.read()
        text = text_bytes.decode("utf-8")
        return text


class BasicMorphoWM(WidgetModel):
    pass


class BasicMorpho2dWM(OutputImageMixin, BasicMorphoWM):
    def compute(
        self,
        arr: np.ndarray or Exception,
        size: int,
        operation: str,
        is_round_shape: bool,
    ):
        if isinstance(arr, Exception):
            return Exception("Wrong parent output.")
        function = OPERATION_DICT["morpho:basic"].get(operation)
        selem = (
            morphology.disk(size) if is_round_shape else morphology.square(size * 2 + 1)
        )
        if arr.ndim == 3:
            # in case of rgb or rgba images
            for i in range(arr.shape[2]):
                arr[:, :, i] = function(arr[:, :, i], selem)
        elif arr.ndim == 2:
            arr = function(arr, selem)
        return self.downsize_raw_array(arr)


class BasicMorpho3dWM(OutputImageMixin, BasicMorphoWM):
    def compute(
        self,
        arr: np.ndarray or Exception,
        size: int,
        operation: str,
        is_round_shape: bool,
    ):
        if isinstance(arr, Exception):
            return Exception("Wrong parent output.")
        function = OPERATION_DICT["morpho:basic"].get(operation)
        selem = (
            morphology.ball(size) if is_round_shape else morphology.cube(size * 2 + 1)
        )
        arr = function(arr, selem)
        return self.downsize_raw_array(arr)

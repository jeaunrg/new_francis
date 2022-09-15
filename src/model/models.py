import os
import sys
from abc import abstractmethod

import nibabel as nib
import numpy as np
from PIL import Image
from skimage import morphology
from src.metadata.metadata import OPERATION_DICT
from src.model.mixin import OutputModelMixin


class WidgetModel:
    def get_heritage(self) -> dict:
        """attributes that children can inherits"""
        return {}

    @abstractmethod
    def compute(self, *args, **kwargs):
        pass


class LoadFileWM(WidgetModel):
    accepted_extensions = []

    def check_path(self, file_path: str) -> Exception or None:
        _, ext = os.path.splitext(file_path)
        if not os.path.isfile(file_path):
            return Exception(f"'{file_path}' is not a file")
        for ext in self.accepted_extensions:
            if file_path.lower().endswith(ext):
                return
        return Exception("Accepted files are " + ", ".join(self.accepted_extensions))

    def compute(self, file_path: str):
        exception = self.check_path(file_path)
        if exception is not None:
            return exception
        return self.load(file_path)

    @abstractmethod
    def load(self, file_path: str):
        pass


class Load2dImageWM(OutputModelMixin, LoadFileWM):
    accepted_extensions = [".png", ".jpg", ".jpeg"]

    @OutputModelMixin.downsize
    def load(self, file_path: str) -> np.ndarray:
        im = Image.open(file_path)
        return np.array(im)


class Load3dImageWM(OutputModelMixin, LoadFileWM):
    accepted_extensions = [".nii", ".nii.gz"]

    @OutputModelMixin.downsize
    def load(self, file_path: str) -> np.ndarray:
        im = nib.load(file_path)
        return im.get_fdata()


class LoadTextWM(LoadFileWM):
    accepted_extensions = [".txt"]

    def load(self, file_path: str) -> str:
        with open(file_path, "rb") as f:
            text_bytes = f.read()
        text = text_bytes.decode("utf-8")
        return text


class BasicMorpho2dWM(OutputModelMixin, WidgetModel):
    @OutputModelMixin.downsize
    def compute(
        self,
        arr: np.ndarray,
        size: int,
        operation: str,
        is_round_shape: bool,
    ) -> np.ndarray or Exception:
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
        return arr


class BasicMorpho3dWM(OutputModelMixin, WidgetModel):
    @OutputModelMixin.downsize
    def compute(
        self,
        arr: np.ndarray or Exception,
        size: int,
        operation: str,
        is_round_shape: bool,
    ) -> np.ndarray or Exception:
        function = OPERATION_DICT["morpho:basic"].get(operation)
        selem = (
            morphology.ball(size) if is_round_shape else morphology.cube(size * 2 + 1)
        )
        arr = function(arr, selem)
        return arr

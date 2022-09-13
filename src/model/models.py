import os
from abc import abstractmethod

import nibabel as nib
import numpy as np
from PIL import Image
from skimage import morphology
from src.metadata.metadata import OPERATION_DICT
from src.model.mixin import OutputImageMixin


class WidgetModel:
    @abstractmethod
    def compute(self, view_input_dict: dict):
        pass


class LoadFileWM(WidgetModel):
    accepted_extensions = []

    def compute(self, file_path: str):
        exception = self.check_path(file_path)
        if exception is not None:
            return exception
        else:
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


class Load2dImageWM(LoadFileWM):
    accepted_extensions = [".png", ".jpg", ".jpeg"]

    def load(self, file_path: str) -> np.ndarray:
        im = Image.open(file_path)
        arr = np.array(im)
        return arr


class Load3dImageWM(OutputImageMixin, LoadFileWM):
    accepted_extensions = [".nii", ".nii.gz"]

    def load(self, file_path: str) -> np.ndarray:
        im = nib.load(file_path)
        arr = im.get_fdata()
        return self.downgrade_raw_array(arr)


class LoadTextWM(LoadFileWM):
    accepted_extensions = [".txt"]

    def load(self, file_path: str) -> str:
        with open(file_path, "rb") as f:
            text_bytes = f.read()
        text = text_bytes.decode("utf-8")
        return text


class BasicMorphoWM(OutputImageMixin, WidgetModel):
    def compute(self, im: np.ndarray or Exception):
        return self.downgrade_raw_array(im)


class BasicMorpho2dWM(BasicMorphoWM):
    def compute(
        self,
        im: np.ndarray or Exception,
        size: int,
        operation: str,
        is_round_shape: bool,
    ):
        if isinstance(im, Exception):
            return Exception("Wrong parent output.")
        elif size != 0:
            function = OPERATION_DICT["morpho:basic"].get(operation)
            selem = (
                morphology.disk(size)
                if is_round_shape
                else morphology.square(size * 2 + 1)
            )
            if im.ndim == 3:
                # in case of rgb or rgba images
                for i in range(im.shape[2]):
                    im[:, :, i] = function(im[:, :, i], selem)
            elif im.ndim == 2:
                im = function(im, selem)
        return super().compute(im)


class BasicMorpho3dWM(BasicMorphoWM):
    def compute(
        self,
        im: np.ndarray or Exception,
        size: int,
        operation: str,
        is_round_shape: bool,
    ):
        if isinstance(im, Exception):
            return Exception("Wrong parent output.")
        elif size != 0:
            function = OPERATION_DICT["morpho:basic"].get(operation)
            selem = (
                morphology.ball(size)
                if is_round_shape
                else morphology.cube(size * 2 + 1)
            )
            im = function(im, selem)
        return super().compute(im)

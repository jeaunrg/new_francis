import os
from abc import abstractmethod

import numpy as np
from PIL import Image
from skimage import morphology
from src.metadata.metadata import OPERATION_DICT


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
        if ext.lower() not in self.accepted_extensions:
            return Exception(
                "Accepted files are " + ", ".join(self.accepted_extensions)
            )

    @abstractmethod
    def load(self, file_path: str):
        pass


class LoadImageWM(LoadFileWM):
    accepted_extensions = [".png", ".jpg", ".jpeg"]

    def load(self, file_path: str) -> np.ndarray:
        im = Image.open(file_path)
        arr = np.array(im)
        return arr


class LoadTextWM(LoadFileWM):
    accepted_extensions = [".txt"]

    def load(self, file_path: str) -> str:
        with open(file_path, "rb") as f:
            text_bytes = f.read()
        text = text_bytes.decode("utf-8")
        return text


class BasicMorphoWM(WidgetModel):
    def _get_selem(self, shape, size: int, is_round_shape: bool):
        if len(shape) == 2:
            selem = (
                morphology.disk(size)
                if is_round_shape
                else morphology.square(size * 2 + 1)
            )
        elif len(shape) == 3:
            selem = (
                morphology.ball(size)
                if is_round_shape
                else morphology.cube(size * 2 + 1)
            )
        return selem

    def compute(
        self,
        im: np.ndarray or Exception,
        size: int,
        operation: str,
        is_round_shape: bool,
    ):
        if isinstance(im, Exception):
            return Exception("Wrong parent output.")
        elif size == 0:
            return im
        selem = self._get_selem(im.shape, size, is_round_shape)
        function = OPERATION_DICT["morpho:basic"].get(operation)
        return function(im, selem)

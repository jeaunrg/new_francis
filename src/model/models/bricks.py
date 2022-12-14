import os
import sys
from abc import abstractmethod

import nibabel as nib
import numpy as np
from PIL import Image
from skimage import morphology
from src.metadata.metadata import OPERATION_DICT
from src.model.models.base import WidgetModel
from src.model.models.mixin import CompressionMixin

"""
from skimage import (
    color, feature, filters, measure, morphology, segmentation, util
)

image = skimage.data.human_mitosis()
thresholds = filters.threshold_multiotsu(image, classes=3)
regions = np.digitize(image, bins=thresholds)
cells = image > thresholds[0]
dividing = image > thresholds[1]
labeled_cells = measure.label(cells)
labeled_dividing = measure.label(dividing)
naive_mi = labeled_dividing.max() / labeled_cells.max()

higher_threshold = 125
dividing = image > higher_threshold
smoother_dividing = filters.rank.mean(util.img_as_ubyte(dividing),
                                      morphology.disk(4))
binary_smoother_dividing = smoother_dividing > 20
"""


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


class Load2dImageWM(CompressionMixin, LoadFileWM):
    accepted_extensions = [".png", ".jpg", ".jpeg"]

    @CompressionMixin.downsize
    def load(self, file_path: str) -> np.ndarray:
        im = Image.open(file_path)
        return np.array(im)


class Load3dImageWM(CompressionMixin, LoadFileWM):
    accepted_extensions = [".nii", ".nii.gz"]

    @CompressionMixin.downsize
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


class BasicMorpho2dWM(CompressionMixin, WidgetModel):
    @CompressionMixin.downsize
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


class BasicMorpho3dWM(CompressionMixin, WidgetModel):
    @CompressionMixin.downsize
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


class AdvancedMorphoWM(CompressionMixin, WidgetModel):
    @CompressionMixin.downsize
    def compute(self, arr: np.ndarray, operation: str) -> np.ndarray or Exception:
        function = OPERATION_DICT["morpho:advanced"].get(operation)
        arr = function(arr)
        return arr


class FilterWM(CompressionMixin, WidgetModel):
    @CompressionMixin.downsize
    def compute(self, arr: np.ndarray, operation: str) -> np.ndarray or Exception:
        function = OPERATION_DICT["filter"].get(operation)
        arr = function(arr)
        return arr


class ThresholdWM(WidgetModel):
    def compute(self, arr: np.ndarray, operation: str) -> list or Exception:
        function = OPERATION_DICT["threshold"].get(operation)
        thresholds = function(arr)
        return thresholds

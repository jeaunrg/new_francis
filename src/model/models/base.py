import os
import sys
from abc import abstractmethod

import nibabel as nib
import numpy as np
from PIL import Image
from skimage import morphology
from src.metadata.metadata import OPERATION_DICT
from src.model.models.mixin import CompressionMixin


class WidgetModel:
    def __init__(self):
        self.has_downsized_output = False

    def set_inherited_attr(self, **kwargs):
        self.__dict__.update(kwargs)

    def get_heritage(self) -> dict:
        """attributes that children can inherits"""
        return {}

    @abstractmethod
    def compute(self, *args, **kwargs):
        pass

    def clean(self):
        pass


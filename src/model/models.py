import os
from abc import abstractmethod

import numpy as np
from PIL import Image


class WidgetModel:
    @abstractmethod
    def compute(self, view_input_dict: dict):
        pass


class LoadFileWM(WidgetModel):
    def compute(self, view_input_dict: dict):
        output = self.load(view_input_dict.get("path"))
        return output

    @abstractmethod
    def load(self, path: str):
        pass


class LoadImageWM(LoadFileWM):
    def load(self, path: str) -> np.ndarray:
        _, ext = os.path.splitext(path)
        accepted_extensions = [".png", ".jpg", ".jpeg"]
        if not os.path.isfile(path):
            return Exception(f"'{path}' is not a file")
        if ext.lower() not in accepted_extensions:
            return Exception("Accepted files are " + ", ".join(accepted_extensions))
        im = Image.open(path)
        arr = np.array(im)
        return arr

import os
from abc import abstractmethod

import numpy as np
from PIL import Image


class WidgetModel:
    @abstractmethod
    def compute(self, view_input_dict: dict):
        pass


class LoadFileWM(WidgetModel):
    accepted_extensions = []

    def compute(self, view_input_dict: dict):
        file_path = view_input_dict.get("path")
        exception = self.check_path(file_path)
        if exception is not None:
            return exception
        else:
            return self.load(file_path)

    def check_path(self, path: str):
        _, ext = os.path.splitext(path)
        if not os.path.isfile(path):
            return Exception(f"'{path}' is not a file")
        if ext.lower() not in self.accepted_extensions:
            return Exception(
                "Accepted files are " + ", ".join(self.accepted_extensions)
            )

    @abstractmethod
    def load(self, path: str):
        pass


class LoadImageWM(LoadFileWM):
    accepted_extensions = [".png", ".jpg", ".jpeg"]

    def load(self, path: str) -> np.ndarray:
        im = Image.open(path)
        arr = np.array(im)
        return arr


class LoadTextWM(LoadFileWM):
    accepted_extensions = [".txt"]

    def load(self, path: str) -> np.ndarray:
        with open(path, "rb") as f:
            text_bytes = f.read()
        text = text_bytes.decode("utf-8")
        return text

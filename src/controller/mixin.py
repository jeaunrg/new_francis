from typing import Union

import numpy as np
from PyQt5 import QtCore, QtGui
from src.controller.utils import qimage_from_array, raise_exception


class Output2dImageMixin:
    def set_view_output(self, output: Union[np.ndarray, Exception]):
        if isinstance(output, Exception):
            return raise_exception(output)
        qimage = qimage_from_array(output)
        if qimage is None:
            message = f"Image format not known. Shape={output.shape}, dtype={output.dtype}, max={output.max()}, min={output.min()}"
            return raise_exception(Exception(message))
        pixmap = QtGui.QPixmap(qimage)
        pixmap = pixmap.scaledToWidth(300, QtCore.Qt.FastTransformation)
        self.view.image.setPixmap(pixmap)


class Output3dImageMixin(Output2dImageMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.section = [0, 0, 0]
        self.viewpoint = 0

    def make_connections(self):
        super().make_connections()
        self.view.image.double_clicked.connect(lambda: self.update_viewpoint())
        self.view.image.scrolled.connect(lambda value: self.update_section(value))

    def update_viewpoint(self):
        self.viewpoint += 1
        if self.viewpoint == 3:
            self.viewpoint = 0
        self.update_section()

    def update_section(self, value: int = 0):
        self.section[self.viewpoint] += value
        if self.section[self.viewpoint] < 0:
            self.section[self.viewpoint] = 0
        elif self.section[self.viewpoint] > self.output.shape[self.viewpoint]:
            self.section[self.viewpoint] = self.output.shape[self.viewpoint]
        self.set_view_output(self.output)

    def set_view_output(self, output: Union[np.ndarray, Exception]):
        if isinstance(output, Exception):
            return raise_exception(output)
        if self.viewpoint == 0:
            output = self.output[self.section[0]]
        elif self.viewpoint == 1:
            output = self.output[:, self.section[1]]
        elif self.viewpoint == 2:
            output = self.output[:, :, self.section[2]]
        return super().set_view_output(output)

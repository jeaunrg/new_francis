import copy
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
    def make_connections(self):
        super().make_connections()
        self.view.image.double_clicked.connect(
            lambda: (self.update_viewpoint(), self.set_view_output())
        )
        self.view.image.scrolled.connect(
            lambda value_delta: (
                self.update_section(value_delta=value_delta),
                self.set_view_output(),
            )
        )

    def update_viewpoint(self, value_delta: int = 1, value: int = None):
        if value is None:
            self.viewpoint += value_delta
        else:
            self.viewpoint = value
        if self.viewpoint == 3:
            self.viewpoint = 0

    def update_section(self, value_delta: int = 0, value: int = None):
        if isinstance(self.output, Exception):
            return
        if value is None:
            self.sections[self.viewpoint] += value_delta
        else:
            self.sections[self.viewpoint] = value
        if self.sections[self.viewpoint] < 0:
            self.sections[self.viewpoint] = 0
        elif self.sections[self.viewpoint] >= self.output.shape[self.viewpoint]:
            self.sections[self.viewpoint] = self.output.shape[self.viewpoint] - 1

    def synchronize(self):
        for w in self.child_list + self.parent_list:
            if w.viewpoint != self.viewpoint or w.sections != self.sections:
                w.update_viewpoint(value=self.viewpoint)
                w.update_section(value=self.sections[self.viewpoint])
                w.set_view_output()

    def init_sections_and_viewpoint(self):
        if len(self.parent_list) == 0:
            s1, s2, s3 = self.output.shape
            self.viewpoint = 0
            self.sections = [int(s1 / 2), int(s2 / 2), int(s3 / 2)]
        else:
            w = self.parent_list[0]
            for i in range(3):
                self.update_viewpoint(value=i)
                self.update_section(value=w.sections[i])
            self.update_viewpoint(value=w.viewpoint)

    def set_view_output(self, output: Union[np.ndarray, Exception] = None):
        if not isinstance(output, Exception):
            if isinstance(output, np.ndarray):
                self.init_sections_and_viewpoint()
            self.synchronize()
            if self.viewpoint == 0:
                output = self.output[self.sections[0]]
            elif self.viewpoint == 1:
                output = self.output[:, self.sections[1]]
            elif self.viewpoint == 2:
                output = self.output[:, :, self.sections[2]]
        return super().set_view_output(output)


class OutputTextMixin:
    def set_view_output(self, output: Union[str, Exception]):
        if isinstance(output, Exception):
            return raise_exception(output)
        self.view.text.setText(output)

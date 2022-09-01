from abc import abstractmethod

import numpy as np
from PyQt5 import QtCore, QtGui
from src.controller.utils import browse_path
from src.model.models import BaseWidgetModel, LoadWidgetModel
from src.view.views import BaseWidgetView, LoadWidgetView


class WidgetController:
    model_class = BaseWidgetModel
    view_class = BaseWidgetView

    def __init__(self):
        self.model = self.model_class()
        self.view = self.view_class()
        self.make_connections()

    def make_connections(self):
        self.view.button.clicked.connect(lambda: self.submit())

    def submit(self):
        view_input_dict = self.get_view_input()
        output = self.model.compute(view_input_dict)
        self.set_view_output(output)

    @abstractmethod
    def get_view_input(self) -> dict:
        pass

    @abstractmethod
    def set_view_output(self, output):
        pass


class LoadWidgetController(WidgetController):
    model_class = LoadWidgetModel
    view_class = LoadWidgetView

    def make_connections(self):
        super().make_connections()
        self.view.browse.clicked.connect(lambda: self.set_browse_path())

    def set_browse_path(self):
        filename = browse_path()
        if filename != "":
            self.view.path.setText(filename)
            self.view.path.setToolTip(filename)

    def get_view_input(self) -> dict:
        return {"path": self.view.path.text()}

    def set_view_output(self, output):
        if isinstance(output, np.ndarray):
            qimage = QtGui.QImage(
                output,
                output.shape[1],
                output.shape[0],
                QtGui.QImage.Format_RGB888,
            )
            pixmap = QtGui.QPixmap(qimage)
            pixmap = pixmap.scaled(640, 400, QtCore.Qt.KeepAspectRatio)
            self.view.image.setPixmap(pixmap)

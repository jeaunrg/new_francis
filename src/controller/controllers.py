from abc import abstractmethod
from typing import Union

import numpy as np
from PyQt5 import QtCore, QtGui
from src.controller.utils import browse_path, qimage_from_array, raise_exception
from src.metadata.metadata import WidgetEnum
from src.model.models import (
    BasicMorphoWM,
    LoadFileWM,
    LoadImageWM,
    LoadTextWM,
    WidgetModel,
)
from src.view.items import WidgetItem
from src.view.views import (
    BasicMorphoWV,
    LoadFileWV,
    LoadImageWV,
    LoadTextWV,
    WidgetView,
)


class Widget:
    model_class = WidgetModel
    view_class = WidgetView

    def __init__(
        self, name: WidgetEnum, position: QtCore.QPointF, parent_list: list = []
    ):
        self.name = name
        self.parent_list = parent_list
        self.model = self.model_class()
        self.view = self.view_class()
        self.item = WidgetItem(self.view, position)
        self.output = Exception("No output yet.")
        self.make_connections()

    def make_connections(self):
        self.view.button.clicked.connect(lambda: self.submit())

    def submit(self):
        view_input_dict = self.get_view_input()
        self.output = self.model.compute(**view_input_dict)
        self.set_view_output(self.output)

    @abstractmethod
    def get_view_input(self) -> dict:
        pass

    @abstractmethod
    def set_view_output(self, output):
        pass


class OutputImageMixin:
    def set_view_output(self, output: Union[np.ndarray, Exception]):
        if isinstance(output, Exception):
            return raise_exception(output)
        qimage = qimage_from_array(output)
        if qimage is None:
            message = (
                f"Image format not known. shape={output.shape}, dtype={output.dtype}"
            )
            return raise_exception(Exception(message))
        pixmap = QtGui.QPixmap(qimage)
        pixmap = pixmap.scaledToWidth(300, QtCore.Qt.FastTransformation)
        self.view.image.setPixmap(pixmap)


class LoadFileW(Widget):
    model_class = LoadFileWM
    view_class = LoadFileWV

    def make_connections(self):
        super().make_connections()
        self.view.browse.clicked.connect(lambda: self.set_browse_path())

    def set_browse_path(self):
        filename = browse_path()
        if filename != "":
            self.view.path.setText(filename)
            self.view.path.setToolTip(filename)

    def get_view_input(self) -> dict:
        return {"file_path": self.view.path.text()}


class LoadImageW(OutputImageMixin, LoadFileW):
    model_class = LoadImageWM
    view_class = LoadImageWV


class LoadTextW(LoadFileW):
    model_class = LoadTextWM
    view_class = LoadTextWV

    def set_view_output(self, output: Union[str, Exception]):
        if isinstance(output, Exception):
            return raise_exception(output)
        self.view.text.setText(output)


class BasicMorphoW(OutputImageMixin, Widget):
    model_class = BasicMorphoWM
    view_class = BasicMorphoWV

    def get_view_input(self) -> dict:
        return {
            "im": self.parent_list[0].output,
            "operation": self.view.operations.checkedButton().text(),
            "size": self.view.size.value(),
            "is_round_shape": self.view.is_round_shape.isChecked(),
        }

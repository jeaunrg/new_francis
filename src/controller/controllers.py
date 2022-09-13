from abc import abstractmethod
from typing import Union

from PyQt5 import QtCore
from src.controller.mixin import Output2dImageMixin, Output3dImageMixin, OutputTextMixin
from src.controller.utils import browse_path
from src.metadata.metadata import WidgetEnum
from src.model.models import (
    BasicMorpho2dWM,
    BasicMorpho3dWM,
    BasicMorphoWM,
    Load2dImageWM,
    Load3dImageWM,
    LoadFileWM,
    LoadTextWM,
    WidgetModel,
)
from src.view.items import WidgetItem
from src.view.views import (
    BasicMorpho2dWV,
    BasicMorpho3dWV,
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
        for parent in parent_list:
            parent.child_list.append(self)
        self.child_list = []
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

    def get_view_output(self):
        return self.output

    @abstractmethod
    def set_view_output(self, output):
        pass


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


class Load2dImageW(Output2dImageMixin, LoadFileW):
    model_class = Load2dImageWM
    view_class = LoadImageWV


class Load3dImageW(Output3dImageMixin, LoadFileW):
    model_class = Load3dImageWM
    view_class = LoadImageWV


class LoadTextW(OutputTextMixin, LoadFileW):
    model_class = LoadTextWM
    view_class = LoadTextWV


class BasicMorphoW(Widget):
    model_class = BasicMorphoWM
    view_class = BasicMorphoWV

    def get_view_input(self) -> dict:
        return {
            "im": self.parent_list[0].get_view_output(),
            "operation": self.view.operations.checkedButton().text(),
            "size": self.view.size.value(),
            "is_round_shape": self.view.is_round_shape.isChecked(),
        }


class BasicMorpho2dW(Output2dImageMixin, BasicMorphoW):
    model_class = BasicMorpho2dWM
    view_class = BasicMorpho2dWV


class BasicMorpho3dW(Output3dImageMixin, BasicMorphoW):
    model_class = BasicMorpho3dWM
    view_class = BasicMorpho3dWV

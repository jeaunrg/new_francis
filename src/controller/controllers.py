from abc import abstractmethod
from typing import Union

from PyQt5 import QtCore
from src.controller.mixin import Output2dImageMixin, Output3dImageMixin
from src.controller.utils import browse_path, raise_exception
from src.metadata.metadata import WidgetEnum
from src.model.models import (
    BasicMorphoWM,
    Load3dImageWM,
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


class LoadImageW(Output2dImageMixin, LoadFileW):
    model_class = LoadImageWM
    view_class = LoadImageWV


class Load3dImageW(Output3dImageMixin, LoadFileW):
    model_class = Load3dImageWM
    view_class = LoadImageWV


class LoadTextW(LoadFileW):
    model_class = LoadTextWM
    view_class = LoadTextWV

    def set_view_output(self, output: Union[str, Exception]):
        if isinstance(output, Exception):
            return raise_exception(output)
        self.view.text.setText(output)


class BasicMorphoW(Output3dImageMixin, Widget):
    model_class = BasicMorphoWM
    view_class = BasicMorphoWV

    def get_view_input(self) -> dict:
        return {
            "im": self.parent_list[0].get_view_output(),
            "operation": self.view.operations.checkedButton().text(),
            "size": self.view.size.value(),
            "is_round_shape": self.view.is_round_shape.isChecked(),
        }

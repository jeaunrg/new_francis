from abc import abstractmethod

from PyQt5 import QtCore
from src.controller.mixin import Output2dImageMixin, Output3dImageMixin
from src.metadata.func import raise_exception
from src.metadata.metadata import WidgetEnum
from src.model.models import (
    BasicMorpho2dWM,
    BasicMorpho3dWM,
    Load2dImageWM,
    Load3dImageWM,
    LoadFileWM,
    LoadTextWM,
    WidgetModel,
)
from src.view.items import GraphLinkItem, WidgetItem
from src.view.utils import browse_path
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
        for parent in parent_list:
            parent.child_list.append(self)
        self.child_list: list[Widget] = []
        self.link_list: list[GraphLink] = []
        self.model = self.model_class()
        self.view = self.view_class()
        self.item = WidgetItem(self.view, position)
        self.output = Exception("No output yet.")
        self.make_connections()

    def inherited_model_attr(self) -> dict:
        """model attributes which can be inherited from parent widget models"""
        inherited_attributes = {}
        for parent in self.parent_list:
            for k, v in parent.model.get_heritage().items():
                if v is not None and inherited_attributes.get(k) is None:
                    inherited_attributes[k] = v
        return inherited_attributes

    def make_connections(self):
        self.view.button.clicked.connect(lambda: self.submit())

    def submit(self):
        self.model.set_inherited_attr(**self.inherited_model_attr())
        view_input_dict = self.get_view_input()
        try:
            self.output = self.model.compute(**view_input_dict)
        except Exception as e:
            self.output = Exception("Wrong parent output.", e)
        self.set_view_output(self.output)

    @abstractmethod
    def get_view_input(self) -> dict:
        pass

    def get_view_output(self):
        return self.output

    @abstractmethod
    def set_view_output(self, output):
        pass

    def close(self):
        for child in self.child_list:
            child.close()
        for link in self.link_list:
            link.close()
        for parent in self.parent_list:
            if self in parent.child_list:
                parent.child_list.remove(self)
        self.item.scene().removeItem(self.item.view.graphicsProxyWidget())
        self.item.scene().removeItem(self.item)
        self.model.clean()


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


class LoadTextW(LoadFileW):
    model_class = LoadTextWM
    view_class = LoadTextWV

    def set_view_output(self, output: str or Exception):
        if isinstance(output, Exception):
            return raise_exception(output)
        self.view.text.setText(output)


class BasicMorphoW(Widget):
    view_class = BasicMorphoWV

    def get_view_input(self) -> dict:
        return {
            "arr": self.parent_list[0].get_view_output(),
            "operation": self.view.operations.checkedButton().text(),
            "size": self.view.size.value(),
            "is_round_shape": self.view.is_round_shape.isChecked(),
        }


class BasicMorpho2dW(Output2dImageMixin, BasicMorphoW):
    model_class = BasicMorpho2dWM
    view_class = BasicMorphoWV


class BasicMorpho3dW(Output3dImageMixin, BasicMorphoW):
    model_class = BasicMorpho3dWM
    view_class = BasicMorphoWV


class GraphLink:
    def __init__(self, parent: Widget, child: Widget):
        self.parent = parent
        self.child = child
        self.parent.link_list.append(self)
        self.child.link_list.append(self)
        self.item = GraphLinkItem()
        self.make_connections()

    def make_connections(self):
        self.parent.view.position_changed.connect(
            lambda: self.item.draw(self.parent.item, self.child.item)
        )
        self.child.view.position_changed.connect(
            lambda: self.item.draw(self.parent.item, self.child.item)
        )

    def close(self):
        self.item.scene().removeItem(self.item)
        self.parent.link_list.remove(self)
        self.child.link_list.remove(self)

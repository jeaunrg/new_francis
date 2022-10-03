from abc import abstractmethod

from PyQt5 import QtCore
from src.controller.mixin import Output2dImageMixin, Output3dImageMixin
from src.metadata.func import raise_exception
from src.metadata.metadata import WidgetEnum
from src.model import models as mo
from src.view import views as vu
from src.view.items import GraphLinkItem, WidgetItem
from src.view.utils import browse_path


class Widget:
    model_class = mo.WidgetModel
    view_class = vu.WidgetView

    def __init__(
        self, key: WidgetEnum, position: QtCore.QPointF, parent_list: list = []
    ):
        self.key = key
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
            self.output = Exception("Wrong parent output.", e, view_input_dict)
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
    model_class = mo.LoadFileWM
    view_class = vu.LoadFileWV
    extensions = []

    def make_connections(self):
        super().make_connections()
        self.view.browse.clicked.connect(lambda: self.set_browse_path())

    def set_browse_path(self):
        filename = browse_path(extensions=self.extensions)
        if filename != "":
            self.view.path.setText(filename)
            self.view.path.setToolTip(filename)

    def get_view_input(self) -> dict:
        return {"file_path": self.view.path.text()}


class Load2dImageW(Output2dImageMixin, LoadFileW):
    model_class = mo.Load2dImageWM
    view_class = vu.LoadImageWV
    extensions = ["png", "jpg", "jpeg", "PNG", "JPEG"]


class Load3dImageW(Output3dImageMixin, LoadFileW):
    model_class = mo.Load3dImageWM
    view_class = vu.LoadImageWV
    extensions = ["nii", "nii.gz"]


class LoadTextW(LoadFileW):
    model_class = mo.LoadTextWM
    view_class = vu.LoadTextWV
    extensions = ["txt"]

    def set_view_output(self, output: str or Exception):
        if isinstance(output, Exception):
            return raise_exception(output)
        self.view.text.setText(output)


class BasicMorphoW(Widget):
    view_class = vu.BasicMorphoWV

    def get_view_input(self) -> dict:
        return {
            "arr": self.parent_list[0].get_view_output(),
            "operation": self.view.operations.checkedButton().text(),
            "size": self.view.size.value(),
            "is_round_shape": self.view.is_round_shape.isChecked(),
        }


class BasicMorpho2dW(Output2dImageMixin, BasicMorphoW):
    model_class = mo.BasicMorpho2dWM
    view_class = vu.BasicMorphoWV


class BasicMorpho3dW(Output3dImageMixin, BasicMorphoW):
    model_class = mo.BasicMorpho3dWM
    view_class = vu.BasicMorphoWV


class AdvancedMorphoW(Widget):
    model_class = mo.AdvancedMorphoWM
    view_class = vu.AdvancedMorphoWV

    def get_view_input(self) -> dict:
        return {
            "arr": self.parent_list[0].get_view_output(),
            "operation": self.view.operations.checkedButton().text(),
        }


class AdvancedMorpho2dW(Output2dImageMixin, AdvancedMorphoW):
    pass


class AdvancedMorpho3dW(Output3dImageMixin, AdvancedMorphoW):
    pass


class FilterW(Widget):
    model_class = mo.FilterWM
    view_class = vu.FilterWV

    def get_view_input(self) -> dict:
        return {
            "arr": self.parent_list[0].get_view_output(),
            "operation": self.view.operations.checkedButton().text(),
        }


class Filter2dW(Output2dImageMixin, FilterW):
    pass


class Filter3dW(Output3dImageMixin, FilterW):
    pass


def widget_factory(
    widget_key: WidgetEnum, widget_position, parent_list: list[Widget]
) -> Widget:
    if widget_key == WidgetEnum.load_2d_im:
        return Load2dImageW(widget_key, widget_position)
    elif widget_key == WidgetEnum.load_3d_im:
        return Load3dImageW(widget_key, widget_position)
    elif widget_key == WidgetEnum.load_txt:
        return LoadTextW(widget_key, widget_position)
    elif widget_key == WidgetEnum.basic_morpho_2d:
        return BasicMorpho2dW(widget_key, widget_position, parent_list[:1])
    elif widget_key == WidgetEnum.basic_morpho_3d:
        return BasicMorpho3dW(widget_key, widget_position, parent_list[:1])
    elif widget_key == WidgetEnum.advanced_morpho_2d:
        return AdvancedMorpho2dW(widget_key, widget_position, parent_list[:1])
    elif widget_key == WidgetEnum.advanced_morpho_3d:
        return AdvancedMorpho3dW(widget_key, widget_position, parent_list[:1])
    elif widget_key == WidgetEnum.filter_2d:
        return Filter2dW(widget_key, widget_position, parent_list[:1])
    elif widget_key == WidgetEnum.filter_3d:
        return Filter2dW(widget_key, widget_position, parent_list[:1])
    else:
        raise Exception(
            f"Missing condition in widget_factory for widget_name={widget_key}"
        )


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

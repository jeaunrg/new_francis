from abc import abstractmethod

from PyQt5 import QtCore
from src.metadata.metadata import WidgetEnum
from src.model import models as mo
from src.view import views as vu
from src.view.items import GraphLinkItem, WidgetItem


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

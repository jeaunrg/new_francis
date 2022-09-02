from enum import Enum

from PyQt5 import QtWidgets
from src.controller.controllers import LoadImageWC, LoadTextWC
from src.model.main_model import MainModel
from src.view.main_view import GraphItem, GraphView, MainView


class WidgetEnum(Enum):
    load_im = "load_im"
    load_txt = "load_txt"


WIDGET_NAME_DICT = {
    "load:image": WidgetEnum.load_im,
    "load:text": WidgetEnum.load_txt,
}


def widget_controller_factory(widget_name: WidgetEnum):
    if widget_name == WidgetEnum.load_im:
        return LoadImageWC()
    if widget_name == WidgetEnum.load_txt:
        return LoadTextWC()


class MainController:
    def __init__(self):
        self.model = MainModel()
        self.view = MainView()
        self.make_connections()
        self.add_tab()

    def make_connections(self):
        self.view.centralWidget().tabCloseRequested.connect(
            lambda index: self.close_tab(index)
        )
        self.view.centralWidget().cornerWidget().clicked.connect(lambda: self.add_tab())

    def add_tab(self):
        graph_controller = GraphController()
        self.view.centralWidget().addTab(graph_controller.view, "Graph")

    def close_tab(self, index: int):
        reply = self.view.popup_dialog("close_scene")
        if reply == QtWidgets.QMessageBox.Yes:
            self.view.centralWidget().removeTab(index)


class GraphController:
    def __init__(self):
        self.view = GraphView()
        self.make_connections()
        self.widget_position = (0, 0)

    def set_widget_position(self, x, y):
        self.widget_position = (x, y)

    def make_connections(self):
        self.view.mouse_clicked.connect(lambda x, y: self.set_widget_position(x, y))
        self.view.menu.activated.connect(
            lambda activation_key: self.add_widget(WIDGET_NAME_DICT[activation_key])
        )

    def add_widget(self, widget_name: WidgetEnum):
        widget_controller = widget_controller_factory(widget_name)
        item = GraphItem(self.widget_position, widget_controller.view)
        self.view.scene().addItem(item)

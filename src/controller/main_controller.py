from enum import Enum

from PyQt5 import QtCore, QtWidgets
from src.controller.controllers import LoadImageWC, LoadTextWC, WidgetController
from src.model.main_model import MainModel
from src.view.main_view import GraphProxy, GraphView, MainView, Menu


class WidgetEnum(Enum):
    load_im = "load_im"
    load_txt = "load_txt"


WIDGET_NAME_DICT = {
    "load:image": WidgetEnum.load_im,
    "load:text": WidgetEnum.load_txt,
}
RIGHT_CLICK_MENU = {
    "scene": {"load": {"image": {}, "text": {}}},
    WidgetEnum.load_im: {"load:image": {}},
    WidgetEnum.load_txt: {"load:text": {}},
}


def widget_controller_factory(widget_name: WidgetEnum):
    if widget_name == WidgetEnum.load_im:
        return LoadImageWC(widget_name)
    if widget_name == WidgetEnum.load_txt:
        return LoadTextWC(widget_name)


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
        self.menu = Menu()
        self.focused_widget = None
        self.widget_position = QtCore.QPoint(0, 0)
        self.make_connections()

    def make_connections(self):
        self.view.right_clicked.connect(lambda x, y: self.open_menu(x, y))
        self.menu.activated.connect(
            lambda activation_key: self.add_widget(WIDGET_NAME_DICT[activation_key])
        )

    def open_menu(self, x, y):
        position = QtCore.QPoint(x, y)
        self.widget_position = self.view.mapToScene(self.view.mapFromGlobal(position))
        menu_key = "scene" if self.focused_widget is None else self.focused_widget.name
        self.menu.build(RIGHT_CLICK_MENU[menu_key])
        self.menu.exec(position)

    def set_focused_widget_cotroller(
        self, widget_controller: WidgetController, focused: bool
    ):
        if focused and self.focused_widget != widget_controller:
            self.focused_widget = widget_controller
        elif not focused and self.focused_widget == widget_controller:
            self.focused_widget = None

    def add_widget(self, widget_name: WidgetEnum):
        widget_controller = widget_controller_factory(widget_name)
        widget_controller.view.focused.connect(
            lambda focused: self.set_focused_widget_cotroller(
                widget_controller, focused
            )
        )
        proxy = GraphProxy(widget_controller.view, self.widget_position)
        self.view.scene().addItem(proxy.item)

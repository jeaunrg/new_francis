from PyQt5 import QtCore, QtWidgets
from src.controller.controllers import GraphLink, Widget, widget_factory
from src.metadata.config import MENU_DICT
from src.metadata.func import make_unique_string
from src.metadata.metadata import WidgetEnum
from src.model.main_model import MainModel
from src.view.main_view import GraphView, MainView, Menu


class MainController:
    def __init__(self, window_size: tuple = (400, 400)):
        self.model = MainModel()
        self.view = MainView(window_size)
        self.graph_controller_dict = {}
        self.make_connections()
        self.add_tab()

    def make_connections(self):
        self.view.centralWidget().tabCloseRequested.connect(
            lambda index: self.close_tab(index)
        )
        self.view.centralWidget().cornerWidget().clicked.connect(lambda: self.add_tab())
        self.view.closed.connect(lambda: self.save_settings())

    def add_tab(self):
        tab_name = make_unique_string("graph", self.graph_controller_dict.keys())
        graph_controller = GraphController()
        self.graph_controller_dict[tab_name] = graph_controller
        self.view.centralWidget().addTab(graph_controller.view, tab_name)

    def close_tab(self, index: int):
        reply = self.view.popup_dialog("close_scene")
        if reply == QtWidgets.QMessageBox.Yes:
            tab_name = self.view.centralWidget().tabText(index)
            print("close", tab_name)
            self.graph_controller_dict.pop(tab_name).close()
            self.view.centralWidget().removeTab(index)

    def save_settings(self):
        setting_dict = self.get_settings()

    def get_settings(self) -> dict:
        return {}


class GraphController:
    def __init__(self):
        self.view = GraphView()
        self.menu = Menu()
        self.focused_widget = None
        self.selected_widget_list: list[Widget] = []
        self.widget_dict = {}
        self.widget_position = QtCore.QPointF(0, 0)
        self.make_connections()

    def make_connections(self):
        self.view.right_clicked.connect(lambda position: self.open_menu(position))
        self.menu.closed.connect(lambda: self.close_selected_widgets())
        self.menu.activated.connect(lambda widget_key: self.add_widget(widget_key))

    def get_selected_widgets(self) -> list[Widget]:
        widget_list = [w for w in self.widget_dict.values() if w.view.is_selected()]
        if self.focused_widget is not None and self.focused_widget not in widget_list:
            widget_list.append(self.focused_widget)
        return widget_list

    def make_menu_hierarchy(self) -> dict:
        self.selected_widget_list = self.get_selected_widgets()
        if len(self.selected_widget_list) == 0:
            menu_key = "scene"
        elif len(self.selected_widget_list) == 1:
            menu_key = self.selected_widget_list[0].key
        else:
            raise ValueError("Condition not implemented")
        menu_hierarchy = MENU_DICT[menu_key]
        return menu_hierarchy

    def open_menu(self, menu_position: QtCore.QPoint):
        self.widget_position = self.view.mapToScene(
            self.view.mapFromGlobal(menu_position)
        )
        menu_hierarchy = self.make_menu_hierarchy()
        self.menu.build(menu_hierarchy)
        self.menu.exec(menu_position)

    def update_focused_widget(self, widget: Widget, focused: bool):
        if focused and self.focused_widget != widget:
            self.focused_widget = widget
        elif not focused and self.focused_widget == widget:
            self.focused_widget = None

    def add_widget(self, widget_key: WidgetEnum):
        widget = widget_factory(
            widget_key, self.widget_position, self.selected_widget_list
        )
        widget_name = make_unique_string("widget", self.widget_dict.keys())
        self.widget_dict[widget_name] = widget
        widget.view.focused.connect(
            lambda focused: self.update_focused_widget(widget, focused)
        )
        self.view.scene().addItem(widget.item)
        for parent_widget in widget.parent_list:
            link = GraphLink(parent_widget, widget)
            self.view.scene().addItem(link.item)

    def close_selected_widgets(self):
        for widget in self.selected_widget_list:
            reply = widget.view.popup_dialog("close_widget")
            if reply == QtWidgets.QMessageBox.Yes:
                widget.close()

    def close(self):
        widget_name_list = self.widget_dict.keys()
        for widget_name in widget_name_list:
            self.widget_dict.pop(widget_name).close()

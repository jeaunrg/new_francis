from PyQt5 import QtCore, QtWidgets
from src.controller.controllers import (
    BasicMorpho2dW,
    BasicMorpho3dW,
    Load2dImageW,
    Load3dImageW,
    LoadTextW,
    Widget,
    WidgetEnum,
)
from src.metadata.func import make_unique_string
from src.metadata.metadata import RIGHT_CLICK_MENU, WIDGET_KEY_DICT
from src.model.main_model import MainModel
from src.view.items import GraphLinkItem
from src.view.main_view import GraphView, MainView, Menu


def widget_factory(
    widget_key: WidgetEnum, widget_position, parent_list: list[Widget]
) -> Widget:
    if widget_key == WidgetEnum.load_im:
        return Load2dImageW(widget_key, widget_position)
    elif widget_key == WidgetEnum.load_3d_im:
        return Load3dImageW(widget_key, widget_position)
    elif widget_key == WidgetEnum.load_txt:
        return LoadTextW(widget_key, widget_position)
    elif widget_key == WidgetEnum.basic_morpho:
        return BasicMorpho2dW(widget_key, widget_position, parent_list[:1])
    elif widget_key == WidgetEnum.basic_morpho_3d:
        return BasicMorpho3dW(widget_key, widget_position, parent_list[:1])
    else:
        raise Exception(
            f"Missing condition in widget_factory for widget_name={widget_key}"
        )


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
        self.parent_widget_list = []
        self.widget_dict = {}
        self.widget_position = QtCore.QPointF(0, 0)
        self.make_connections()

    def make_connections(self):
        self.view.right_clicked.connect(lambda position: self.open_menu(position))
        self.menu.closed.connect(lambda: self.close_widget())
        self.menu.activated.connect(
            lambda activation_key: self.add_widget(WIDGET_KEY_DICT[activation_key])
        )

    def get_selected_widgets(self):
        widget_list = [w for w in self.widget_dict.values() if w.view.is_selected()]
        if self.focused_widget is not None and self.focused_widget not in widget_list:
            widget_list.append(self.focused_widget)
        return widget_list

    def open_menu(self, menu_position: QtCore.QPoint):
        self.parent_widget_list = self.get_selected_widgets()
        self.widget_position = self.view.mapToScene(
            self.view.mapFromGlobal(menu_position)
        )
        menu_key = "scene" if self.focused_widget is None else self.focused_widget.name
        self.menu.build(RIGHT_CLICK_MENU[menu_key])
        self.menu.exec(menu_position)

    def update_focused_widget(self, widget: Widget, focused: bool):
        if focused and self.focused_widget != widget:
            self.focused_widget = widget
        elif not focused and self.focused_widget == widget:
            self.focused_widget = None

    def add_widget(self, widget_key: WidgetEnum):
        widget = widget_factory(
            widget_key, self.widget_position, self.parent_widget_list
        )
        widget_name = make_unique_string("widget", self.widget_dict.keys())
        self.widget_dict[widget_name] = widget
        widget.view.focused.connect(
            lambda focused: self.update_focused_widget(widget, focused)
        )
        self.view.scene().addItem(widget.item)
        for parent_widget in widget.parent_list:
            link = GraphLinkController(parent_widget, widget)
            self.view.scene().addItem(link.item)

    def close_widget(self):
        for parent_widget in self.parent_widget_list:
            reply = parent_widget.view.popup_dialog("close_widget")
            if reply == QtWidgets.QMessageBox.Yes:
                parent_widget.close()

    def close(self):
        widget_name_list = self.widget_dict.keys()
        for widget_name in widget_name_list:
            print("close", widget_name)
            self.widget_dict.pop(widget_name).close()


class GraphLinkController:
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
        self.item.close()
        self.parent.link_list.remove(self)
        self.child.link_list.remove(self)

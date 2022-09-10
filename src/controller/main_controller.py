from PyQt5 import QtCore, QtWidgets
from src.controller.controllers import LoadImageW, LoadTextW, Widget, WidgetEnum
from src.model.main_model import MainModel
from src.view.items import GraphLinkItem
from src.view.main_view import GraphView, MainView, Menu

WIDGET_NAME_DICT = {
    "load:image": WidgetEnum.load_im,
    "load:text": WidgetEnum.load_txt,
}
RIGHT_CLICK_MENU = {
    "scene": {"load": {"image": {}, "text": {}}},
    WidgetEnum.load_im: {"load:image": {}},
    WidgetEnum.load_txt: {"load:text": {}},
}


def widget_factory(
    widget_name: WidgetEnum, widget_position, parent_list: list[Widget]
) -> Widget:
    if widget_name == WidgetEnum.load_im:
        return LoadImageW(widget_name, widget_position, parent_list)
    if widget_name == WidgetEnum.load_txt:
        return LoadTextW(widget_name, widget_position, parent_list)


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
        self.parent_widget_list = []
        self.widget_list = []
        self.widget_position = QtCore.QPointF(0, 0)
        self.make_connections()

    def make_connections(self):
        self.view.right_clicked.connect(lambda position: self.open_menu(position))
        self.menu.activated.connect(
            lambda activation_key: self.add_widget(WIDGET_NAME_DICT[activation_key])
        )

    def get_selected_widgets(self):
        widget_list = [w for w in self.widget_list if w.view.is_selected()]
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

    def add_widget(self, widget_name: WidgetEnum):
        widget = widget_factory(
            widget_name, self.widget_position, self.parent_widget_list
        )
        self.widget_list.append(widget)
        widget.view.focused.connect(
            lambda focused: self.update_focused_widget(widget, focused)
        )
        self.view.scene().addItem(widget.item)
        for parent_widget in widget.parent_list:
            link = GraphLinkController(parent_widget, widget)
            self.view.scene().addItem(link.item)


class GraphLinkController:
    def __init__(self, parent: Widget, child: Widget):
        self.parent = parent
        self.child = child
        self.item = GraphLinkItem()
        self.make_connections()

    def make_connections(self):
        self.parent.view.position_changed.connect(
            lambda: self.item.draw(self.parent.item, self.child.item)
        )
        self.child.view.position_changed.connect(
            lambda: self.item.draw(self.parent.item, self.child.item)
        )

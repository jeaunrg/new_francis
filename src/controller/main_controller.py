from enum import Enum

from src.controller.controllers import LoadImageWC, LoadTextWC
from src.model.main_model import MainModel
from src.view.main_view import GraphItem, GraphView, MainView


class WidgetEnum(Enum):
    load_im = "load_im"
    load_txt = "load_txt"


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
        self.add_widget(WidgetEnum.load_im)

    def make_connections(self):
        self.view.centralWidget().cornerWidget().clicked.connect(lambda: self.add_tab())

    def add_tab(self):
        graph_view = GraphView()
        self.view.centralWidget().addTab(graph_view, "Tab1")

    def add_widget(self, widget_name: WidgetEnum):
        widget_controller = widget_controller_factory(widget_name)
        item = GraphItem(widget_controller.view)
        current_graph = self.view.centralWidget().currentWidget()
        current_graph.scene().addItem(item)

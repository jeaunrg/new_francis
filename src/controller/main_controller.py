from enum import Enum

from src.controller.controllers import LoadImageWC
from src.model.main_model import MainModel
from src.view.main_view import MainView


class WidgetEnum(Enum):
    load = "load"


def widget_controller_factory(widget_name: WidgetEnum):
    if widget_name == WidgetEnum.load:
        return LoadImageWC()


class MainController:
    def __init__(self):
        self.model = MainModel()
        self.view = MainView()
        self.add_widget(WidgetEnum.load)

    def add_widget(self, widget_name: WidgetEnum):
        widget_controller = widget_controller_factory(widget_name)
        self.view.setCentralWidget(widget_controller.view)

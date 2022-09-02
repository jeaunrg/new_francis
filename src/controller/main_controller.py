from enum import Enum

from src.controller.controllers import LoadImageWC, LoadTextWC
from src.model.main_model import MainModel
from src.view.main_view import MainView


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
        self.add_widget(WidgetEnum.load_im)
        self.add_widget(WidgetEnum.load_txt)

    def add_widget(self, widget_name: WidgetEnum):
        widget_controller = widget_controller_factory(widget_name)
        self.view.layout.addWidget(widget_controller.view)

from enum import Enum

from PyQt5.QtWidgets import QMessageBox
from skimage import morphology


class WidgetEnum(str, Enum):
    load_im = "load_im"
    load_3d_im = "load_3d_im"
    load_txt = "load_txt"
    basic_morpho = "basic_morpho"
    basic_morpho_3d = "basic_morpho_3d"


DATA_DIR = "data/"

OPERATION_DICT = {
    "morpho:basic": {
        "erosion": morphology.erosion,
        "dilation": morphology.dilation,
        "binary_erosion": morphology.binary_erosion,
        "binary_dilation": morphology.binary_dilation,
        "opening": morphology.opening,
        "closing": morphology.closing,
    }
}

WIDGET_NAME_DICT = {
    "load:image": WidgetEnum.load_im,
    "load:3dimage": WidgetEnum.load_3d_im,
    "load:text": WidgetEnum.load_txt,
    "morpho:basic": WidgetEnum.basic_morpho,
    "morpho3d:basic": WidgetEnum.basic_morpho_3d,
}

RIGHT_CLICK_MENU = {
    "scene": {"load": {"image": {}, "3dimage": {}, "text": {}}},
    WidgetEnum.load_im: {"morpho:basic": {}},
    WidgetEnum.load_3d_im: {"morpho3d:basic": {}},
    WidgetEnum.load_txt: {},
    WidgetEnum.basic_morpho: {"morpho:basic": {}},
    WidgetEnum.basic_morpho_3d: {"morpho3d:basic": {}},
}

POPUPS = {
    "close_scene": (
        "Are you sure to close this scene ?",
        QMessageBox.Yes | QMessageBox.No,
    ),
    "close_widget": (
        "Are you sure to close this widget ?",
        QMessageBox.Yes | QMessageBox.No,
    ),
}

from enum import Enum

from PyQt5.QtWidgets import QMessageBox
from skimage import morphology


class WidgetEnum(str, Enum):
    load_2d_im = "load_im"
    load_3d_im = "load_3d_im"
    load_txt = "load_txt"
    basic_morpho_2d = "basic_morpho_2d"
    basic_morpho_3d = "basic_morpho_3d"
    advanced_morpho_2d = "advanced_morpho_2d"
    advanced_morpho_3d = "advanced_morpho_3d"


DATA_DIR = "data/"

OPERATION_DICT = {
    "morpho:basic": {
        "erosion": morphology.erosion,
        "dilation": morphology.dilation,
        "binary_erosion": morphology.binary_erosion,
        "binary_dilation": morphology.binary_dilation,
        "opening": morphology.opening,
        "closing": morphology.closing,
    },
    "morpho:advanced": {
        "black_tophat": morphology.black_tophat,
        "white_tophat": morphology.white_tophat,
        "convex_hull": morphology.convex_hull_image,
        # "flood_fill": morphology.flood_fill,
        # "h_maxima": morphology.h_maxima,
        # "h_minima": morphology.h_minima,
        # "local_maxima": morphology.local_maxima,
        # "local_minima": morphology.local_minima,
        "skeletonize": morphology.skeletonize_3d,
        "thinning": morphology.thin,
    },
}

WIDGET_KEY_DICT = {
    "load:image": WidgetEnum.load_2d_im,
    "load:3dimage": WidgetEnum.load_3d_im,
    "load:text": WidgetEnum.load_txt,
    "morpho2d:basic": WidgetEnum.basic_morpho_2d,
    "morpho3d:basic": WidgetEnum.basic_morpho_3d,
    "morpho2d:advanced": WidgetEnum.advanced_morpho_2d,
    "morpho3d:advanced": WidgetEnum.advanced_morpho_3d,
}

_MORPHO_MENU = {"basic": {}, "advanced": {}}
_2D_MENU = {"morpho2d": _MORPHO_MENU}
_3D_MENU = {"morpho2d": _MORPHO_MENU}

RIGHT_CLICK_MENU = {
    "scene": {"load": {"image": {}, "3dimage": {}, "text": {}}},
    WidgetEnum.load_2d_im: _2D_MENU,
    WidgetEnum.load_3d_im: _3D_MENU,
    WidgetEnum.load_txt: {},
    WidgetEnum.basic_morpho_2d: _2D_MENU,
    WidgetEnum.basic_morpho_3d: _3D_MENU,
    WidgetEnum.advanced_morpho_2d: _2D_MENU,
    WidgetEnum.advanced_morpho_3d: _3D_MENU,
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

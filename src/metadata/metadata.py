from enum import Enum

from skimage import morphology


class WidgetEnum(str, Enum):
    load_im = "load_im"
    load_txt = "load_txt"
    basic_morpho = "basic_morpho"


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
    "load:text": WidgetEnum.load_txt,
    "morpho:basic": WidgetEnum.basic_morpho,
}
RIGHT_CLICK_MENU = {
    "scene": {"load": {"image": {}, "text": {}}},
    WidgetEnum.load_im: {"morpho:basic": {}},
    WidgetEnum.load_txt: {},
}

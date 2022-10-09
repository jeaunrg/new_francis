from src.metadata.metadata import WidgetEnum

MENU_2D = {
    "morpho": {
        "basic": [WidgetEnum.basic_morpho_2d],
        "advanced": [WidgetEnum.advanced_morpho_2d],
    },
    "filter": [WidgetEnum.filter_2d],
    "threshold": [WidgetEnum.threshold_2d],
}
MENU_3D = {
    "morpho": {
        "basic": [WidgetEnum.basic_morpho_3d],
        "advanced": [WidgetEnum.advanced_morpho_3d],
    },
    "filter": [WidgetEnum.filter_3d],
    "threshold": [WidgetEnum.threshold_3d],
}
MENU_DICT = {
    "scene": {
        "load": [WidgetEnum.load_2d_im, WidgetEnum.load_3d_im, WidgetEnum.load_txt]
    },
    WidgetEnum.load_2d_im: MENU_2D,
    WidgetEnum.load_3d_im: MENU_3D,
    WidgetEnum.load_txt: {},
    WidgetEnum.basic_morpho_2d: MENU_2D,
    WidgetEnum.basic_morpho_3d: MENU_3D,
    WidgetEnum.advanced_morpho_2d: MENU_2D,
    WidgetEnum.advanced_morpho_3d: MENU_3D,
    WidgetEnum.threshold_2d: MENU_2D,
    WidgetEnum.threshold_3d: MENU_3D,
}

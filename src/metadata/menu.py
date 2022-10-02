from src.metadata.metadata import WidgetEnum

_2D_MENU = {
    "morpho2d": {
        "basic": WidgetEnum.basic_morpho_2d,
        "advanced": WidgetEnum.advanced_morpho_2d,
    }
}
_3D_MENU = {
    "morpho3d": {
        "basic": WidgetEnum.basic_morpho_3d,
        "advanced": WidgetEnum.advanced_morpho_3d,
    }
}
MENU_DICT = {
    "scene": {
        "load": {
            "image": WidgetEnum.load_2d_im,
            "3dimage": WidgetEnum.load_3d_im,
            "text": WidgetEnum.load_txt,
        }
    },
    WidgetEnum.load_2d_im: _2D_MENU,
    WidgetEnum.load_3d_im: _3D_MENU,
    WidgetEnum.load_txt: {},
    WidgetEnum.basic_morpho_2d: _2D_MENU,
    WidgetEnum.basic_morpho_3d: _3D_MENU,
    WidgetEnum.advanced_morpho_2d: _2D_MENU,
    WidgetEnum.advanced_morpho_3d: _3D_MENU,
}

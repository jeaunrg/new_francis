from enum import Enum
from pathlib import Path

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


DATA_DIR = Path(__file__).parent.parent.parent / "data"

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
        "skeletonize": morphology.skeletonize_3d,
        "thinning": morphology.thin,
    },
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

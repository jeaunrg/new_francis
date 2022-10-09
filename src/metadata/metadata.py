from enum import Enum
from pathlib import Path

from PyQt5.QtWidgets import QMessageBox
from skimage import filters, morphology


class WidgetEnum(str, Enum):
    load_2d_im = "load 2d image"
    load_3d_im = "load 3d image"
    load_txt = "load text"
    basic_morpho_2d = "basic morpho 2d"
    basic_morpho_3d = "basic morpho 3d"
    advanced_morpho_2d = "advanced morpho 2d"
    advanced_morpho_3d = "advanced morpho 3d"
    filter_2d = "filter 2d"
    filter_3d = "filter 3d"
    threshold_2d = "threshold 2d"
    threshold_3d = "threshold 3d"


DATA_DIR = Path(__file__).parent.parent.parent / "data"

OPERATION_DICT = {
    "morpho:basic": {
        "erosion": morphology.erosion,
        "dilation": morphology.dilation,
        "binary erosion": morphology.binary_erosion,
        "binary dilation": morphology.binary_dilation,
        "opening": morphology.opening,
        "closing": morphology.closing,
    },
    "morpho:advanced": {
        "black tophat": morphology.black_tophat,
        "white tophat": morphology.white_tophat,
        "convex hull": morphology.convex_hull_image,
        "skeletonize": morphology.skeletonize_3d,
        "thinning": morphology.thin,
    },
    "filter": {
        "sauvola threshold": filters.threshold_sauvola,
    },
    "threshold": {"multiotsu": filters.threshold_multiotsu},
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

from typing import Union

import numpy as np
from PyQt5 import QtGui, QtWidgets
from src.metadata.metadata import DATA_DIR


def _get_arr_infos(
    arr: np.ndarray,
) -> Union[int or None, QtGui.QImage.Format or None]:
    bytes_per_line, im_format = None, None
    if arr.ndim == 2:
        bytes_per_line = arr.shape[1]
        if arr.dtype == np.uint8:
            im_format = QtGui.QImage.Format_Grayscale8
    elif arr.ndim == 3:
        bytes_per_line = arr.shape[1] * arr.shape[2]
        if arr.dtype == np.uint8:
            if arr.shape[2] == 3:
                im_format = QtGui.QImage.Format_RGB888
            elif arr.shape[2] == 4:
                im_format = QtGui.QImage.Format_RGBA8888
    return bytes_per_line, im_format


def make_qimage(arr: np.ndarray) -> QtGui.QImage or None:
    bytes_per_line, im_format = _get_arr_infos(arr)
    if bytes_per_line is None or im_format is None:
        return None
    qimage = QtGui.QImage(
        arr.tobytes(),
        arr.shape[1],
        arr.shape[0],
        bytes_per_line,
        im_format,
    )
    return qimage


def browse_path(parent: QtWidgets.QWidget or None = None) -> str:
    """
    open a browse window to select a file and update path widget
    """
    dialog = QtWidgets.QFileDialog()
    filename, ok = dialog.getOpenFileName(
        parent,
        "Select a file...",
        DATA_DIR,
        filter="*.nii.gz *.nii *.png *.jpg *.txt *.pkl",
    )
    if not ok:
        filename = ""
    return filename

import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from src.metadata.func import raise_exception
from src.view.utils import make_qimage


class QRadioButtonGroup(QtWidgets.QButtonGroup):
    def __init__(self, button_name_list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.buttons = [
            QtWidgets.QRadioButton(button_name) for button_name in button_name_list
        ]
        self.buttons[0].setChecked(True)
        for button in self.buttons:
            self.addButton(button)


class QInteractiveImage(QtWidgets.QLabel):
    double_clicked = QtCore.pyqtSignal()
    scrolled = QtCore.pyqtSignal(int)

    def set_array(self, arr: np.ndarray):
        qimage = make_qimage(arr)
        if qimage is None:
            message = f"Image format not known. Shape={arr.shape}, dtype={arr.dtype}, max={arr.max()}, min={arr.min()}"
            return raise_exception(Exception(message))
        pixmap = QtGui.QPixmap(qimage)
        pixmap = pixmap.scaledToWidth(300, QtCore.Qt.FastTransformation)
        self.setPixmap(pixmap)

    def mouseDoubleClickEvent(self, event):
        self.double_clicked.emit()
        return super().mouseDoubleClickEvent(event)

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            self.scrolled.emit(-1)
        else:
            self.scrolled.emit(1)
        return super().wheelEvent(event)

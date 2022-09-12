from abc import abstractmethod

from PyQt5 import QtCore, QtWidgets
from src.metadata.metadata import OPERATION_DICT
from src.view.utils import QRadioButtonGroup


class WidgetView(QtWidgets.QWidget):
    submit_text = "Validate"
    focused = QtCore.pyqtSignal(bool)
    position_changed = QtCore.pyqtSignal()

    def __init__(self):
        super(WidgetView, self).__init__()
        self.message = QtWidgets.QLabel("")
        self.button = QtWidgets.QPushButton(self.submit_text)
        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.addWidget(self.make_grid_widget())
        mainLayout.addWidget(self.message)
        mainLayout.addWidget(self.button)
        self.setLayout(mainLayout)

    def make_grid_widget(self):
        self.make_widgets()
        grid_dict = self.make_grid_dict()
        grid_layout = QtWidgets.QGridLayout()
        for widget, grid_anchor in grid_dict.items():
            grid_layout.addWidget(widget, *grid_anchor)
        grid_widget = QtWidgets.QWidget()
        grid_widget.setLayout(grid_layout)
        return grid_widget

    def is_selected(self):
        return True

    def enterEvent(self, event):
        self.focused.emit(True)
        return super().enterEvent(event)

    def leaveEvent(self, event):
        self.focused.emit(False)
        return super().leaveEvent(event)

    @abstractmethod
    def make_widgets(self):
        """declare all displayed widgets"""
        pass

    @abstractmethod
    def make_grid_dict(self) -> dict[QtWidgets.QWidget, list[int]]:
        """arrange declared widgets in grid layout

        Return
        ------
        grid_dict = {
            widget1: [row, column, row_span, column_span],
            widget2: [row, column],
            ...
        }
        """
        pass


class LoadFileWV(WidgetView):
    submit_text = "Load"

    def make_widgets(self):
        self.path = QtWidgets.QLineEdit()
        self.browse = QtWidgets.QPushButton("...")

    def make_grid_dict(self) -> dict[QtWidgets.QWidget, list[int]]:
        return {self.path: [0, 0], self.browse: [0, 1]}


class LoadImageWV(LoadFileWV):
    def make_widgets(self):
        super().make_widgets()
        self.image = QtWidgets.QLabel()

    def make_grid_dict(self) -> dict[QtWidgets.QWidget, list[int]]:
        grid_dict = super().make_grid_dict()
        grid_dict[self.image] = [1, 0, 1, 2]
        return grid_dict


class LoadTextWV(LoadFileWV):
    def make_widgets(self):
        super().make_widgets()
        self.text = QtWidgets.QTextEdit()

    def make_grid_dict(self) -> dict[QtWidgets.QWidget, list[int]]:
        grid_dict = super().make_grid_dict()
        grid_dict[self.text] = [1, 0, 1, 2]
        return grid_dict


class BasicMorphoWV(WidgetView):
    submit_text = "apply"

    def make_widgets(self):
        self.operations = QRadioButtonGroup(OPERATION_DICT["morpho:basic"].keys())
        self.size = QtWidgets.QSpinBox()
        self.is_round_shape = QtWidgets.QCheckBox("round shape")
        self.image = QtWidgets.QLabel()

    def make_grid_dict(self) -> dict[QtWidgets.QWidget, list[int]]:
        grid_dict = {}
        for i, button in enumerate(self.operations.buttons):
            if i < 3:
                grid_dict[button] = [0, i]
            else:
                grid_dict[button] = [1, i - 3]
        grid_dict[self.size] = [2, 0]
        grid_dict[self.is_round_shape] = [2, 1]
        grid_dict[self.image] = [3, 0, 1, 3]
        return grid_dict

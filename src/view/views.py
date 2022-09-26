from abc import abstractmethod

import numpy as np
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from src.metadata.metadata import OPERATION_DICT, POPUPS
from src.view.custom_widgets import QInteractiveImage, QRadioButtonGroup
from src.view.utils import parse_str_to_array


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
        grid_matrix, grid_args = self.make_grid_matrix()
        grid_dict = self.matrix_to_grid_dict(grid_matrix, grid_args)
        grid_layout = QtWidgets.QGridLayout()
        for widget, grid_anchor in grid_dict.items():
            grid_layout.addWidget(widget, *grid_anchor)
        grid_widget = QtWidgets.QWidget()
        grid_widget.setLayout(grid_layout)
        return grid_widget

    def is_selected(self):
        return False

    def enterEvent(self, event):
        self.focused.emit(True)
        return super().enterEvent(event)

    def leaveEvent(self, event):
        self.focused.emit(False)
        return super().leaveEvent(event)

    def popup_dialog(self, popup_key: str):
        question, responses = POPUPS[popup_key]
        return QMessageBox.question(self, "", question, responses)

    @staticmethod
    def matrix_to_grid_dict(matrix, args):
        arr = parse_str_to_array(matrix)
        grid_dict = {}
        for value in np.unique(arr):
            if value == 0:
                continue
            line, column = np.where(arr == value)
            grid_dict[args[value]] = [
                line.min(),
                column.min(),
                line.max() - line.min() + 1,
                column.max() - column.min() + 1,
            ]
        return grid_dict

    @abstractmethod
    def make_widgets(self):
        """declare all displayed widgets"""
        pass

    @abstractmethod
    def make_grid_matrix(self) -> tuple[str, dict]:
        """declare matrix and args"""
        pass


class LoadFileWV(WidgetView):
    submit_text = "Load"

    def make_widgets(self):
        self.path = QtWidgets.QLineEdit()
        self.browse = QtWidgets.QPushButton("...")

    def make_grid_matrix(self):
        grid_matrix = """
        1 2 
        """
        return grid_matrix, {1: self.path, 2: self.browse}


class LoadImageWV(LoadFileWV):
    def make_widgets(self):
        super().make_widgets()
        self.image = QInteractiveImage()

    def make_grid_matrix(self):
        grid_matrix = """
        1 2
        3 3 
        """
        return grid_matrix, {1: self.path, 2: self.browse, 3: self.image}


class LoadTextWV(LoadFileWV):
    def make_widgets(self):
        super().make_widgets()
        self.text = QtWidgets.QTextEdit()

    def make_grid_matrix(self):
        grid_matrix = """
        1 2 
        3 3
        """
        return grid_matrix, {1: self.path, 2: self.browse, 3: self.text}


class BasicMorphoWV(WidgetView):
    submit_text = "apply"

    def make_widgets(self):
        self.operations = QRadioButtonGroup(OPERATION_DICT["morpho:basic"].keys())
        self.size = QtWidgets.QSpinBox()
        self.is_round_shape = QtWidgets.QCheckBox("round shape")
        self.image = QInteractiveImage()

    def make_grid_matrix(self):
        grid_matrix = """
        1 2 3
        4 5 6
        7 8
        9 9 9
        """
        args = {i + 1: self.operations.buttons[i] for i in range(6)}
        args.update({7: self.size, 8: self.is_round_shape, 9: self.image})
        return grid_matrix, args


class AdvancedMorphoWV(WidgetView):
    submit_text = "apply"

    def make_widgets(self):
        self.operations = QRadioButtonGroup(OPERATION_DICT["morpho:advanced"].keys())
        self.image = QInteractiveImage()

    def make_grid_matrix(self):
        grid_matrix = """
        1 2 3  
        4 5
        6 6 6
        """
        args = {i + 1: self.operations.buttons[i] for i in range(5)}
        args.update({6: self.image})
        return grid_matrix, args

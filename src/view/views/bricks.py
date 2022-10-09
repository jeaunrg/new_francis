from PyQt5 import QtWidgets
from src.metadata.metadata import OPERATION_DICT
from src.view.misc.qwidgets import QInteractiveImage, QRadioButtonGroup
from src.view.views.base import WidgetView


class LoadFileWV(WidgetView):
    submit_text = "Load"

    def make_widgets(self):
        self.path = QtWidgets.QLineEdit()
        self.browse = QtWidgets.QPushButton("...")

    def make_grid_matrix(self):
        grid_matrix = """
        1 2 
        """
        args = {1: self.path, 2: self.browse}
        return grid_matrix, args


class LoadImageWV(LoadFileWV):
    def make_widgets(self):
        super().make_widgets()
        self.image = QInteractiveImage()

    def make_grid_matrix(self):
        grid_matrix = """
        1 2
        3 3 
        """
        args = {1: self.path, 2: self.browse, 3: self.image}
        return grid_matrix, args


class LoadTextWV(LoadFileWV):
    def make_widgets(self):
        super().make_widgets()
        self.text = QtWidgets.QTextEdit()

    def make_grid_matrix(self):
        grid_matrix = """
        1 2 
        3 3
        """
        args = {1: self.path, 2: self.browse, 3: self.text}
        return grid_matrix, args


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


class FilterWV(WidgetView):
    submit_text = "apply"

    def make_widgets(self):
        self.operations = QRadioButtonGroup(OPERATION_DICT["filter"].keys())
        self.image = QInteractiveImage()

    def make_grid_matrix(self):
        grid_matrix = """
        1 
        3 3
        """
        args = {i + 1: self.operations.buttons[i] for i in range(1)}
        args.update({3: self.image})
        return grid_matrix, args


class ThresholdWV(WidgetView):
    submit_text = "apply"

    def make_widgets(self):
        self.operations = QRadioButtonGroup(OPERATION_DICT["threshold"].keys())
        self.label = QtWidgets.QLabel()

    def make_grid_matrix(self):
        grid_matrix = """
        1 1
        2 3
        """
        args = {i + 1: self.operations.buttons[i] for i in range(1)}
        args.update({2: QtWidgets.QLabel("Thresholds: "), 3: self.label})
        return grid_matrix, args

from abc import abstractmethod

from PyQt5 import QtCore, QtWidgets
from src.metadata.metadata import OPERATION_DICT


class WidgetView(QtWidgets.QWidget):
    submit_text = "Validate"
    focused = QtCore.pyqtSignal(bool)
    position_changed = QtCore.pyqtSignal()

    def __init__(self):
        super(WidgetView, self).__init__()
        content_widget = self.make_content()
        self.message = QtWidgets.QLabel("")
        self.button = QtWidgets.QPushButton(self.submit_text)
        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.addWidget(content_widget)
        mainLayout.addWidget(self.message)
        mainLayout.addWidget(self.button)
        self.setLayout(mainLayout)

    def is_selected(self):
        return True

    def enterEvent(self, event):
        self.focused.emit(True)
        return super().enterEvent(event)

    def leaveEvent(self, event):
        self.focused.emit(False)
        return super().leaveEvent(event)

    @abstractmethod
    def make_content(self) -> QtWidgets.QWidget:
        pass


class LoadFileWV(WidgetView):
    submit_text = "Load"

    def make_content(self):
        self.path = QtWidgets.QLineEdit()
        self.browse = QtWidgets.QPushButton("...")
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.path)
        layout.addWidget(self.browse)
        content_widget = QtWidgets.QWidget()
        content_widget.setLayout(layout)
        return content_widget


class LoadImageWV(LoadFileWV):
    def make_content(self):
        content_widget = super().make_content()
        self.image = QtWidgets.QLabel()
        content_widget.layout().addWidget(self.image)
        return content_widget


class LoadTextWV(LoadFileWV):
    def make_content(self):
        content_widget = super().make_content()
        self.text = QtWidgets.QTextEdit()
        content_widget.layout().addWidget(self.text)
        return content_widget


class BasicMorphoWV(WidgetView):
    submit_text = "apply"

    def make_content(self):
        layout = QtWidgets.QVBoxLayout()
        self.operations = QtWidgets.QButtonGroup()
        for operation_name in OPERATION_DICT["morpho:basic"].keys():
            operation_button = QtWidgets.QRadioButton(operation_name)
            layout.addWidget(operation_button)
            self.operations.addButton(operation_button)
        self.size = QtWidgets.QSpinBox()
        self.is_round_shape = QtWidgets.QCheckBox("round shape")
        self.image = QtWidgets.QLabel()
        layout.addWidget(self.size)
        layout.addWidget(self.is_round_shape)
        layout.addWidget(self.image)
        content_widget = QtWidgets.QWidget()
        content_widget.setLayout(layout)
        return content_widget

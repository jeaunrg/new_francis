from abc import abstractmethod

from PyQt5 import QtWidgets


class BaseWidgetView(QtWidgets.QWidget):
    submit_text = "Validate"

    def __init__(self):
        super(BaseWidgetView, self).__init__()
        content_widget = self.make_content()
        self.message = QtWidgets.QLabel("")
        self.button = QtWidgets.QPushButton(self.submit_text)
        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.addWidget(content_widget)
        mainLayout.addWidget(self.message)
        mainLayout.addWidget(self.button)
        self.setLayout(mainLayout)

    @abstractmethod
    def make_content(self) -> QtWidgets.QWidget:
        pass


class LoadWidgetView(BaseWidgetView):
    submit_text = "Load"

    def make_content(self):
        self.path = QtWidgets.QLineEdit()
        self.browse = QtWidgets.QPushButton("...")
        self.image = QtWidgets.QLabel()
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.path)
        layout.addWidget(self.browse)
        content_widget = QtWidgets.QWidget()
        content_widget.setLayout(layout)
        return content_widget

import sys

from PyQt5 import QtWidgets

from src.controller.main import MainController


def main():
    """
    this function initialize the application and the MVP app design

    """
    app = QtWidgets.QApplication(sys.argv)
    controller = MainController(window_size=(800, 800))
    controller.view.show()

    app.exec()

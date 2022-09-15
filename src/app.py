import sys

from PyQt5 import QtWidgets

from src.controller import main_controller


def main():
    """
    this function initialize the application and the MVP app design

    """
    app = QtWidgets.QApplication(sys.argv)
    cont = main_controller.MainController(window_size=(800, 800))
    cont.view.show()

    app.exec()

from PyQt5 import QtCore, QtWidgets


class MainView(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowState(QtCore.Qt.WindowActive)
        self.setWindowTitle("NewFrancis")
        self.layout = QtWidgets.QVBoxLayout()
        central_widget = QtWidgets.QWidget()
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)

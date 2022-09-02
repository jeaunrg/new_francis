from PyQt5 import QtCore, QtWidgets


class MainView(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowState(QtCore.Qt.WindowActive)
        self.setWindowTitle("NewFrancis")
        tab_widget = QtWidgets.QTabWidget()
        new_tab_button = QtWidgets.QPushButton("+")
        tab_widget.setCornerWidget(new_tab_button)
        self.setCentralWidget(tab_widget)


class GraphView(QtWidgets.QGraphicsView):
    def __init__(self):
        super().__init__()
        scene = QtWidgets.QGraphicsScene()
        self.setScene(scene)


class ModuleView(QtWidgets.QGraphicsItem):
    def __init__(self):
        super().__init__()

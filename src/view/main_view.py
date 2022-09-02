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


class GraphItem(QtWidgets.QGraphicsRectItem):
    def __init__(self, widget):
        super().__init__(0, 0, 75, 40)
        proxy = QtWidgets.QGraphicsProxyWidget(self)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)
        self.setBrush(QtCore.Qt.lightGray)
        proxy.setWidget(widget)
        proxy.setPos(0, 15)
        proxy.setFlags(
            QtWidgets.QGraphicsItem.ItemIsMovable
            | QtWidgets.QGraphicsItem.ItemIsSelectable
        )

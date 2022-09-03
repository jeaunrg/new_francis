from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from src.view.views import WidgetView

POPUPS = {
    "close_scene": (
        "Are you sure to close this scene ?",
        QMessageBox.Yes | QMessageBox.No,
    )
}


class MainView(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowState(QtCore.Qt.WindowActive)
        self.setWindowTitle("NewFrancis")
        self.resize(400, 400)
        tab_widget = QtWidgets.QTabWidget()
        tab_widget.setTabsClosable(True)
        new_tab_button = QtWidgets.QPushButton("+")
        tab_widget.setCornerWidget(new_tab_button)
        self.setCentralWidget(tab_widget)

    def popup_dialog(self, popup_key: str):
        question, responses = POPUPS[popup_key]
        return QMessageBox.question(self, "", question, responses)


class GraphView(QtWidgets.QGraphicsView):
    right_clicked = QtCore.pyqtSignal(QtCore.QPoint)

    def __init__(self):
        super().__init__()
        scene = QtWidgets.QGraphicsScene()
        self.setScene(scene)

    def contextMenuEvent(self, event: QtGui.QContextMenuEvent):
        position = QtGui.QCursor.pos()
        self.right_clicked.emit(position)
        return super().contextMenuEvent(event)


class GraphProxy(QtWidgets.QGraphicsProxyWidget):
    def __init__(self, widget: WidgetView, position: QtCore.QPoint):
        self.item = QtWidgets.QGraphicsRectItem(0, 0, 75, 40)
        self.item.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)
        self.item.setBrush(QtCore.Qt.lightGray)
        self.item.moveBy(position.x(), position.y())
        super().__init__(self.item)
        self.setWidget(widget)
        self.setPos(0, 15)
        self.setFlags(
            QtWidgets.QGraphicsItem.ItemIsMovable
            | QtWidgets.QGraphicsItem.ItemIsSelectable
        )


class Menu(QtWidgets.QMenu):
    activated = QtCore.pyqtSignal(str)

    def __init__(self, menu_dict: dict = {}):
        super().__init__()
        self.build(menu_dict)

    def build(self, menu_dict: dict):
        self.clear()
        for key, values in menu_dict.items():
            self._build_recursively(self, key, values, key)

    def _build_recursively(
        self, menu: QtWidgets.QMenu, key: str, values: dict, activation_key: str
    ):
        if len(values) == 0:
            action = menu.addAction(key)
            action.triggered.connect(lambda: self.activated.emit(activation_key))
        else:
            submenu = menu.addMenu(key)
            for key, values in values.items():
                self._build_recursively(submenu, key, values, f"{activation_key}:{key}")

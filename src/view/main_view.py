from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox

RIGHT_CLICK_MENU = {"load": {"image": {}, "text": {}}}
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
    mouse_clicked = QtCore.pyqtSignal(int, int)

    def __init__(self):
        super().__init__()
        scene = QtWidgets.QGraphicsScene()
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorViewCenter)
        self.setViewportUpdateMode(QtWidgets.QGraphicsView.NoViewportUpdate)
        self.setScene(scene)
        self.menu = Menu(RIGHT_CLICK_MENU)

    def contextMenuEvent(self, event):
        menu_position = QtGui.QCursor.pos()
        mouse_position = self.mapToScene(self.mapFromGlobal(menu_position))
        self.mouse_clicked.emit(mouse_position.x(), mouse_position.y())
        self.menu.exec(menu_position)
        return super().contextMenuEvent(event)


class Menu(QtWidgets.QMenu):
    activated = QtCore.pyqtSignal(str)

    def __init__(self, menu_dict: dict):
        super().__init__()
        for key, values in menu_dict.items():
            self.recursive_fill_menu(self, key, values, key)

    def recursive_fill_menu(self, menu, key, values, activation_key):
        if len(values) == 0:
            action = menu.addAction(key)
            action.triggered.connect(lambda: self.activated.emit(activation_key))
        else:
            submenu = menu.addMenu(key)
            for key, values in values.items():
                self.recursive_fill_menu(
                    submenu, key, values, f"{activation_key}:{key}"
                )


class GraphItem(QtWidgets.QGraphicsRectItem):
    def __init__(self, position, widget):
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
        self.moveBy(*position)

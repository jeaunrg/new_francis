from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from src.metadata.metadata import POPUPS


class MainView(QtWidgets.QMainWindow):
    closed = QtCore.pyqtSignal()

    def __init__(self, window_size: tuple = (400, 400)):
        super().__init__()
        self.setWindowState(QtCore.Qt.WindowActive)
        self.setWindowTitle("NewFrancis")
        self.resize(*window_size)
        tab_widget = QtWidgets.QTabWidget()
        tab_widget.setTabsClosable(True)
        new_tab_button = QtWidgets.QPushButton("+")
        tab_widget.setCornerWidget(new_tab_button)
        self.setCentralWidget(tab_widget)
        self.restore_window_state()

    def popup_dialog(self, popup_key: str):
        question, responses = POPUPS[popup_key]
        return QMessageBox.question(self, "", question, responses)

    def closeEvent(self, event):
        self.save_window_state()
        self.closed.emit()
        return super().closeEvent(event)

    def save_window_state(self):
        settings = QtCore.QSettings("FrancisInc", "FrancisApp")
        settings.setValue("geometry", self.saveGeometry())
        settings.setValue("windowState", self.saveState())

    def restore_window_state(self):
        settings = QtCore.QSettings("FrancisInc", "FrancisApp")
        self.restoreGeometry(settings.value("geometry"))
        self.restoreState(settings.value("windowState"))


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


class Menu(QtWidgets.QMenu):
    activated = QtCore.pyqtSignal(str)
    closed = QtCore.pyqtSignal()

    def __init__(self, menu_dict: dict = {}):
        super().__init__()
        self.build(menu_dict)

    def build(self, menu_dict: dict):
        self.clear()
        for key, values in menu_dict.items():
            self._build_recursively(self, key, values, key)
        close_action = self.addAction("close")
        close_action.triggered.connect(lambda: self.closed.emit())

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

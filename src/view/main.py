from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from src.metadata.metadata import POPUPS, WidgetEnum


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
    activated = QtCore.pyqtSignal(WidgetEnum)
    closed = QtCore.pyqtSignal()

    def __init__(self, menu_dict: dict = {}):
        super().__init__()
        self.build(menu_dict)

    def build(self, menu_hierarchy: dict):
        self.clear()
        for label, submenu_hierarchy in menu_hierarchy.items():
            self._build_recursively(self, label, submenu_hierarchy)
        close_action = self.addAction("close")
        close_action.triggered.connect(lambda: self.closed.emit())

    def _add_action(self, menu: QtWidgets.QMenu, widget_key: WidgetEnum):
        action = menu.addAction(widget_key)
        action.triggered.connect(lambda: self.activated.emit(widget_key))

    def _build_recursively(
        self,
        menu: QtWidgets.QMenu,
        label: str,
        submenu_hierarchy: dict or list[WidgetEnum],
    ):
        submenu = menu.addMenu(label)
        if isinstance(submenu_hierarchy, dict):
            for label, submenu_hierarchy in submenu_hierarchy.items():
                self._build_recursively(submenu, label, submenu_hierarchy)
        elif isinstance(submenu_hierarchy, list):
            for widget_key in submenu_hierarchy:
                self._add_action(submenu, widget_key)

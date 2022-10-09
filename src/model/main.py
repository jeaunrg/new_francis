from PyQt5 import QtCore


class MainModel:
    def __init__(self, name: str = "FrancisApp"):
        self.name = name

    def save_settings(self, setting_dict):
        settings = QtCore.QSettings("FrancisInc", self.name)
        for k, v in setting_dict.items():
            settings.setValue(k, v)

    def get_settings(self):
        settings = QtCore.QSettings("FrancisInc", self.name)

from PyQt5 import QtWidgets


class QRadioButtonGroup(QtWidgets.QButtonGroup):
    def __init__(self, button_name_list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.buttons = [
            QtWidgets.QRadioButton(button_name) for button_name in button_name_list
        ]
        self.buttons[0].setChecked(True)
        for button in self.buttons:
            self.addButton(button)

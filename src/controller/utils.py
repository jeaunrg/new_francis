from PyQt5 import QtWidgets


def browse_path(parent=None, data_dir=None):
    """
    open a browse window to select a file and update path widget
    """
    dialog = QtWidgets.QFileDialog()
    filename, ok = dialog.getOpenFileName(
        parent,
        "Select a file...",
        data_dir,
        filter="*.nii.gz *.nii *.png *.jpg *.txt *.pkl",
    )
    if not ok:
        filename = ""
    return filename

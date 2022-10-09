from src.controller.controllers.base import Widget
from src.controller.controllers.mixin import Output2dImageMixin, Output3dImageMixin
from src.metadata.func import raise_exception
from src.metadata.metadata import WidgetEnum
from src.model import models as mo
from src.view import views as vu
from src.view.misc.func import browse_path


def widget_factory(
    widget_key: WidgetEnum, widget_position, parent_list: list[Widget]
) -> Widget:
    if widget_key == WidgetEnum.load_2d_im:
        return Load2dImageW(widget_key, widget_position)
    elif widget_key == WidgetEnum.load_3d_im:
        return Load3dImageW(widget_key, widget_position)
    elif widget_key == WidgetEnum.load_txt:
        return LoadTextW(widget_key, widget_position)
    elif widget_key == WidgetEnum.basic_morpho_2d:
        return BasicMorpho2dW(widget_key, widget_position, parent_list[:1])
    elif widget_key == WidgetEnum.basic_morpho_3d:
        return BasicMorpho3dW(widget_key, widget_position, parent_list[:1])
    elif widget_key == WidgetEnum.advanced_morpho_2d:
        return AdvancedMorpho2dW(widget_key, widget_position, parent_list[:1])
    elif widget_key == WidgetEnum.advanced_morpho_3d:
        return AdvancedMorpho3dW(widget_key, widget_position, parent_list[:1])
    elif widget_key == WidgetEnum.filter_2d:
        return Filter2dW(widget_key, widget_position, parent_list[:1])
    elif widget_key == WidgetEnum.filter_3d:
        return Filter2dW(widget_key, widget_position, parent_list[:1])
    elif widget_key == WidgetEnum.threshold_2d:
        return Threshold2dW(widget_key, widget_position, parent_list[:1])
    elif widget_key == WidgetEnum.threshold_3d:
        return Threshold3dW(widget_key, widget_position, parent_list[:1])
    else:
        raise Exception(
            f"Missing condition in widget_factory for widget_name={widget_key}"
        )


class LoadFileW(Widget):
    model_class = mo.LoadFileWM
    view_class = vu.LoadFileWV
    extensions = []

    def make_connections(self):
        super().make_connections()
        self.view.browse.clicked.connect(lambda: self.set_browse_path())

    def set_browse_path(self):
        filename = browse_path(extensions=self.extensions)
        if filename != "":
            self.view.path.setText(filename)
            self.view.path.setToolTip(filename)

    def get_view_input(self) -> dict:
        return {"file_path": self.view.path.text()}


class Load2dImageW(Output2dImageMixin, LoadFileW):
    model_class = mo.Load2dImageWM
    view_class = vu.LoadImageWV
    extensions = ["png", "jpg", "jpeg", "PNG", "JPEG"]


class Load3dImageW(Output3dImageMixin, LoadFileW):
    model_class = mo.Load3dImageWM
    view_class = vu.LoadImageWV
    extensions = ["nii", "nii.gz"]


class LoadTextW(LoadFileW):
    model_class = mo.LoadTextWM
    view_class = vu.LoadTextWV
    extensions = ["txt"]

    def set_view_output(self, model_output: str or Exception):
        if isinstance(model_output, Exception):
            return raise_exception(model_output)
        self.view.text.setText(model_output)


class BasicMorphoW(Widget):
    view_class = vu.BasicMorphoWV

    def get_view_input(self) -> dict:
        return {
            "arr": self.parent_list[0].get_view_output(),
            "operation": self.view.operations.checkedButton().text(),
            "size": self.view.size.value(),
            "is_round_shape": self.view.is_round_shape.isChecked(),
        }


class BasicMorpho2dW(Output2dImageMixin, BasicMorphoW):
    model_class = mo.BasicMorpho2dWM
    view_class = vu.BasicMorphoWV


class BasicMorpho3dW(Output3dImageMixin, BasicMorphoW):
    model_class = mo.BasicMorpho3dWM
    view_class = vu.BasicMorphoWV


class AdvancedMorphoW(Widget):
    model_class = mo.AdvancedMorphoWM
    view_class = vu.AdvancedMorphoWV

    def get_view_input(self) -> dict:
        return {
            "arr": self.parent_list[0].get_view_output(),
            "operation": self.view.operations.checkedButton().text(),
        }


class AdvancedMorpho2dW(Output2dImageMixin, AdvancedMorphoW):
    pass


class AdvancedMorpho3dW(Output3dImageMixin, AdvancedMorphoW):
    pass


class FilterW(Widget):
    model_class = mo.FilterWM
    view_class = vu.FilterWV

    def get_view_input(self) -> dict:
        return {
            "arr": self.parent_list[0].get_view_output(),
            "operation": self.view.operations.checkedButton().text(),
        }


class Filter2dW(Output2dImageMixin, FilterW):
    pass


class Filter3dW(Output3dImageMixin, FilterW):
    pass


class ThresholdW(Widget):
    model_class = mo.ThresholdWM
    view_class = vu.ThresholdWV

    def get_view_input(self) -> dict:
        return {
            "arr": self.parent_list[0].get_view_output(),
            "operation": self.view.operations.checkedButton().text(),
        }

    def set_view_output(self, model_output: list or Exception):
        if isinstance(model_output, Exception):
            return raise_exception(model_output)
        model_output = [str(n) for n in model_output]
        self.view.label.setText(", ".join(model_output))


class Threshold2dW(ThresholdW):
    pass


class Threshold3dW(ThresholdW):
    pass

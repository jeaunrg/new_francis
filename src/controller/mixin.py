from typing import Union

import numpy as np
from src.metadata.func import raise_exception


class Output2dImageMixin:
    def submit(self):
        if len(self.parent_list) == 0:
            # reset block_size to 0 for primary widgets
            self.model.block_size = None
        super().submit()

    def get_view_output(self):
        if self.model.has_downsized_output:
            return self.model.get_raw_array()
        return self.output

    def set_view_output(self, output: np.ndarray or Exception):
        if isinstance(output, Exception):
            return raise_exception(output)
        self.view.image.set_array(output)


class Output3dImageMixin(Output2dImageMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.viewpoint = 0
        self.sections = [0, 0, 0]

    def _get_related_widgets(self, widget, widget_list: list = []):
        for w in widget.parent_list + widget.child_list:
            if w != self and w not in widget_list:
                widget_list.append(w)
                widget_list = self._get_related_widgets(w, widget_list)
        return widget_list

    @staticmethod
    def _make_connections(transmitter, receiver):
        transmitter.view.image.double_clicked.connect(
            lambda: (receiver.update_viewpoint(), receiver.set_view_output())
        )
        transmitter.view.image.scrolled.connect(
            lambda value_delta: (
                receiver.update_section(value_delta=value_delta),
                receiver.set_view_output(),
            )
        )

    def make_connections(self):
        super().make_connections()
        Output3dImageMixin._make_connections(self, self)
        for widget in self._get_related_widgets(self):
            Output3dImageMixin._make_connections(widget, self)
            Output3dImageMixin._make_connections(self, widget)

    def update_viewpoint(self, value_delta: int = 1, value: int = None):
        if value is None:
            self.viewpoint += value_delta
        else:
            self.viewpoint = value
        if self.viewpoint == 3:
            self.viewpoint = 0

    def update_section(self, value_delta: int = 0, value: int = None):
        if isinstance(self.output, Exception):
            return
        if value is None:
            self.sections[self.viewpoint] += value_delta
        else:
            self.sections[self.viewpoint] = value
        if self.sections[self.viewpoint] < 0:
            self.sections[self.viewpoint] = 0
        elif self.sections[self.viewpoint] >= self.output.shape[self.viewpoint]:
            self.sections[self.viewpoint] = self.output.shape[self.viewpoint] - 1

    def init_sections_and_viewpoint(self):
        s1, s2, s3 = self.output.shape
        self.viewpoint = 0
        self.sections = [int(s1 / 2), int(s2 / 2), int(s3 / 2)]
        if len(self.parent_list) > 0:
            w = self.parent_list[0]
            for i in range(3):
                self.update_viewpoint(value=i)
                self.update_section(value=w.sections[i])
            self.update_viewpoint(value=w.viewpoint)

    def set_view_output(self, output: Union[np.ndarray, Exception] or None = None):
        if not isinstance(self.output, Exception):
            if isinstance(output, np.ndarray):
                self.init_sections_and_viewpoint()
            if self.viewpoint == 0:
                output = self.output[self.sections[0]]
            elif self.viewpoint == 1:
                output = self.output[:, self.sections[1]]
            elif self.viewpoint == 2:
                output = self.output[:, :, self.sections[2]]
        return super().set_view_output(output)

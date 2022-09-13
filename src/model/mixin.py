import pickle

import numpy as np


class OutputImageMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_downgraded = False
        self.path = "tmp.pkl"

    def downgrade_raw_array(self, raw_arr: np.ndarray) -> np.ndarray:
        """return downgraded data"""
        max_size = 10
        self.is_downgraded = False
        if raw_arr.size > max_size:
            with open(self.path, "wb") as f:
                pickle.dump(raw_arr, f)
            self.is_downgraded = True
            return raw_arr.astype(np.uint8)
        return raw_arr

    def get_view_output(self):
        """return"""
        if self.is_downgraded:
            with open(self.path, "rb") as f:
                return pickle.load(f)
        else:
            super().get_view_output()

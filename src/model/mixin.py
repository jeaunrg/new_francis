import pickle
import sys

import numpy as np
from skimage.measure import block_reduce


class OutputImageMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_downsized = False
        self.path = "tmp.npy"

    @staticmethod
    def get_block_size(ratio, ndim):
        block_size = int(ratio ** (1 / ndim))
        return tuple([block_size] * ndim)

    def downsize_raw_array(self, raw_arr: np.ndarray) -> np.ndarray:
        """return downgraded data"""
        max_size = 1000000
        self.is_downsized = False
        ratio = raw_arr.nbytes / max_size
        print(raw_arr.nbytes, raw_arr.shape, raw_arr.dtype)
        if ratio > 1:
            np.save(self.path, raw_arr)
            self.is_downsized = True
            blok_size = OutputImageMixin.get_block_size(ratio, raw_arr.ndim)
            arr = block_reduce(raw_arr, blok_size, func=np.mean).astype(np.uint8)
            return arr
        return raw_arr

    def get_raw_array(self):
        if self.is_downsized:
            return np.load(self.path)

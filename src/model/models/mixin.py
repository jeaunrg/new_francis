import os
import uuid

import numpy as np
from skimage.measure import block_reduce


class CompressionMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.block_size = None
        self.has_downsized_output = True
        self.path = str(uuid.uuid4()) + ".npy"

    def get_heritage(self) -> dict:
        attributes = super().get_heritage()
        attributes["block_size"] = self.block_size
        return attributes

    def _downsample_raw_array(self, arr: np.ndarray) -> np.ndarray:
        if self.block_size is None:
            ratio = arr.nbytes / 1000000
            if ratio > 1:
                block_size = int(ratio ** (1 / arr.ndim))
            else:
                block_size = 1
            self.block_size = tuple([block_size] * arr.ndim)
        np.save(self.path, arr)
        arr = block_reduce(arr, self.block_size, func=np.mean)
        return arr

    def downsize(f):
        def wrapper(cls, *args, **kwargs):
            output = f(cls, *args, **kwargs)
            if isinstance(output, np.ndarray):
                output = cls._downsample_raw_array(output)
                output = output.astype(np.uint8)
            return output

        return wrapper

    def get_raw_array(self):
        return np.load(self.path)

    def delete_raw_array(self):
        if os.path.isfile(self.path):
            os.remove(self.path)

    def clean(self):
        self.delete_raw_array()

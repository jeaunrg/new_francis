import uuid

import numpy as np
from skimage.measure import block_reduce


class OutputImageMixin:
    def __init__(self, block_size=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.block_size = block_size
        self.is_downsized = False
        self.path = str(uuid.uuid4()) + ".npy"

    def get_heritage(self) -> dict:
        attributes = super().get_heritage()
        attributes["block_size"] = self.block_size
        return attributes

    def downsample_raw_array(self, arr: np.ndarray) -> np.ndarray:
        self.is_downsized = False
        if self.block_size is None:
            ratio = arr.nbytes / 1000000
            if ratio > 1:
                self.is_downsized = True
                np.save(self.path, arr)
                block_size = int(ratio ** (1 / arr.ndim))
            else:
                block_size = 1
            self.block_size = tuple([block_size] * arr.ndim)
        arr = block_reduce(arr, self.block_size, func=np.mean)
        return arr

    def downsize_output(f):
        def wrapper(cls, *args, **kwargs):
            output = f(cls, *args, **kwargs)
            if isinstance(output, np.ndarray):
                output = cls.downsample_raw_array(output)
                output = output.astype(np.uint8)
            return output

        return wrapper

    def get_raw_array(self):
        return np.load(self.path)

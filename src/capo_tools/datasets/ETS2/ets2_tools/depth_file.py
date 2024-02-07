import os.path
import struct
import warnings

import numpy as np
import rawutil


def read_depth_file(file_path: str) -> 'ETS2DepthFile':
    ets2_depth_file = ETS2DepthFile(file_path, eager_load=True)
    return ets2_depth_file


class ETS2DepthFileHeader:
    def __init__(self, data):
        """
        ETS2 Datset depth file header
        Args:
            data ():
        """
        self.magic: str = None
        self.size: int = None
        self.width: int = None
        self.height: int = None
        self.min_val: int = None
        self.max_val: int = None
        self.offset: int = None
        self.bit_depth: int = None
        self._read_header(data)

    def _read_header(self, data):
        if len(data) == 3525146:
            header = {
                "magic": bytes(struct.unpack('bb', data[0:2])).decode('utf-8'),
                "size": struct.unpack('<l', data[2:6])[0],
                "width": struct.unpack('<l', data[6:10])[0],
                "height": struct.unpack('<l', data[10:14])[0],
                "min_val": struct.unpack('<f', data[14:18])[0],
                "max_val": struct.unpack('<f', data[18:22])[0],
                "offset": struct.unpack('<l', data[22:26])[0],
                "bit_depth": 24
            }
        else:
            header = {
                "magic": bytes(struct.unpack('bb', data[0:2])).decode('utf-8'),
                "size": struct.unpack('<l', data[2:6])[0],
                "width": struct.unpack('<l', data[6:10])[0],
                "height": struct.unpack('<l', data[10:14])[0],
                "min_val": struct.unpack('<f', data[14:18])[0],
                "max_val": struct.unpack('<f', data[18:22])[0],
                "bit_depth": struct.unpack('<h', data[22:24])[0],
                "offset": struct.unpack('<l', data[24:28])[0]
            }

        self.__dict__.update(header)
        del header

    def __str__(self):
        return (f"magic: {self.magic}, "
                f"size: {self.size}, "
                f"widht: {self.width}, "
                f"height: {self.height}, "
                f"minimum value: {self.min_val}, "
                f"maximum value: {self.max_val}, "
                f"bit depth: {self.bit_depth}, "
                f"offset: {self.offset}")


class ETS2DepthFile:
    def __init__(self, file: str, far_value: float = 10000, eager_load: bool = True):
        """
        ETS2 dataset depth file reader
        Args:
            file ():
            far_value ():
            eager_load ():
        """
        # File must exist
        assert os.path.exists(file)
        self.base, _file_name = os.path.split(file)
        self.file_name, self.ext = os.path.splitext(_file_name)

        # File name assertions
        assert self.ext == ".raw"
        assert len(self.file_name.split('.')) > 1
        assert self.file_name.split('.')[1] == 'depth'

        self.bit_depth = None
        self.data = None

        self.eager_load = eager_load
        self.far_value = far_value
        self._read_depth_file()

    def _read_depth_file(self):
        data = np.fromfile(os.path.join(self.base, f"{self.file_name}{self.ext}"), dtype='byte')
        self.header = ETS2DepthFileHeader(data)

        # TODO: review, find a better way to do this,
        #
        self.is_real_depth = (self.header.bit_depth == 16)

        if self.eager_load:
            self._read_data(data)
            del data

    def _read_depth_data(self, file_data):
        data_bytes = self.header.bit_depth // 8
        denorm = pow(2, 24) - 1
        # TODO: Review, this hardcoded 28 should be self.header.offset?
        format = '<%sU' % int((self.header.size - 26) / data_bytes)
        self.data = np.array(rawutil.unpack(format, file_data[self.header.offset:]))
        # self.data = -np.frombuffer(file_data[self.header.offset:], dtype=np.float16).astype(np.float32)
        self.data = self.data / denorm
        # data = normalize(data)

    def _read_realdepth_data(self, file_data):
        data_bytes = self.header.bit_depth // 8

        # TODO: Review, make sure this is the same, as np.from_buffer is much much faster than rawutil.unpack
        # TODO: Review, this hardcoded 28 should be self.header.offset?
        # format = '<%se' % int((self.header.size - 28) / data_bytes)
        # self.data = -np.array(rawutil.unpack(format, file_data[self.header.offset:]))
        self.data = -np.frombuffer(file_data[self.header.offset:], dtype=np.float16).astype(np.float32)

        # NaN handling
        data_nans = np.count_nonzero(np.isnan(self.data))
        if data_nans > 0:
            warnings.warn(f"{os.path.join(self.base, f'{self.file_name}{self.ext}')}: There are {data_nans} NaN values in depth data, transforming them to zeros")
            self.data[np.isnan(self.data)] = 0

    def _read_data(self, data):
        if self.is_real_depth:
            self._read_realdepth_data(data)
        else:
            self._read_depth_data(data)

    def get_data(self):
        if self.data is None:
            data = np.fromfile(os.path.join(self.base, f"{self.file_name}{self.ext}"), dtype='byte')
            self._read_data(data)
            del data

        return self.data

    def size(self):
        return self.header.width, self.header.height
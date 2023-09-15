import struct
import pandas as pd
    
class Decoder():
    DATA_FORMAT = 'lL?BBllllfffffffffffffffffBf'
    DATA_SIZE = struct.calcsize(DATA_FORMAT)
    DATA_FRAME_HEADERS = ["Timestamp (ms)", ""]
    _source_path : str
    _output_dir : str
    
    _dataframe : pd.DataFrame

    def __init__(self, source_path: str, _output_dir: str="output/") -> None:
        self._source_path = source_path
        self._output_dir = _output_dir
        
    @property
    def acceleration(self):
        return self.decode().iloc[:, [0, 8, 9, 10]]
    
    @property
    def rotation_rate(self):
        return self.decode().iloc[:, [0, 11, 12, 13]]
        
    def decode(self):
        if not self._dataFrame:
            data = []
            with open(self._source_path, "rb") as file:
                while True:
                    buf = file.read(self.DATA_SIZE)
                    if not buf:
                        break
                    
                    # Unpack the binary data using the specified format
                    unpacked_data = struct.unpack(self.DATA_FORMAT, buf)
                    timestamp_redux = unpacked_data[0]*1e3 + unpacked_data[1] # Merge timestamps and convert to milliseconds
                    unpacked_data_fixed = (timestamp_redux,) + unpacked_data[2:] # Replace old timestamps with newly formatted one
                    data.append(unpacked_data_fixed)
            self._dataFrame = pd.DataFrame(data)
        return self._dataFrame
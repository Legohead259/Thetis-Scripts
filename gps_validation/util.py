from ctypes import *
from math import inf
import pandas as pd
import matplotlib as plt

class ThetisData(Structure):
    """
    Data structure used by Thetis to log telemetry data
    """
    _fields_ = [('epoch', c_long),
                ('mSecond', c_ulong),
                ('GPSYear', c_uint16),
                ('GPSMonth', c_uint8),
                ('GPSDay', c_uint8),
                ('GPSHour', c_uint8),
                ('GPSMinute', c_uint8),
                ('GPSSecond', c_uint8),
                ('GPSHundredth', c_uint8),
                ('voltage', c_float),
                ('GPSFix', c_bool),
                ('numSats', c_uint8),
                ('HDOP', c_uint8),
                ('latitude', c_long),
                ('longitude', c_long),
                ('GPSSpeed', c_long),
                ('GPSCourse', c_long),
                ('sysCal', c_uint8),
                ('gyroCal', c_uint8),
                ('accelCal', c_uint8),
                ('magCal', c_uint8),
                ('rawAccelX', c_float),
                ('rawAccelY', c_float),
                ('rawAccelZ', c_float),
                ('accelX', c_float),
                ('accelY', c_float),
                ('accelZ', c_float),
                ('rawGyroX', c_float),
                ('rawGyroY', c_float),
                ('rawGyroZ', c_float),
                ('gyroX', c_float),
                ('gyroY', c_float),
                ('gyroZ', c_float),
                ('rawMagX', c_float),
                ('rawMagY', c_float),
                ('rawMagZ', c_float),
                ('magX', c_float),
                ('magY', c_float),
                ('magZ', c_float),
                ('roll', c_float),
                ('pitch', c_float),
                ('yaw', c_float),
                ('linAccelX', c_float),
                ('linAccelY', c_float),
                ('linAccelZ', c_float),
                ('quatW', c_float),
                ('quatX', c_float),
                ('quatY', c_float),
                ('quatZ', c_float),
                ('imuTemp', c_float),
                ('state', c_uint8)]


def read_oscilloscope_data(path: str):
    df = pd.read_csv(path, names=["time", "voltage"])
    df.time = df.time + abs(min(df.time)) # Shift all the time values such that they start at 0
    print(df.time) # DEBUG
    fig = plt.figure()
    


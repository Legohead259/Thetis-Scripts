"""
Script that will calculate the theoretical sine wave generated by the DataPhysics V-20 shaker table. The experimental setup consists of the following:


  ┌─────────┐                                  ┌────────────┐
  │SensoTec ├──────────────────────────────────►Oscilloscope│
  │Amplifier│                                  └──▲─────────┘
  └────▲────┘                                     │
       │                                          │
       │                                       ┌──┴──────┐
       │             ┌─────────────────┐       │Waveform │
       │             │Thetis Instrument│       │Generator│
       │             │     Package     │       └──┬──────┘
       │             └─▲───────────────┘          │
       │               │                          │
  ┌────┴────────┐    ┌─┴──────────────┐        ┌──▼───────────────┐
  │SensoTec     ├────►DataPhysics V-20◄────────┤DataPhysics PA300E│
  │Accelerometer│    │Vibration Table │        │    Amplifier     │
  └─────────────┘    └────────────────┘        └──────────────────┘


The waveform generator will create a sinusoidal waveform at a given frequency, f, (maximum 20 Hz) that is sent to the amplifier. The amplifier then converts that to a signal that drives the vibration table at a higher amplitude.

At lower frequencies, the vibration table is unable to generate a clean sine wave signal. Therefore, another accelerometer of known calibration was attached to the vibration table in the axis of movement to act as a ground truth reference. It is this ground truth that will be compared with the Thetis data to validate the instrument.
Data is recorded from the accelerometer using the oscilloscope. These data files are saved as CSVs that can be plotted alongside the Thetis data.

To plot the data appropriately, we need to scale both accelerations to the same scale. We will use the Thetis scale as the "true" scale and therefore need to convert the accelerometer readings (presented as V) to meters per second squared. We can use the known calibration constants for the accelerometer and in-line amplifier to accomplish this using the following equation:

    a(t) [m/s/s] = ß [mV/V] / α [mV/g] * 9.81 [m/s/s / g] * V(t) [V]

CHANGELOG:
 - Version 1.0: Initial Release
 - Version 2.0: Revamped to account for new testing procedure

TODO:
"""

__author__      = "Braidan Duffy"
__copyright__   = "Copyright 2022"
__credits__     = "Braidan Duffy"
__license__     = "MIT"
__version__     = "2.0.0"
__maintainer__  = "Braidan Duffy"
__email__       = "bduffy2018@my.fit.edu"

from ctypes import sizeof
from util import ThetisData, read_oscilloscope_data
import matplotlib.pyplot as plt
import datetime as dt
from math import pi
import numpy as np
import pandas as pd

# Constants and measurements
ALPHA = 5.296                       # Accelerometer sensitivity - mV/g
BETA = 20                           # Amplifier gain - mV/V
SCALE_FACTOR = BETA / ALPHA * 9.81 # Convert oscilloscope voltage measurements to accelerations - m/s/s / V


# =================================
# === READ IN OSCILLOSCOPE DATA ===
# =================================

df = pd.read_csv("vibration_validation/data/x-axis/x_scope_3_6Hz.CSV", names=["time", "voltage"])
df.time = df.time + abs(min(df.time)) # Shift all the time values such that they start at 0
scope_accel = df.voltage * SCALE_FACTOR # Scale all the voltage values to accelerations


# ===========================
# === READ IN THETIS DATA ===
# ===========================


with open('vibration_validation/data/x-axis/x_thetis_3_6Hz.bin', 'rb') as file:
    epoch_data = []
    raw_accel_data = []
    accel_data = []

    data = ThetisData()
    while file.readinto(data) == sizeof(data):
        timestamp = dt.datetime.utcfromtimestamp(data.epoch) + dt.timedelta(milliseconds=data.mSecond)
        epoch_data.append(timestamp)
        raw_accel_data.append((data.rawAccelX))
        # accel_data.append((data.accelX, data.accelY, data.accelZ))
        accel_data.append(data.accelX)

# Generate theoretical sinusoidal data
# START_INDEX = 0
START_INDEX = 233
# TIME_WIDTH = len(epoch_data)
TIME_WIDTH = 22
END_INDEX = START_INDEX + TIME_WIDTH

x_meas = [epoch_data[START_INDEX + x]-epoch_data[START_INDEX] for x in range(TIME_WIDTH)]
x_meas = [x_meas[x].total_seconds() for x in range(TIME_WIDTH)]

# Make plots
# fig_accel = plt.figure(1)
# ax_accel = fig_accel.add_subplot(1,1,1)
# ax_accel.set_title("Comparison of Raw and Filtered Accelerations")
# ax_accel.plot(epoch_data, raw_accel_data)
# ax_accel.plot(epoch_data, accel_data)
# ax_accel.set_xlabel("Timestamp")
# ax_accel.set_ylabel("Accelerations [m/s/s]")
# ax_accel.legend(["Raw", "Kalman Filtered"])


fig_comp = plt.figure(2)
ax_comp = fig_comp.add_subplot(1,2,1)
ax_comp.set_title("Comparison of Measured and Reference Accelerations")
ax_comp.plot(x_meas, raw_accel_data[START_INDEX:END_INDEX], 'o-')
# ax_comp.plot(x_meas, accel_data[START_INDEX:END_INDEX], 'o-')
ax_comp.plot(df.time, scope_accel)
ax_comp.set_xlabel("Time [s]")
ax_comp.set_ylabel("Accelerations [m/s/s]")
ax_comp.legend(["Thetis (Raw)", "Reference"])

ax_scale = fig_comp.add_subplot(1,2,2)
ax_scale.set_title("Comparison of Measured and Scaled Reference Accelerations")
ax_scale.plot(x_meas, raw_accel_data[START_INDEX:END_INDEX], 'o-')
ax_scale.plot(df.time, scope_accel*2.8)
ax_scale.set_xlabel("Time [s]")
ax_scale.set_ylabel("Accelerations [m/s/s]")
ax_scale.legend(["Thetis (Raw)", "Reference (x2.8)"])

print("Number of samples: ", len(epoch_data)) #DEBUG
print("Total Sample Time: ", max(x_meas)) #DEBUG
print("Average Sample Rate: ", len(epoch_data) / max(x_meas)) #DEBUG

plt.show()
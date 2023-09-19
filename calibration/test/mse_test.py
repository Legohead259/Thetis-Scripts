
"""
ChatGPT Conversation: https://chat.openai.com/c/ef545f4e-6aa6-4598-8c37-371934ac2cd9
"""

import os
import matplotlib.pyplot as plt
import pandas as pd
import math
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages  # Add this import
from scipy import signal


# Define the root directory
root_dir = "C:/Users/bduffy2018/OneDrive - Florida Institute of Technology/School/Thesis/Experiments/Calibration/x-IMU3"
output_pdf = 'mse_test.pdf'

# Initialize an empty list to store the sensor information
sensor_data = []

# Iterate through the directories
for sensor_dir in os.listdir(root_dir):
    sensor_name, axis, ground_truth_name = sensor_dir.split("_")

    # Process into a more usable format
    if sensor_name == "accel":
        sensor_name = "Accelerometer"
        unit = "g"
        
        if axis == "x-axis":
            ground_truth_value = -1 * math.cos(math.radians(float(ground_truth_name)))
        elif axis == "y-axis":
            ground_truth_value = 1 * math.cos(math.radians(float(ground_truth_name)))
        elif axis == "z-axis":
            ground_truth_value = -1 * math.cos(math.radians(float(ground_truth_name)))
            
        ground_truth_name += " degrees"
            
    elif sensor_name == "gyro":
        sensor_name = "Gyroscope"
        unit = "deg/s"
        ground_truth_value = float(ground_truth_name)
        ground_truth_name = f"{ground_truth_value} {unit} CCW" if ground_truth_value < 0 else f"{ground_truth_value} {unit} CW"
        
        
    axis = axis[0].capitalize()
    
    # Initialize a dictionary to store the sensor information
    sensor_info = {
        "sensor_name": sensor_name,
        "axis": axis,
        "ground_truth_name": ground_truth_name,
        "ground_truth_value": ground_truth_value,
        "devices": [],
        "unit": unit
    }

    # Iterate through the device directories
    device_dir = os.path.join(root_dir, sensor_dir)
    for device_dir_name in os.listdir(device_dir):
        # print(device_dir_name.split())
        device_id = device_dir_name.split()[0]
        inertial_csv_path = os.path.join(device_dir, device_dir_name, "Inertial.csv")
        
        # Append the device information to the sensor dictionary
        sensor_info["devices"].append({
            "device_id": device_id,
            "inertial_csv_path": inertial_csv_path
        })

    # Append the sensor dictionary to the list
    sensor_data.append(sensor_info)


def reject_outliers(data, m = 2.):
    d = np.abs(data - np.median(data))
    mdev = np.median(d)
    s = d/mdev if mdev else np.zeros(len(d))
    return data[s<m]


def upsample_data(data, original_sample_rate, target_sample_rate):
    ratio = target_sample_rate / original_sample_rate
    return signal.resample(data, int(len(data)*ratio))


def percent_difference(v1, v2):
    return np.abs(v1-v2) / (np.mean([v1,v2])) * 100


def mse(v1, v2):
    return np.mean((v1-v2)**2)


def msep(v_true, v_meas):
    return np.mean(((v_true-v_meas) / v_true)**2)


with PdfPages(output_pdf) as pdf:

    for sensor_info in sensor_data:
        # Create a figure with two subplots side by side
        fig, ax = plt.subplots(1, 1, figsize=(12, 4))
        m0_list = []
        
        # Iterate through devices
        for i, device in enumerate(sensor_info["devices"]):
            # Load the CSV data into a DataFrame
            df = pd.read_csv(device["inertial_csv_path"])
            timestamps = df["Timestamp (us)"]
            data = df[f"{sensor_info['sensor_name']} {sensor_info['axis']} ({sensor_info['unit']})"]
            data = reject_outliers(data)
                
            print(len(data))
            
            # Plot the data on the respective subplot     
            f_ref, psd_ref = signal.periodogram(data, 50)
            ax.plot(f_ref, psd_ref, label=f'{device["device_id"]}')
            ax.set_xlabel('Frequency (Hz)')
            ax.set_ylabel('Vibration Energy [$m^2/s^3$]')
            
            m0 = np.sum(f_ref * psd_ref) / np.sum(psd_ref)
            m0_list.append(m0)
        
        diff = percent_difference(m0_list[0], m0_list[1])
        print(f"{diff:0.1f} %")
        
        ax.legend()
        # Set the title for the whole figure
        fig.suptitle(f"{sensor_info['sensor_name']} {sensor_info['axis']} | {sensor_info['ground_truth_name']}")
        
        fig.text(0.7, 0.91, f"$m_0$ Percent Difference: {diff:0.1f}%", fontsize=12)

        # Adjust layout to prevent overlapping
        # plt.tight_layout()

        # Show the plot or save it as an image (optional)
        # plt.show()  # Use plt.savefig("filename.png") to save as an image instead of displaying
        
        pdf.savefig(fig, bbox_inches='tight')
        plt.close(fig)

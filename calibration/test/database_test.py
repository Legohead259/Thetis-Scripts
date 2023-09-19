"""
ChatGPT Conversation: https://chat.openai.com/c/ef545f4e-6aa6-4598-8c37-371934ac2cd9
"""

import os
import matplotlib.pyplot as plt
import pandas as pd
import math
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages  # Add this import

# Define the root directory
root_dir = "C:/Users/bduffy2018/OneDrive - Florida Institute of Technology/School/Thesis/Experiments/Calibration/x-IMU3"
output_pdf = 'output_plots.pdf'

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

# Now, sensor_data contains a list of dictionaries with sensor information

# Example usage:
# for sensor_info in sensor_data:
#     print(f"Sensor Name: {sensor_info['sensor_name']}")
#     print(f"Axis: {sensor_info['axis']}")
#     print(f"Ground Truth: {sensor_info['ground_truth']}")
#     for device in sensor_info["devices"]:
#         print(f"Device ID: {device['device_id']}")
#         print(f"Inertial CSV Path: {device['inertial_csv_path']}")


def RMSE(time_series: np.ndarray, ground_truth: float):
    return np.sqrt(np.mean((time_series - ground_truth) ** 2))


# def dynamically_trim_time_series(time_series, threshold):
#     """
#     Dynamically trim a time series by removing data points with z-scores exceeding a threshold.

#     Args:
#         time_series (numpy.ndarray): Array containing the time series data.
#         threshold (float): Threshold for z-scores.

#     Returns:
#         numpy.ndarray: Trimmed time series.
#     """
#     z_scores = np.abs((time_series - np.mean(time_series)) / np.std(time_series))
#     outliers = z_scores > threshold

#     return time_series[~outliers]


def reject_outliers(data, m = 2.):
    d = np.abs(data - np.median(data))
    mdev = np.median(d)
    s = d/mdev if mdev else np.zeros(len(d))
    return data[s<m]


def down_sample_average(data: np.array, n: int=2) -> np.array:
    """Down samples a data array by a factor.
    For example, if data is a time series sampled at 100 Hz, down_sample_average(data)
    will return the array averaged to 50 Hz.

    Args:
        data (np.array): The time series data to be modified
        n (int): the factor of reduction. 2 for half rate, 3 for third, etc. Defaults to 2

    Returns:
        np.array: The down sampled array
    """
    end = n * int(len(data)/n)
    return np.mean(data[:end].reshape(-1, n), axis=1)


with PdfPages(output_pdf) as pdf:

    for sensor_info in sensor_data:
        # Create a figure with two subplots side by side
        fig, axes = plt.subplots(1, 2, figsize=(12, 4))

        # Iterate through devices
        for i, device in enumerate(sensor_info["devices"]):
            # Load the CSV data into a DataFrame
            df = pd.read_csv(device["inertial_csv_path"])
            
            # Plot the data on the respective subplot
            ax = axes[i]
            timestamps = df["Timestamp (us)"]
            data = df[f"{sensor_info['sensor_name']} {sensor_info['axis']} ({sensor_info['unit']})"].to_numpy()
            
            if sensor_info['sensor_name'] == "x-IMU3": # Downsample x-IMU3 data to 100 Hz
                data = down_sample_average(data)
                
            data = reject_outliers(data)
            
            ax.plot(data)  # Assuming Time and Value are column names

            # Plot the ground truth value
            ax.axhline(y=sensor_info['ground_truth_value'], color='r', linestyle='--')
            
            # Add a label for the RMSE
            rmse = RMSE(data, sensor_info['ground_truth_value'])
            # print(f"RMSE: {rmse:0.3f} {sensor_info['unit']}")
            # ax.text(0.5, 0.5, f"RMSE: {rmse:0.3f} {sensor_info['unit']}", fontsize=12, color='blue', va='center', ha='left', rotation='vertical')
            fig.text(0.12+0.68*i, 0.91, f"RMSE: {rmse:0.3f} {sensor_info['unit']}", fontsize=12, color='blue', va='center', ha='left')
            
            # Set title and labels
            ax.set_title(f"{device['device_id']}")
            ax.set_xlabel("Time")
            ax.set_ylabel("Value")

        # Set the title for the whole figure
        fig.suptitle(f"{sensor_info['sensor_name']} {sensor_info['axis']} | {sensor_info['ground_truth_name']}")

        # Adjust layout to prevent overlapping
        # plt.tight_layout()

        # Show the plot or save it as an image (optional)
        plt.show()  # Use plt.savefig("filename.png") to save as an image instead of displaying
        
        # pdf.savefig(fig, bbox_inches='tight')
        # plt.close(fig)

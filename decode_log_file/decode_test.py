import numpy as np
import matplotlib.pyplot as plt
import struct

# Define the structure format for reading the binary data
data_format = 'lL?BBllllfffffffffffffffffBf'

# Calculate the size of the data structure in bytes
data_size = struct.calcsize(data_format)
print(data_size)

# Initialize lists to store the extracted data
timestamps = []
accel_data = []
gyro_data = []

# Open the binary file for reading
with open("data/caldata_accel_x.bin", "rb") as file:
    while True:
        data = file.read(data_size)
        if not data:
            break
        
        # Unpack the binary data using the specified format
        unpacked_data = struct.unpack(data_format, data)
        
        # Extract the required values
        timestamp = unpacked_data[0]
        accel_x, accel_y, accel_z = unpacked_data[11:14]
        gyro_x, gyro_y, gyro_z = unpacked_data[14:17]
        
        # Append the values to the corresponding lists
        timestamps.append(timestamp)
        accel_data.append([accel_x, accel_y, accel_z])
        gyro_data.append([gyro_x, gyro_y, gyro_z])

# Convert lists to NumPy arrays
timestamps = np.array(timestamps)
accel_data = np.array(accel_data)
gyro_data = np.array(gyro_data)

# Plot accelerometer data
plt.figure(figsize=(10, 6))
plt.plot(accel_data[:, 0], label='Accel X')
plt.plot(accel_data[:, 1], label='Accel Y')
plt.plot(accel_data[:, 2], label='Accel Z')
plt.xlabel('Timestamp')
plt.ylabel('Acceleration (m/s^2)')
plt.title('Accelerometer Data')
plt.legend()
plt.grid(True)
plt.show()

# Plot gyroscope data
plt.figure(figsize=(10, 6))
plt.plot(gyro_data[:, 0], label='Gyro X')
plt.plot(gyro_data[:, 1], label='Gyro Y')
plt.plot(gyro_data[:, 2], label='Gyro Z')
plt.xlabel('Timestamp')
plt.ylabel('Angular Velocity (rad/s)')
plt.title('Gyroscope Data')
plt.legend()
plt.grid(True)
plt.show()

# Save the data to separate column vectors
np.savetxt("accel_data.csv", accel_data, delimiter=",")
np.savetxt("gyro_data.csv", gyro_data, delimiter=",")
import pandas as pd
import matplotlib.pyplot as plt

# Read CSV file
# df = pd.read_csv('E:/gyro_z-axis_200/Connection 0/Inertial.csv')  # Replace 'your_file.csv' with your actual file name
df = pd.read_csv('C:/Users/bduffy2018/OneDrive - Florida Institute of Technology/School/Thesis/Experiments/Calibration/x-IMU3/gyro_z-axis_200/x-IMU3 - 6BFD-5410-EC7B-DA7B (UDP)/Inertial.csv')  # Replace 'your_file.csv' with your actual file name

# Create the plot
plt.figure(figsize=(10, 6))

# Plot the data
plt.plot(df['Timestamp (us)'], df['Gyroscope Z (deg/s)'])  # Replace 'Column1' and 'Column2' with actual column names

# Add labels and title
plt.xlabel('X Axis Label')
plt.ylabel('Y Axis Label')
plt.title('CSV Data Plot')

# Enable zooming and panning
plt.gca().set(title='Scroll to zoom, drag to pan', autoscale_on=False)
plt.gca().set_yscale('linear')
plt.gca().set_xscale('linear')
plt.gca().autoscale(tight=False)

# Show the plot
plt.show()

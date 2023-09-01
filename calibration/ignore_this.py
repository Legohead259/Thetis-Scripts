import pandas as pd
import numpy as np
from scipy.optimize import minimize

# Load the CSV file into a Pandas DataFrame
datafile_x = "data/caldata_accel_x/Thetis - Unknown (USB)/Inertial.csv"  # Replace with your CSV file path
datafile_y = "data/caldata_accel_y/Thetis - Unknown (USB)/Inertial.csv"  # Replace with your CSV file path
datafile_z = "data/caldata_accel_z/Thetis - Unknown (USB)/Inertial.csv"  # Replace with your CSV file path
df_x = pd.read_csv(datafile_x)
df_y = pd.read_csv(datafile_y)
df_z = pd.read_csv(datafile_z)

# Extract timestamps
timestamps_x = df_x['Timestamp (us)']
timestamps_y = df_y['Timestamp (us)']
timestamps_z = df_z['Timestamp (us)']

# Extract accelerometer XYZ columns
accel_data_x = df_x[['Accelerometer X (g)', 'Accelerometer Y (g)', 'Accelerometer Z (g)']].to_numpy()
accel_data_y = df_y[['Accelerometer X (g)', 'Accelerometer Y (g)', 'Accelerometer Z (g)']].to_numpy()
accel_data_z = df_z[['Accelerometer X (g)', 'Accelerometer Y (g)', 'Accelerometer Z (g)']].to_numpy()

offset_x = np.mean(accel_data_x[0])
offset_y = np.mean(accel_data_y[1])
offset_z = np.mean(accel_data_z[2])
offset = np.vstack((offset_x, offset_y, offset_z))

# Establish reference vectors
ref_data_x = np.array([[-1, 0, 0] for _ in range(len(accel_data_x))])
ref_data_y = np.array([[0, -1, 0] for _ in range(len(accel_data_y))])
ref_data_z = np.array([[0, 0, 1] for _ in range(len(accel_data_z))])

# TODO: Plot data

I_u_list = np.vstack((accel_data_x, accel_data_y, accel_data_z))
I_ref_list = np.vstack((ref_data_x, ref_data_y, ref_data_z))
num_samples = len(I_u_list)  # Adjust the number of samples as needed

print(I_u_list)
print(I_ref_list)
print(num_samples)

# Define the loss functions
def rmse_loss(M_flattened):
    M = M_flattened.reshape((3, 3))
    total_loss = 0.0
    
    for i in range(num_samples):
        difference = np.dot(I_u_list[i], M) - I_ref_list[i]
        rmse = np.linalg.norm(difference)**2
        total_loss += rmse
    
    return np.sqrt(total_loss)

# Remove bias from the signal
# I_u_list = np.array([I_u_list[u] - offset for u in range(len(I_u_list))])

# Initial guess for M
initial_M = np.zeros((3, 3))

# Perform optimization for each loss function
result_rmse = minimize(rmse_loss, initial_M.flatten(), method='SLSQP')

# Reshape the results to get the 3x3 matrices M
optimal_M_rmse = result_rmse.x.reshape((3, 3))

# Function to extract diagonal matrix and return normalized M and diagonal
def extract_diagonal_matrix(matrix):
    diagonal = np.diag(matrix)
    normalized_M = matrix / diagonal
    return normalized_M, diagonal

# Extract diagonal and normalize for each optimization result
normalized_M_rmse, sensitivity_rmse = extract_diagonal_matrix(optimal_M_rmse)

# Compare the results
# print("Bias (offset):")
# print(offset)
# print()

print("Sensitivity (diagonal) vector (MSE loss):")
print(sensitivity_rmse)
print()

print("Normalized M matrix (MSE loss):")
print(normalized_M_rmse)
print()
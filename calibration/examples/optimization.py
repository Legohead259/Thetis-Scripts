import numpy as np
from scipy.optimize import minimize

# Example data (replace with your actual values)
num_samples = 5  # Adjust the number of samples as needed

I_u_list = [np.random.rand(1, 3) for _ in range(num_samples)]
I_ref_list = [np.random.rand(1, 3) for _ in range(num_samples)]

# Calculate average component values across all I_u vectors
bias = np.mean(np.array([u[0] for u in I_u_list]), axis=0)

# Subtract bias from each vector in I_u_list
for i in range(num_samples):
    I_u_list[i] -= bias

# Define the loss functions
def mse_loss(M_flattened):
    M = M_flattened.reshape((3, 3))
    total_loss = 0.0
    
    for i in range(num_samples):
        difference = np.dot(I_u_list[i], M) - I_ref_list[i]
        mse = np.sum(difference**2)
        total_loss += mse
    
    return total_loss / num_samples

# Define the loss functions
def rmse_loss(M_flattened):
    M = M_flattened.reshape((3, 3))
    total_loss = 0.0
    
    for i in range(num_samples):
        difference = np.dot(I_u_list[i], M) - I_ref_list[i]
        rmse = np.linalg.norm(difference)**2
        total_loss += rmse
    
    return np.sqrt(total_loss)

# Initial guess for M
initial_M = np.zeros((3, 3))

# Perform optimization for each loss function
result_mse = minimize(mse_loss, initial_M.flatten(), method='SLSQP')
result_rmse = minimize(rmse_loss, initial_M.flatten(), method='SLSQP')

# Reshape the results to get the 3x3 matrices M
optimal_M_mse = result_mse.x.reshape((3, 3))
optimal_M_rmse = result_rmse.x.reshape((3, 3))

# Function to extract diagonal matrix and return normalized M and diagonal
def extract_diagonal_matrix(matrix):
    diagonal = np.diag(matrix)
    normalized_M = matrix / diagonal
    return normalized_M, diagonal

# Extract diagonal and normalize for each optimization result
normalized_M_mse, sensitivity_mse = extract_diagonal_matrix(optimal_M_mse)

# Compare the results
print("Optimal M matrix (MSE loss):")
print(optimal_M_mse)

print("Optimal M matrix (RMSE loss):")
print(optimal_M_rmse)

print("Sensitivity (diagonal) vector (MSE loss):")
print(sensitivity_mse)

print("Normalized M matrix (MSE loss):")
print(normalized_M_mse)

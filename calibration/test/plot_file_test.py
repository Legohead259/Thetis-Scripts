import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages  # Add this import

# Define source directory and output PDF file name
source_dir = 'C:/Users/bduffy2018/OneDrive - Florida Institute of Technology/School/Thesis/Experiments/Calibration/x-IMU3'
output_pdf = 'output_plots.pdf'

# Create a list to hold the plots
plots = []

# Iterate through directories and files
for root, dirs, files in os.walk(source_dir):
    for file in files:
        if file == "Inertial.csv":
            folder_name = os.path.basename(root)
            file_path = os.path.join(root, file)

            # Read CSV file
            df = pd.read_csv(file_path)

            # Create the plot
            fig, ax = plt.subplots(1, 2, figsize=(10, 6))
            ax.plot(df.iloc[:, 0], df.iloc[:,1])  # Replace 'Column1' and 'Column2' with actual column names
            ax.set_xlabel('X Axis Label')
            ax.set_ylabel('Y Axis Label')
            ax.set_title('CSV Data Plot')
            ax.set(title='Scroll to zoom, drag to pan', autoscale_on=False)
            ax.set_yscale('linear')
            ax.set_xscale('linear')
            ax.autoscale(tight=False)

            # Add the plot to the list
            plots.append(plt)

# Create a PDF file with all the plots
with PdfPages(output_pdf) as pdf:
    for plot in plots:
        pdf.savefig(plot.gcf(), bbox_inches='tight')

print(f'Plots saved to {output_pdf}.')

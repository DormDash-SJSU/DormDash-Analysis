import pandas as pd
import matplotlib.pyplot as plt

# Load the data from a CSV file
file_path = 'LiDAR data for accuracy - Sheet1.csv'
data = pd.read_csv(file_path)

# Create a plot to compare Actual Distance vs LiDAR Distance
plt.figure(figsize=(10, 6))
plt.plot(data['Measurement Number'], data['Actual Distance (cm)'], label='Actual Distance (cm)', marker='o')
plt.plot(data['Measurement Number'], data['LiDAR distance (cm)'], label='LiDAR Distance (cm)', marker='x')

# Add labels, title, and legend
plt.xlabel('Measurement Number')
plt.ylabel('Distance (cm)')
plt.title('LiDAR vs Actual Distance')
plt.legend()
plt.grid(True)
plt.savefig("lidar_plot1.svg")

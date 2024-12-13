import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
file_path = 'LiDAR data for accuracy - Sheet1.csv'
lidar_data = pd.read_csv(file_path)

# Calculate errors
lidar_data['Error (cm)'] = lidar_data['Actual Distance (cm)'] - lidar_data['LiDAR distance (cm)']
systematic_error = lidar_data['Error (cm)'].mean()  # Average error
random_error = lidar_data['Error (cm)'].std()      # Standard deviation of error

# Total measurements
total_measurements = lidar_data.shape[0]

# Plotting
fig, ax = plt.subplots(figsize=(8, 6))

# Create the bar chart
bar_labels = ['Systematic Error', 'Random Error']
bar_values = [systematic_error, random_error]
colors = ['mediumpurple', 'lightgreen']
ax.bar(bar_labels, bar_values, color=colors, edgecolor='black')

# Add labels to the bars
for i, value in enumerate(bar_values):
    ax.text(i, value + 0.1, f"{value:.2f} cm", ha='center', fontsize=10)

# Customize the plot
ax.set_title('LiDAR Performance Metrics', fontsize=16, weight='bold', pad=20)
ax.set_ylabel('Error (cm)', fontsize=12)
ax.set_ylim(0, max(bar_values) + 0.5)

# Add the total measurements outside the plot
fig.text(0.1, 0.91, f'Total Measurements: {total_measurements}', fontsize=12, weight='bold', ha='left')

# Adjust layout to prevent overlap
plt.tight_layout(rect=[0, 0, 1, 0.9])  # Reserve space at the top for the text
plt.savefig("lidar_plot2.svg")

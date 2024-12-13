import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
file_path = 'fps_analysis_20241210_230124.csv'
data = pd.read_csv(file_path)

# Convert timestamp to minutes starting from 0
data['timestamp'] = pd.to_datetime(data['timestamp'], unit='s')
data['minutes'] = (data['timestamp'] - data['timestamp'].min()).dt.total_seconds() / 60

# Plot 1: Frame Processing Rates with Error Bars
plt.figure(figsize=(12, 6))
plt.errorbar(data['minutes'], data['camera_fps'], yerr=data['camera_std'], fmt='-o', label='Camera FPS')
plt.errorbar(data['minutes'], data['detection_fps'], yerr=data['detection_std'], fmt='-o', label='Detection FPS', color='orange')

plt.title('Frame Processing Rate: Camera vs Detection')
plt.xlabel('Minutes from Start')
plt.ylabel('Frames Per Second (FPS)')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig("fps_plot1.svg")

# Plot 2: Standard Deviation Comparison
plt.figure(figsize=(12, 6))
plt.plot(data['minutes'], data['camera_std'], '-o', label='Camera FPS Std Dev')
plt.plot(data['minutes'], data['detection_std'], '-o', label='Detection FPS Std Dev', color='orange')

plt.title('Standard Deviation of Frame Processing Rate')
plt.xlabel('Minutes from Start')
plt.ylabel('Standard Deviation (FPS)')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig("fps_plot2.svg")

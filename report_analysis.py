# Analyze the data by calculating the mean and standard deviation for camera and detection performance
analysis = {
    "Camera Performance": {
        "Average Frame Rate (FPS)": data["camera_fps"].mean(),
        "Standard Deviation (FPS)": data["camera_std"].mean()
    },
    "Object Detection Performance": {
        "Average Processing Rate (FPS)": data["detection_fps"].mean(),
        "Standard Deviation Range (FPS)": (data["detection_std"].min(), data["detection_std"].max())
    }
}

analysis

#############

# Calculate statistics for LiDAR performance analysis
mean_actual = lidar_data["Actual Distance (cm)"].mean()
mean_measured = lidar_data["LiDAR distance (cm)"].mean()
systematic_error = mean_measured - mean_actual
percentage_error = (systematic_error / mean_actual) * 100
std_deviation = lidar_data["LiDAR distance (cm)"].std()
max_deviation = abs(lidar_data["LiDAR distance (cm)"] - mean_measured).max()
within_95 = (lidar_data["LiDAR distance (cm)"] - mean_measured).abs().le(0.5).sum() / len(lidar_data) * 100

lidar_analysis = {
    "Mean Measured Distance": mean_measured,
    "Mean Actual Distance": mean_actual,
    "Systematic Error (cm)": systematic_error,
    "Percentage Error": percentage_error,
    "Standard Deviation (cm)": std_deviation,
    "95% Measurements Within ±0.5 cm": within_95,
    "Maximum Observed Deviation (cm)": max_deviation
}

lidar_analysis

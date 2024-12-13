#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import CompressedImage
from darknet_ros_msgs.msg import BoundingBoxes
from collections import deque
import time
from statistics import mean, stdev
import csv
from datetime import datetime

class FPSAnalyzer(Node):
    def __init__(self, num_samples=100):
        super().__init__('fps_analyzer')
        
        # Number of samples to collect
        self.num_samples = num_samples
        self.current_samples = 0
        
        # Data storage
        self.data = []
        
        # Create subscribers
        self.camera_sub = self.create_subscription(
            CompressedImage,
            '/image_raw/compressed',  # Adjust topic name as needed
            self.camera_callback,
            10)
            
        self.detection_sub = self.create_subscription(
            BoundingBoxes,
            '/darknet_ros/bounding_boxes',  # Adjust topic name as needed
            self.detection_callback,
            10)
            
        # Timestamps for FPS calculation
        self.camera_timestamps = deque(maxlen=100)
        self.detection_timestamps = deque(maxlen=100)
        
        # Create timer for periodic FPS calculation
        self.timer = self.create_timer(5.0, self.calculate_fps)
        
        self.get_logger().info(f'FPS Analyzer initialized. Collecting {num_samples} samples...')
        
    def camera_callback(self, msg):
        self.camera_timestamps.append(time.time())
        
    def detection_callback(self, msg):
        self.detection_timestamps.append(time.time())
        
    def calculate_fps(self):
        if self.current_samples >= self.num_samples:
            return
            
        now = time.time()
        
        # Calculate camera FPS
        if len(self.camera_timestamps) > 1:
            camera_intervals = [j-i for i, j in zip(self.camera_timestamps, list(self.camera_timestamps)[1:])]
            camera_fps = 1.0 / mean(camera_intervals) if camera_intervals else 0
            camera_std = stdev(camera_intervals) if len(camera_intervals) > 1 else 0
        else:
            camera_fps = 0
            camera_std = 0
            
        # Calculate detection FPS
        if len(self.detection_timestamps) > 1:
            detection_intervals = [j-i for i, j in zip(self.detection_timestamps, list(self.detection_timestamps)[1:])]
            detection_fps = 1.0 / mean(detection_intervals) if detection_intervals else 0
            detection_std = stdev(detection_intervals) if len(detection_intervals) > 1 else 0
        else:
            detection_fps = 0
            detection_std = 0
            
        # Store the data
        sample_data = {
            'timestamp': now,
            'camera_fps': camera_fps,
            'camera_std': camera_std,
            'detection_fps': detection_fps,
            'detection_std': detection_std
        }
        
        self.data.append(sample_data)
        self.current_samples += 1
        
        # Print progress
        self.get_logger().info(
            f'Sample {self.current_samples}/{self.num_samples}\n'
            f'Camera FPS: {camera_fps:.2f} ± {camera_std:.2f}\n'
            f'Detection FPS: {detection_fps:.2f} ± {detection_std:.2f}\n'
        )
        
        # Check if we've collected enough samples
        if self.current_samples >= self.num_samples:
            self.save_data()
            rclpy.shutdown()

    def save_data(self):
        # Generate filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'fps_analysis_{timestamp}.csv'
        
        # Save to CSV
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['timestamp', 'camera_fps', 'camera_std', 'detection_fps', 'detection_std']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for sample in self.data:
                writer.writerow(sample)
                
        self.get_logger().info(f'Data saved to {filename}')

def main():
    rclpy.init()
    # Create the node with desired number of samples
    fps_analyzer = FPSAnalyzer(num_samples=20)  # Adjust number of samples as needed
    rclpy.spin(fps_analyzer)
    fps_analyzer.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

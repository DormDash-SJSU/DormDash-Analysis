import serial
import time
import csv
from datetime import datetime


class Lidar:
    def __init__(self, serial_port='/dev/ttyS0', baud_rate=115200):
        # Initialize serial communication
        try:
            self.ser = serial.Serial(serial_port, baud_rate)
            time.sleep(2)
            print(f"Connected to Lidar on {serial_port} at {baud_rate} baud")
        except serial.SerialException as e:
            print(f"Failed to connect to Lidar: {e}")
            self.ser = None

        self.data_buffer = []  # To store readings for 1 minute
        self.start_time = time.time()  # To track time for data collection
        
        # Store latest readings
        self.latest_distance = None
        self.latest_strength = None
        self.latest_temperature = None

    def read_data(self):
        if self.ser and self.ser.is_open:
            try:
                if self.ser.in_waiting > 8:
                    bytes_serial = self.ser.read(9)
                    self.ser.reset_input_buffer()
                    if bytes_serial[0] == 0x59 and bytes_serial[1] == 0x59:
                        distance = bytes_serial[2] + bytes_serial[3] * 256
                        strength = bytes_serial[4] + bytes_serial[5] * 256
                        temp = bytes_serial[6] + bytes_serial[7] * 256
                        temp = (temp / 8) - 256

                        if distance > 0:
                            # Store latest readings
                            self.latest_distance = distance
                            self.latest_strength = strength
                            self.latest_temperature = temp

                            # Add data to buffer
                            self.data_buffer.append({
                                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                'distance': distance,
                                'strength': strength,
                                'temperature': temp
                            })
                            
                            # Print current readings
                            print(f"Distance: {distance}mm, Strength: {strength}, Temperature: {temp}°C")
                        else:
                            print("Invalid distance data")
            except serial.SerialException as e:
                print(f"Serial communication error: {e}")

        # Check if 1 minute has elapsed
        if time.time() - self.start_time >= 60:
            self.save_to_csv()
            self.start_time = time.time()  # Reset timer
            self.data_buffer.clear()  # Clear buffer

    def save_to_csv(self):
        if not self.data_buffer:
            print("No data to save")
            return

        filename = f"lidar_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        try:
            with open(filename, 'w', newline='') as csvfile:
                fieldnames = ['timestamp', 'distance', 'strength', 'temperature']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writeheader()
                writer.writerows(self.data_buffer)

            print(f"Data saved to {filename}")
        except Exception as e:
            print(f"Failed to save data to CSV: {e}")

    def close(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
            print("Lidar connection closed")


def main():
    # Create Lidar instance with default or custom settings
    lidar = Lidar(serial_port='/dev/ttyS0', baud_rate=115200)
    
    try:
        print("Starting LIDAR data collection. Press Ctrl+C to stop...")
        while True:
            lidar.read_data()
            time.sleep(0.1)  # 100ms delay between readings
    except KeyboardInterrupt:
        print("\nStopping LIDAR data collection...")
    finally:
        lidar.close()


if __name__ == '__main__':
    main()

import struct
import datetime
import csv     
import argparse       

# define the format of the binary data file
# replace with actual format of the binary data file
fmt = 'lL?BBllllfffffffffffffffffBf'

data_size = struct.calcsize(fmt)
print(data_size) # DEBUG


def create_raw_dump(f, path="", filename="raw_data.csv"):
    with open(f, 'rb') as bin_file:
        # open a CSV file to write the data to
        with open(path+filename, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            # Write the header line to the CSV file
            writer.writerow(["Timestamp", "GPSYear", "GPSMonth", "GPSday", "GPSHour", "GPSMinute", "GPSSecond", "GPSHundredth", "voltage", "GPSFix", "numSats", "HDOP", "Latitude", "Longitude", "GPSSpeed", "GPSCourse", "sysCal", "gyroCal", "accelCal", "magCal", "rawAccelX", "rawAccelY", "rawAccelZ", "accelX", "accelY", "accelZ", "rawGyroX", "rawGyroY", "rawGyroZ", "gyroX", "gyroY", "gyroZ", "rawMagX", "rawMagY", "rawMagZ", "magX", "magY", "magZ", "roll", "pitch", "yaw", "linAccelX", "linAccelY", "linAccelZ", "quatW", "quatX", "quatY", "quatZ", "imuTemp", "state"])
            # Loop through the binary data file, unpacking the data and writing it to the CSV file
            while True:
                # Read the binary data
                binary_data = bin_file.read(data_size)
                if len(binary_data) < data_size: # Check if reached the end of the file
                    break
                # Unpack the binary data
                fields = struct.unpack(fmt, binary_data)
                # Format the timestamp into ISO8601
                dt = datetime.datetime.fromtimestamp(fields[0] + (fields[1] / 1000))
                fields = (dt.isoformat(),) + fields[1:]
                # Write the fields to the CSV file
                writer.writerow(str(field) for field in fields)


def create_gps_dump(f, path="", filename="gps_data.csv"):
    with open(f, 'rb') as bin_file:
        # open a CSV file to write the data to
        with open(path+filename, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            # Write the header line to the CSV file
            writer.writerow(["Timestamp", "GPSYear", "GPSMonth", "GPSday", "GPSHour", "GPSMinute", "GPSSecond", "GPSHundredth", "voltage", "GPSFix", "numSats", "HDOP", "Latitude", "Longitude", "GPSSpeed", "GPSCourse"])
            # Loop through the binary data file, unpacking the data and writing it to the CSV file
            while True:
                # Read the binary data
                binary_data = bin_file.read(data_size)
                if len(binary_data) < data_size: # Check if reached the end of the file
                    break
                # Unpack the binary data
                fields = struct.unpack(fmt, binary_data)
                # Format the timestamp into ISO8601
                dt = datetime.datetime.fromtimestamp(fields[0] + (fields[1] / 1000))
                fields = (dt.isoformat(),) + fields[1:]
                # Write the fields to the CSV file
                writer.writerow(str(field) for field in fields[:15])


def create_imu_dump(f, path="", filename="imu_data.csv"):
    with open(f, 'rb') as bin_file:
        # open a CSV file to write the data to
        with open(path+filename, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            # Write the header line to the CSV file
            writer.writerow(["Timestamp", "sysCal", "gyroCal", "accelCal", "magCal", "rawAccelX", "rawAccelY", "rawAccelZ", "accelX", "accelY", "accelZ", "rawGyroX", "rawGyroY", "rawGyroZ", "gyroX", "gyroY", "gyroZ", "rawMagX", "rawMagY", "rawMagZ", "magX", "magY", "magZ", "linAccelX", "linAccelY", "linAccelZ"])
            # Loop through the binary data file, unpacking the data and writing it to the CSV file
            while True:
                # Read the binary data
                binary_data = bin_file.read(data_size)
                if len(binary_data) < data_size: # Check if reached the end of the file
                    break
                # Unpack the binary data
                fields = struct.unpack(fmt, binary_data)
                print(fields)
                # Format the timestamp into ISO8601
                dt = datetime.datetime.fromtimestamp(fields[0] + (fields[1] / 1000))
                fields = (dt.isoformat(),) + fields[17:39] + fields[42:45]
                # Write the fields to the CSV file
                writer.writerow(str(field) for field in fields)

def create_ahrs_dump(f, path="", filename="ahrs_data.csv"):
    with open(f, 'rb') as bin_file:
        # open a CSV file to write the data to
        with open(path+filename, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            # Write the header line to the CSV file
            writer.writerow(["Timestamp", "roll", "pitch", "yaw", "quatW", "quatX", "quatY", "quatZ"])
            # Loop through the binary data file, unpacking the data and writing it to the CSV file
            while True:
                # Read the binary data
                binary_data = bin_file.read(data_size)
                if len(binary_data) < data_size: # Check if reached the end of the file
                    break
                # Unpack the binary data
                fields = struct.unpack(fmt, binary_data)
                # Format the timestamp into ISO8601
                dt = datetime.datetime.fromtimestamp(fields[0] + (fields[1] / 1000))
                fields = (dt.isoformat(),) + fields[39:42] + fields[45:49]
                # Write the fields to the CSV file
                writer.writerow(str(field) for field in fields)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('binary_log', type=str, help='The binary log file to parse')
    parser.add_argument('-t', '--output_types', nargs='+', default=['raw'],
                        choices=['raw', 'gps', 'imu', 'ahrs'],
                        help='The types of output files to generate. \n -\'raw\' will output the entire decoded log file, \n -\'gps\' will output only the GPS-specific data, \n-\'imu\' will output only IMU-specific data, \n -\'ahrs\' will output only attitude-specific data.')
    parser.add_argument('-p', '--path', type=str, default="", help='Path to the log file')

    args = parser.parse_args()

    if 'raw' in args.output_types:
        create_raw_dump(args.binary_log, path=args.path)
    if 'gps' in args.output_types:
        create_gps_dump(args.binary_log, path=args.path)
    if 'imu' in args.output_types:
        create_imu_dump(args.binary_log, path=args.path)
    if 'ahrs' in args.output_types:
        create_ahrs_dump(args.binary_log, path=args.path)

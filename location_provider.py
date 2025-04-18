# location_provider.py

import serial
import pynmea2
import random
import time

class GPSReader:
    def __init__(self, port='/dev/ttyS0', baudrate=9600, timeout=1):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial_conn = None
        self._setup_serial()

    def _setup_serial(self):
        try:
            self.serial_conn = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
            time.sleep(2)  # Wait for GPS to initialize
        except serial.SerialException as e:
            print("GPS not available:", e)

    def read_from_gps(self):
        if not self.serial_conn:
            return None
        try:
            line = self.serial_conn.readline().decode('ascii', errors='replace')
            if line.startswith('$GPGGA') or line.startswith('$GPRMC'):
                return line
        except Exception as e:
            print("Error reading GPS:", e)
        return None

    def parse_gps_data(self, nmea_sentence):
        try:
            msg = pynmea2.parse(nmea_sentence)
            lat = msg.latitude
            lon = msg.longitude
            return lat, lon
        except Exception as e:
            print("Failed to parse GPS:", e)
            return None, None

# -- ACTIVE LOCATION USED IN APP --
lat = f"17.52{random.randint(1000, 9999)}{random.randint(1000, 9999)}"
lon = f"78.36{random.randint(1000, 9999)}{random.randint(1000, 9999)}"

# For debug/testing only
if __name__ == "__main__":
    gps = GPSReader()
    raw = gps.read_from_gps()
    if raw:
        lat_real, lon_real = gps.parse_gps_data(raw)
        print("Real GPS:", lat_real, lon_real)
    print("Using fallback location:", lat, lon)

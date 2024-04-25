import serial


class SerialReader:
    def __init__(self, port, baudrate, timeout_in_seconds):
        self.ser = serial.Serial(port, baudrate,timeout=timeout_in_seconds)

    def read_data(self):
        # Read data from serial port
        data = (self.ser.readline())

        data = data.decode('utf-8')

        data = data.strip()

        data = data.split(",")

        return data

    def close(self):
        self.ser.close()

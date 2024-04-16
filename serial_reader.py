import serial


class SerialReader:
    def __init__(self, port, baudrate):
        self.ser = serial.Serial(port, baudrate)

    def read_data(self):
        # Read data from serial port (replace with error handling if needed)
        data = (self.ser.readline())

        data = data.decode('utf-8')

        data = data.strip()

        data = data.split(",")

        return data

    def close(self):
        self.ser.close()

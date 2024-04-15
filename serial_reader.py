import serial


class SerialReader:
    def __init__(self, port, baudrate):
        self.ser = serial.Serial(port, baudrate)

    def read_data(self):
        # Read data from serial port (replace with error handling if needed)
        data = self.ser.readline().decode('utf-8').strip()
        sensorValue = int(data)
        return sensorValue

    def close(self):
        self.ser.close()

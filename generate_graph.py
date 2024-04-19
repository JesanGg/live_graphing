import sys

import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from serial_reader import SerialReader

# Define serial port and baud rate
port = 'COM10'  # Replace with your port name
baudrate = 9600  # Baudrate from Arduino IDE flash

# Initialize data storage (replace with your data type if needed)
x = []  # Change for desired data - x_voltage, y_voltage...
y = []
y_2 = []


def animate(i):

    # Check if figure is closed
    if not (plt.fignum_exists(1)):
        Exit()

    # Read data from serial port
    try:  # Assign serial data to 2 variables
        voltage, current = SerialReader.read_data()
    except serial.SerialException:  # If serial has been closed by previous "if not"
        return 0

    # Update data lists
    x.append(i)
    y.append(float(voltage))
    y_2.append(float(current))

    # Update the plot data
    line.set_xdata(x)
    line.set_ydata(y)
    line2.set_xdata(x)
    line2.set_ydata(y_2)

    # Axis limit - also dynamic after 300 samples / ~3s
    plt.ylim([min(y_2) - .5, max(y) + .5])

    # Graph is expanding for first 300 samples
    if max(x) < 300:
        plt.xlim([0, max(x)+1])
        return line, line2,

    # Graph size is constant after 300 samples
    plt.xlim([max(x) - 300, max(x)])
    return line, line2,


def Exit():  # Exit animation without infinite loop
    plt.close()
    SerialReader.close()


# Open serial connection
SerialReader = SerialReader(port, baudrate)  # Create a serial reader object

fig, ax = plt.subplots()

# Create the line object
line, = ax.plot([], [], label='Sensor Data')
line2, = ax.plot([], [], label='Sensor Data')

# Add labels and title
ax.set_xlabel('Time (or Sample)')
ax.set_ylabel('Sensor Reading')  # ***************************************VOLTAGE CURRENT?
ax.set_title('Live Sensor Data Plot')


# Animate the plot - Need to stop loop after figure is closed
anim = animation.FuncAnimation(fig, animate, interval=1, cache_frame_data=False, blit=False)

plt.legend()

plt.show()


# Close serial connection
SerialReader.close()

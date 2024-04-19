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
x_2 = []
y_2 = []


def animate(i):
    # Check if figure is closed
    if not (plt.fignum_exists(1)):
        Exit()

    # Read data from serial port
    try:  # Assign serial data to 2 variables
        voltage, current = SerialReader.read_data()
        print(voltage, current)
    except serial.SerialException:  # If serial has been closed by previous "if not"
        return 0

    # Update data lists
    x.append(i)
    y.append(float(voltage))

    """
    power calcs
    # x_2.append(float(current))
    # y_2.append(float(current)*0.08)
    """

    x_2.append(i)
    y_2.append(float(current))  # Actually voltage currently

    # Update the plot data
    line.set_xdata(x)
    line.set_ydata(y)

    line2.set_xdata(x_2)
    line2.set_ydata(y_2)

    # Axis limit - also dynamic after 300 samples / ~3s
    ax1.set_ylim([min(y) - .5, max(y) + .5])

    ax2.set_ylim([min(y_2) - .5, max(y_2) + .5])
    ax2.set_xlim([0, max(x_2)])

    # Graph is expanding for first 300 samples
    if max(x) < 300:
        ax1.set_xlim([0, max(x) + 1])
        return line, line2

    # Graph size is constant after 300 samples
    ax1.set_xlim([max(x) - 300, max(x)])

    return line, line2


def Exit():  # Exit animation without infinite loop
    plt.close()
    SerialReader.close()


# Open serial connection
SerialReader = SerialReader(port, baudrate, 2)  # Create a serial reader object

fig, (ax1, ax2) = plt.subplots(1, 2)

# Create the line object
line, = ax1.plot([], [], label='Voltage')
line2, = ax2.plot([], [], label='Power')

# Add labels and title
ax1.set_xlabel('Time (or Sample)')
ax1.set_ylabel('Voltage')  # ***************************************VOLTAGE CURRENT?
ax1.set_title('Live Sensor Data Plot')

ax2.set_xlabel('Time (or Sample)')
ax2.set_ylabel('Current')  # ***************************************VOLTAGE CURRENT?
ax2.set_title('Sensor Current Data Plot')

# Animate the plot - Need to stop loop after figure is closed
anim = animation.FuncAnimation(fig, animate, interval=1, cache_frame_data=False, blit=False)

plt.legend()

plt.show()

# Close serial connection
SerialReader.close()

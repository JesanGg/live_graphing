import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from serial_reader import SerialReader
import datetime
import time  # Timing functions to see time cost

# Define serial port and baud rate
port = 'COM10'  # Replace with your port name
baudrate = 115200  # Baudrate from Arduino IDE flash

# Initialize data storage
voltage_x = []
voltage_y = []
power_x = []  # Change for desired data - x_voltage, y_voltage...
power_y = []


def animate(i):
    # Check if figure is closed
    if not (plt.fignum_exists(1)):
        Exit()

    # start_time = time.perf_counter()

    # Read data from serial port
    try:  # Assign serial data to 2 variables
        voltage, current = SerialReader.read_data()
        # print(voltage, current)
    except serial.SerialException:  # If serial has been closed by previous "if not"
        return 0
    except ValueError:  # If nothing is sent
        voltage = 0, 0

    if i % 100 == 0:  # Write every 100 samples
        f.write(f"{i},{voltage},{current}\n")

    # Update data lists
    try:
        voltage_x.append(i)
        voltage_y.append(float(voltage))
    except ValueError:  # If nothing is sent
        voltage = 0
        voltage_y.append(float(voltage))

    """
    power calcs
    # x_2.append(float(current))
    # y_2.append(float(current)*0.08)
    """

    power_x.append(i)
    power_y.append(float(current))  # Actually voltage currently

    # Update the plot data
    line.set_xdata(voltage_x)
    line.set_ydata(voltage_y)

    line2.set_xdata(power_x)
    line2.set_ydata(power_y)

    # Axis limit - also dynamic after 300 samples / ~3s
    ax2.set_ylim([min(power_y) - .5, max(power_y) + .5])

    try:
        ax2.set_xlim([0, max(power_x)])
    except UserWarning:
        ax2.set_xlim([0, 5])  # First few plots have no readings but not big deal.

    # Graph is expanding for first 300 samples
    if max(voltage_x) < 300:
        ax1.set_xlim([0, max(voltage_x) + 1])
        ax1.set_ylim([min(voltage_y) - .5, max(voltage_y) + .5])
        return line, line2

    # Graph size is constant after 300 samples
    ax1.set_ylim([min(voltage_y[-300:]) - .5, max(voltage_y[-300:]) + .5])
    ax1.set_xlim([max(voltage_x) - 300, max(voltage_x)])

    # # Calculate frame time in milliseconds
    # frame_time = (time.perf_counter() - start_time) * 1000
    #
    # # Print or store frame time for analysis (optional)
    # print(f"Frame {i} time: {frame_time:.2f} ms")

    return line, line2


def Exit():  # Exit animation without infinite loop
    plt.close()
    SerialReader.close()
    f.close()


# Open serial connection
SerialReader = SerialReader(port, baudrate, 2)  # Create a serial reader object

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 8))

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

# Get current date and time for unique filename
now = datetime.datetime.now()
unique_filename = f"live_data_{now.strftime('%Y-%m-%d_%H-%M-%S')}.txt"

f = open(unique_filename, "w")
f.write("i,voltage,current\n")

# Animate the plot - Need to stop loop after figure is closed
anim = animation.FuncAnimation(fig, animate, interval=1, cache_frame_data=False, blit=False)

# plt.legend()
#
plt.show()

f.close()

# Close serial connection
SerialReader.close()

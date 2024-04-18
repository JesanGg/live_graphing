import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from serial_reader import SerialReader

# Define serial port and baud rate
port = 'COM10'  # Replace with your port name
baudrate = 9600

# Initialize data storage (replace with your data type if needed)
x = []
y = []
y_2 = []


def animate(i):
    try:
        # Read data from serial port (replace with error handling)
        print(i)

        voltage, current = SerialReader.read_data()  # Returns string list of length 2

        # Update data lists
        x.append(i)  # Replace with timestamp if needed
        y.append(float(voltage))
        y_2.append(float(current))

        # Update the plot data
        line.set_xdata(x)
        line.set_ydata(y)
        line2.set_xdata(x)
        line2.set_ydata(y_2)

        # Optional: Set axis limits for efficiency
        plt.xlim([0, max(x) - 1])  # Adjust as needed
        plt.ylim([min(y_2) - .5, max(y) + .5])  # Adjust as needed

        return line, line2,

    except serial.SerialException as e:
        print(f"Error reading serial port: {e}")
        return line, line2,  # Keep the plot running even on errors


# Open serial connection (moved inside the animation loop)
SerialReader = SerialReader(port, baudrate)  # Create a serial reader object

window_closed = False

fig, ax = plt.subplots()

# Create the line object
line, = ax.plot([], [], label='Sensor Data')
line2, = ax.plot([], [], label='Sensor Data')

# Add labels and title
ax.set_xlabel('Time (or Sample)')  # Replace with appropriate label
ax.set_ylabel('Sensor Reading')
ax.set_title('Live Sensor Data Plot')

print("preanimate")

# Animate the plot
anim = animation.FuncAnimation(fig, animate, interval=5, cache_frame_data=False, blit=True)

print("show")

plt.legend()
plt.show()

# Close serial connection (optional)
SerialReader.close()

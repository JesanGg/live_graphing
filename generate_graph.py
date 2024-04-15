from itertools import count
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from serial_reader import SerialReader

port = "COM10"
baudrate = 9600

x_vals = []
y_vals = []


def animate(i):
    sensorValue = SerialReader.read_data()

    x_vals.append(i)
    y_vals.append(sensorValue)

    line.set_xdata(x_vals)
    line.set_ydata(y_vals)

    plt.xlim([0, len(x_vals) - 1])
    plt.ylim([min(y_vals), max(y_vals) + 10])

    return line,


reader = SerialReader(port, baudrate)  # Create a serial reader object

fig, ax = plt.subplots()

# Create the line object
line, = ax.plot([], [], label='Sensor Data')

# Add labels and title
ax.set_xlabel('Time (or Sample)')  # Replace with appropriate label
ax.set_ylabel('Sensor Reading')
ax.set_title('Live Sensor Data Plot')

# Animate the plot
anim = FuncAnimation(fig, animate, frames=100, interval=20, blit=True)

plt.legend()
plt.show()

reader.close()  # Close serial connection

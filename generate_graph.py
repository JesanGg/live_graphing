import serial
import random as rand
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Define serial port and baud rate
port = 'COM10'  # Replace with your port name
baudrate = 9600

# Initialize data storage (replace with your data type if needed)
x = []
y = []

def animate(i):
  try:
    # Read data from serial port (replace with error handling)

    data = ser.readline()

    data = data.decode("utf-8")

    data = data.strip()

    sensorValue = int(data)


    # Update data lists
    x.append(i)  # Replace with timestamp if needed
    y.append(sensorValue)

    # Update the plot data
    line.set_xdata(x)
    line.set_ydata(y)

    # Optional: Set axis limits for efficiency
    plt.xlim([0, len(x) - 1])  # Adjust as needed
    plt.ylim([min(y), max(y) + 10])  # Adjust as needed

    return line,

  except serial.SerialException as e:
    print(f"Error reading serial port: {e}")
    return line,  # Keep the plot running even on errors

# Open serial connection (moved inside the animation loop)
ser = serial.Serial(port, baudrate)

fig, ax = plt.subplots()

# Create the line object
line, = ax.plot([], [], label='Sensor Data')

# Add labels and title
ax.set_xlabel('Time (or Sample)')  # Replace with appropriate label
ax.set_ylabel('Sensor Reading')
ax.set_title('Live Sensor Data Plot')



# Animate the plot
anim = animation.FuncAnimation(fig, animate, interval=50, cache_frame_data=False, blit=True)



plt.legend()
plt.show()

# Close serial connection (optional)
ser.close()

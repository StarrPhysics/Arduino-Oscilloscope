import serial # https://pyserial.readthedocs.io/en/latest/pyserial.html
import random
import json
import time
from multiprocessing import Process, Queue
import re
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import numpy as np
import datetime

class queueDataStructure():
        pinData: dict
        miscData: dict

        def __init__(self, pinData: dict, miscelaneousData: dict):
            self.pinData = pinData
            self.miscData = miscelaneousData

# Async Function for Reading Serial Port
def openSerialPortStream(queue: Queue) -> None:
    
    lastRecordedTime: float = 0

    ser = serial.Serial()
    ser.port = 'COM3'
    ser.baudrate = 9600
    ser.open()
    print(ser.name)
    ser.flushInput()

    while ser.in_waiting == 0: # Empties Queue for latest value
        continue
    
    while True:
        loopStartTime = datetime.datetime.now()

        try:
            # Read the data from the serial port
            # Incoming data example: '{"A0": "1.23", "A1": "1.35"}'
            pinData = json.loads(re.sub("\\r+|\s+|\\n+", "", ser.readline().decode('utf-8'))) 
            
        except UnicodeDecodeError:
            continue
        
        while not queue.empty(): # Empty the queue for the latest data
                _ = queue.get()

        processingTime      = float((datetime.datetime.now() - loopStartTime).microseconds*1e-6) # Seconds
        processingFrequency = 1.0 / processingTime # Hertz

        queue.put(queueDataStructure(pinData, {'processingTime': processingTime, 'processingFrequency': processingFrequency}))

# The following functions interact with Matplotlib.animation in order to create the display
# They are the consumers in the queue pipeline.

# Function which initializes the structure of 'APinRecord' in order
# to be ready for furthur incoming data from the serial port.
def init():
    for pinName, pinValue in inialData.pinData.items():
        print()
        line2D, = display.plot([0], [pinValue])
        line2D.set_label(pinName)
        pinData[pinName] = line2D
    
    # https://matplotlib.org/stable/api/_as_gen/matplotlib.lines.Line2D.html
    # Needed for operations on line2Ds ^^^
    return pinData

def animate(i, queue: Queue):
    serialData: queueDataStructure = queue.get()
    global timeDataPoints

    timeDataPoints.append(round(timeDataPoints[-1] + serialData.miscData['processingTime'] * 1000, 2))
    
    if len(timeDataPoints) > 25:
        timeDataPoints = timeDataPoints[1:]

    for pinName, Line2D in pinData.items():
        voltageDataPoints = np.append(Line2D.get_data()[1], serialData.pinData[pinName])

        if len(voltageDataPoints) > 25:
            voltageDataPoints = voltageDataPoints[1:]
        
        display.set_xlim(min(timeDataPoints), max(timeDataPoints))
        display.set_ylim(0, 5)
        display.legend(loc="upper right")

        pinData[pinName].set_data(timeDataPoints, voltageDataPoints)
    print(f'Loop {i}')
    
    return pinData
# Function which initalizes some important global variables (in its own subprocess scope)
# and sets up the basic properties of the plot.
def beginAnimation(queue: Queue):
    global fig, display, pinData, inialData, timeDataPoints

    inialData= queue.get()

    pinData = {}
    timeDataPoints = [0]

    style.use('fivethirtyeight')

    fig     = plt.figure()
    display = fig.add_subplot(1,1,1)
    display.set_title('Arduino Serial Plotter')

    processingInterval = int(round(inialData.miscData['processingTime'] * 1000, 1)) # Milliseconds

    ani = animation.FuncAnimation(fig, animate, fargs=(queue,), interval=10, init_func=init, blit=False, cache_frame_data=False)
    plt.show()


# Main
if __name__=='__main__':
    serialDataQueue = Queue(maxsize=1)

    p1 = Process(target = openSerialPortStream, args=(serialDataQueue,))
    p1.start()
    p2 = Process(target = beginAnimation, args=(serialDataQueue,))
    p2.start()

    p1.join()
    p2.join()

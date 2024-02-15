import serial # https://pyserial.readthedocs.io/en/latest/pyserial.html
from serial.tools.list_ports import comports as getPortInfo
from serial.tools.list_ports_common import ListPortInfo

import random
import os
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

    avaliablePorts: list[ListPortInfo] = getPortInfo()

    print('Scanning Ports...')
    for portInfo in avaliablePorts:
            if (manufacturer := portInfo.manufacturer) == None:
                continue
                
            if manufacturer.find('Arduino') >= 0:
                print('Found Arduino Port!')
                serialPortStream(portInfo, queue)
                return
    print('No Arduino Port Found')    
    exit(0)
    
    while True:
        loopStartTime = datetime.datetime.now()

        try:
            # Read the data from the serial port
            # Incoming data example: '{"A0": "1.23", "A1": "1.35"}'
            pinData = json.loads(re.sub("\\r+|\s+|\\n+", "", ser.readline().decode('utf-8'))) 
        except UnicodeDecodeError:
            continue
        

        processingTime      = float((datetime.datetime.now() - loopStartTime).microseconds*1e-6) # Seconds
        processingFrequency = 1.0 / processingTime # Hertz

        queue.put(queueDataStructure(pinData, {'processingTime': processingTime, 'processingFrequency': processingFrequency}))

def serialPortStream(portInfo: ListPortInfo, queue: Queue) -> None:
    print(f'Attempting to connect to port "{portInfo.device}"...')
    ser = serial.Serial()
    ser.port = portInfo.device

    ser.baudrate = 9600
    ser.open()
    #ser.flushInput()
    print(f'Connected to port "{portInfo.device}"!')


    while True:
        
        

    """
    #ser.flushInput()

    while True:
        print('_______')
        print(ser.in_waiting)
        if ser.in_waiting > 0:
            x = ' '.join(format(ord(x), 'b') for x in ser.readline().decode('utf-8'))
            print(x)
        #print(s)
        
        #ser.write(b'Testing 1 2 3')
    """

# The following functions interact with Matplotlib.animation in order to create the display
# They are the consumers in the queue pipeline.


# Function which initalizes some important global variables (in its own subprocess scope)
# and sets up the basic properties of the plot.
def beginAnimation(queue: Queue):
    style.use('fivethirtyeight')
    fig     = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.set_title('Arduino Serial Plotter')

    serialData: queueDataStructure = queue.get()
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 5)

    artists: list[plt.Line2D] = [
         ax.plot(
                np.arange(0,1,1/50),
                [Voltage]*50,
                label=pinName,
                #color = 'blue' if simObject.isStatic else 'red',
                linewidth = 1
                )[0]
    for (pinName, Voltage) in serialData.pinData.items()]

    ax.legend(loc="upper right")

    def animate(i):
        serialData = queue.get()
        for artist in artists:
            voltage = serialData.pinData[artist.get_label()]
            
            y = artist.get_ydata()

            y[i % 50] = voltage

            artist.set_ydata(y)
        return artists

    ani = animation.FuncAnimation(fig, animate, interval=0, blit=True, cache_frame_data=False)
    plt.show()

# Main
if __name__=='__main__':
    
    serialDataQueue = Queue(maxsize=1)
    
    p1 = Process(target = openSerialPortStream, args=(serialDataQueue,))
    p1.start()
    
    #p2 = Process(target = beginAnimation, args=(serialDataQueue,))
    #p2.start()

    p1.join()
    #p2.join()
        

    

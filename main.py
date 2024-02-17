from multiprocessing import Process, Queue
import serial_utils
import plot_utils

# Main
if __name__=='__main__':
    queue = Queue(maxsize=1)
    
    serialProcess = Process(target = serial_utils.main, args=(queue,))
    serialProcess.start()
    
    plotterProcess = Process(target = plot_utils.main, args=(queue,))
    plotterProcess.start()

    serialProcess.join()
    plotterProcess.join()
        

    
"""
# Modules
import serial # https://pyserial.readthedocs.io/en/latest/pyserial.html
import random
import os
import sys
import json
import time
from typing import Union

import re
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import numpy as np
import datetime
"""
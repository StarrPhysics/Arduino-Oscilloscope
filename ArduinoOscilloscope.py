"""
Please execute the `run()` function in this file to start the oscilloscope program.
"""
from multiprocessing import Process, Queue, freeze_support
import serial_utils
import plot_utils

def run(*, baud: int = 9600, wrap_limit = 50, save: bool = False, filename: str = 'oscilloscope') -> None:
    """
    Runs the Arduino Oscilloscope program.
    
    # Parameters
        baud (int): The baud rate for serial communication. Default is 9600.

        wrap_limit: The maximum number of data points to display on the plot before wrapping around. Default is 50.

        save (bool): Flag indicating whether to save the plot as an image file. Default is False.

        filename (str): The name of the image file to save. Default is 'oscilloscope'.
    """

    queue = Queue(maxsize=1)
    
    serialProcess = Process(target = serial_utils.main, args=(queue,baud))
    serialProcess.start()
    
    plotterProcess = Process(target = plot_utils.main, args=(queue,wrap_limit))
    plotterProcess.start()

    serialProcess.join()
    plotterProcess.join()


# Main
if __name__=='__main__':
    run(save=True, filename='test')
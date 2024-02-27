from multiprocessing import Queue
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import numpy as np

def animate(i, 
            queue: Queue, 
            wrap_limit: int, 
            artists: list[plt.Line2D], 
            lastArtistIndex: list[int]
        ) -> list[plt.Line2D]:
        """
        This function is called by the `FuncAnimation` object to update the plot with new data.
        The way that data is displayed on the plot is irregular compared to traditional methods.
        Instead of appending new data to an artists's x and y data, the data is overwritten on these values in a circular/modular fashion.
        
        """
        serialDataArray = queue.get()

        for pin_index_id, voltage in serialDataArray:
            artist      = artists[pin_index_id]
            lastIndex   = lastArtistIndex[pin_index_id]
            y = artist.get_ydata()
            y[i % wrap_limit] = voltage
            artist.set_ydata(y)

            lastIndex += 1
            
        return artists

def main(queue: Queue, 
         wrap_limit: int, 
         # save: bool,  Saving files is not implemented yet.
         # filename: str
        ) -> None:
    """
    The main function for the `plot_utils.py` file, which establishes the plot's runtime.

    Args:
        queue (Queue)       -> Contains a reference to the multiprocessing queue, which is used to communicate between the `serial_utils.py` and `plot_utils.py` processes.
        
        wrap_limit (int)    -> The number of data points to be displayed on the plot before the plot wraps around and starts overwriting the first data point.
    """

    # Initalize plot elements and properties
    style.use('fivethirtyeight')
    fig     = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.set_title('Arduino Oscilloscope')
    ax.set_xlim(0, 1)
    ax.set_ylim(-.1, 5.1)
    ax.get_xaxis().set_visible(False)
    
    while queue.empty(): pass  # Waits for initalization data to be avaliable, which contains the pin names.
    
    initalizationData = queue.get() # Aquires the list of pin names from the queue.

    lastArtistIndex = [0]* len(initalizationData) # The index of the last data point for each pin.

    artists: list[plt.Line2D] = [ # Creates a unique artist in the `artists` list for each pin name.
         ax.plot(
                np.arange(0,1,1/wrap_limit),
                [0.0]*wrap_limit,
                label=pinName,
                linewidth = 1,
                )[0] for pinName in initalizationData]

    ax.legend(loc="upper right")
    
    # Establishes animation
    ani = animation.FuncAnimation(fig, animate, fargs=(queue,wrap_limit,artists, lastArtistIndex), interval=1, blit=True, cache_frame_data=False)
    plt.show()
    queue.close()
    
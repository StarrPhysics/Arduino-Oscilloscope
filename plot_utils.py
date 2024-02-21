from multiprocessing import Queue
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import numpy as np
import random

def animate(i, queue: Queue, artists: list[plt.Line2D]):

        serialDataArray = queue.get()

        print(serialDataArray)

        for artist in artists:
            
            y = artist.get_ydata()
            y[i % 50] = random.uniform(0.0, 5.0)
            artist.set_ydata(y)
            
        return artists

def main(queue: Queue):
    style.use('fivethirtyeight')
    fig     = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.set_title('Arduino Oscilloscope')

    # Wait for the data to be ready
    while queue.empty(): pass

    initalizationData = queue.get()
    
    ax.set_xlim(0, 1)
    ax.get_xaxis().set_visible(False)
    ax.set_ylim(-.1, 5.1)

    artists: list[plt.Line2D] = [
         ax.plot(
                np.arange(0,1,1/50),
                [0.0]*50,
                label=pinName,
                #color = 'blue' if simObject.isStatic else 'red',
                linewidth = 1
                )[0]

    for pinName in initalizationData]

    ax.legend(loc="upper right")

    ani = animation.FuncAnimation(fig, animate, fargs=(queue,artists), interval=1, blit=True, cache_frame_data=False)

    plt.show()



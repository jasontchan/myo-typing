import multiprocessing
import queue
import numpy as np
import mpl_toolkits.mplot3d as plt3d
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.cm import get_cmap

from pyomyo import Myo, emg_mode

print("Press ctrl+pause/break to stop")

# ------------ Myo Setup ---------------
# q = multiprocessing.Queue()


# ------------ Plot Setup ---------------
QUEUE_SIZE = 100
SENSORS = 8
subplots = []
lines = []
# Set the size of the plot
plt.rcParams["figure.figsize"] = (4, 8)
# using the variable axs for multiple Axes
fig, subplots = plt.subplots(SENSORS, 1)
fig.canvas.manager.set_window_title("8 Channel EMG plot")
fig.tight_layout()
# Set each line to a different color

name = "tab10"  # Change this if you have sensors > 10
cmap = get_cmap(name)  # type: matplotlib.colors.ListedColormap
colors = cmap.colors  # type: list

for i in range(0, SENSORS):
    (ch_line,) = subplots[i].plot(
        range(QUEUE_SIZE), [0] * (QUEUE_SIZE), color=colors[i]
    )
    lines.append(ch_line)

emg_queue = queue.Queue(QUEUE_SIZE)


def animate(i, *fargs):
    # Myo Plot
    q = fargs[0]
    while not (q.empty()):
        myox = list(q.get())
        if emg_queue.full():
            emg_queue.get()
        emg_queue.put(myox)

    channels = np.array(emg_queue.queue)

    if emg_queue.full():
        for i in range(0, SENSORS):
            channel = channels[:, i]
            lines[i].set_ydata(channel)
            subplots[i].set_ylim(0, max(1024, max(channel)))


def run(q):

    print("RUNNIGN RUN FUNC")
    while q.empty():
        # print("q is empty in run func")
        # Wait until we actually get data
        continue
    print("q is not empty anym,ore")
    anim = animation.FuncAnimation(fig, animate, blit=False, interval=2, fargs=(q,))
    print("animation func made")

    def on_close(event):
        raise KeyboardInterrupt
        print("On close has ran")

    fig.canvas.mpl_connect("close_event", on_close)

    try:
        print("try plt.show")
        plt.show()
        print("after show")
    except KeyboardInterrupt:
        plt.close()
        quit()


if __name__ == "__main__":
    run()

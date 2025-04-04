# from pyomyo import Myo, emg_mode
import sys

sys.path.append("../")  # Add parent directory to path
from pyomyo_main.src.pyomyo.pyomyo import Myo, emg_mode
import time

# ------------ Myo Setup ---------------
MODE = emg_mode.RAW


def worker(q, mac, tty):
    print("MAC", mac, flush=True)
    m = Myo(mode=MODE, tty=tty)
    m.connect(input_address=mac)

    def add_to_queue(emg, movement):
        curr_time = (time.time(),)
        emg = emg + curr_time
        print("EMG TUPLE", emg)
        q.put(emg)

    m.add_emg_handler(add_to_queue)

    # Orange logo and bar LEDs
    m.set_leds([128, 128, 0], [128, 128, 0])
    # Vibrate to know we connected okay
    m.vibrate(1)

    """worker function"""
    while True:
        m.run()
    print("Worker Stopped")

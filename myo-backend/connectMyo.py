from pyomyo import Myo, emg_mode

# ------------ Myo Setup ---------------
MODE = emg_mode.PREPROCESSED


def worker(q):
    m = Myo(mode=MODE)
    m.connect()

    def add_to_queue(emg, movement):
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

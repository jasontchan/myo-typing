import threading
import matplotlib

matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.cm import get_cmap
import multiprocessing
import time
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

from pynput import keyboard
from pynput.keyboard import Controller, Key
import h5py
import numpy as np
import json

import os
import sys
import shutil
import queue

# import connection scripts
from connectMyo import worker

from collections import defaultdict

import mpl_toolkits.mplot3d as plt3d
from mpl_toolkits.mplot3d import Axes3D

from functools import partial

DATA_STORAGE = "temp/"

# ------------ Plot Setup ---------------
QUEUE_SIZE = 100
SENSORS = 16
subplots = []
lines = []
# Set the size of the plot
plt.rcParams["figure.figsize"] = (8, 16)
# using the variable axs for multiple Axes
fig, subplots = plt.subplots(SENSORS, 1, sharex=True)
fig.canvas.manager.set_window_title("16 Channel EMG plot")
fig.tight_layout()
plt.subplots_adjust(wspace=0, hspace=0)
# Set each line to a different color

name = "seismic"
cmap = get_cmap(name)  # type: matplotlib.colors.ListedColormap
colors = [cmap(i / (SENSORS - 1)) for i in range(SENSORS)]
colors.reverse()
# colors = cmap.colors  # type: list

for i in range(0, SENSORS):
    (ch_line,) = subplots[i].plot(
        range(QUEUE_SIZE), [0] * (QUEUE_SIZE), color=colors[i]
    )
    lines.append(ch_line)

emg_queue = queue.Queue(QUEUE_SIZE)
vertical_queue = queue.Queue(QUEUE_SIZE)

drawn_events = set()
vertical_events = []
sample_count = 0


def animate(i, q):
    global sample_count
    # Myo Plot
    # current_offset = time.time() - start_time.value
    while not (key_q.empty()):
        event = key_q.get()
        if event not in drawn_events:
            drawn_events.add(event)
            timestamp, character = event
            event_sample = sample_count
            event_x_initial = QUEUE_SIZE - 1
            event_lines = []
            for i, ax in enumerate(subplots):
                line = ax.axvline(
                    x=event_x_initial, color="black", linestyle="solid", linewidth=1
                )
                event_lines.append(line)
                if i == 0:
                    y_min, y_max = ax.get_ylim()
                    text_y = y_max - (y_max - y_min) * 0.1
                    text_obj = ax.text(
                        timestamp,
                        text_y,
                        character if character != "Key.space" else "_",
                        verticalalignment="center",
                        horizontalalignment="right",
                        fontsize=32,
                        color="black",
                    )
            vertical_events.append(
                {
                    "sample_index": event_sample,
                    "character": character,
                    "lines": event_lines,
                    "text": text_obj,
                }
            )

    while not (q.empty()):
        myox = list(q.get())
        sample_count += 1
        if emg_queue.full():
            emg_queue.get()
        emg_queue.put(myox)

    current_sample = sample_count
    left_bound = current_sample - QUEUE_SIZE + 1

    events_to_remove = []
    for event in vertical_events:
        x_visible = event["sample_index"] - left_bound
        if x_visible < 0 or x_visible > QUEUE_SIZE - 1:
            for i in range(len(event["lines"])):
                event["lines"][i].remove()
            event["text"].remove()
            events_to_remove.append(event)

        else:
            for l in event["lines"]:
                l.set_xdata([x_visible, x_visible])
            current_text_pos = event["text"].get_position()
            event["text"].set_position((x_visible, current_text_pos[1]))

    for event in events_to_remove:
        vertical_events.remove(event)

    channels = np.array(emg_queue.queue)

    if emg_queue.full():
        for i in range(0, SENSORS):
            channel = channels[:, i]
            lines[i].set_ydata(channel)
            subplots[i].set_ylim(-127, 128)
            subplots[i].spines[["top", "bottom", "right"]].set_visible(False)
            subplots[i].yaxis.set_visible(False)
            if i != SENSORS - 1:
                subplots[i].xaxis.set_visible(False)

    # for (timestamp, character), objects in vertical_event_objects.items():
    #     new_x = timestamp
    #     for line in objects[0]:
    #         line.set_xdata(new_x)
    #     text_obj = objects[1]
    #     y_min, y_max = subplots[-1].get_ylim()
    #     text_y = y_max - (y_max - y_min)*0.1
    #     text_obj.set_position((new_x, text_y))


def run(q, start_time):
    while q.empty():
        # print("q is empty in run func")
        # Wait until we actually get data
        continue
    start_time.value = time.time()
    anim = animation.FuncAnimation(fig, partial(animate, q=q), blit=False, interval=2)

    def on_close(event):
        sys.exit(0)
        print("On close has ran")

    fig.canvas.mpl_connect("close_event", on_close)

    try:
        print("try plt.show")
        plt.show()
        print("after show")
    except KeyboardInterrupt:
        plt.close()
        quit()


def start_flask(start_time):
    app = Flask(__name__)
    # CORS(app, origins=["http://localhost:3000"])
    CORS(app, resources={r"/*": {"origins": "*"}})
    app.config["CORS_HEADERS"] = "Content-Type"

    q_l = multiprocessing.Queue()
    q_r = multiprocessing.Queue()

    # q_r_vis = multiprocessing.Queue()

    p_l = None
    p_r = None

    p_vis_l = None
    p_vis_r = None

    manager = None
    # recording = None
    p_recording = None
    recording = multiprocessing.Value("i", 0)

    # [start time, end time, 'k']
    def create_listener(key_log):
        global key_q

        key_start_times = defaultdict(int)
        key_start_times["Key.enter"] = time.time()  # edge case

        def on_press(key):
            try:
                key_name = key.char
            except AttributeError:
                key_name = str(key)

            key_start_times[key_name] = time.time()
            if key_name not in ("Key.enter", "Key.backspace", "Key.esc"):
                key_q.put((float(time.time()) - float(start_time.value), key_name))

        def on_release(key):
            try:
                key_name = key.char
            except AttributeError:
                key_name = str(key)
            if key == Key.esc:
                return False
            # record this as a key release
            key_log.append([key_start_times[key_name], time.time(), key_name])

        return keyboard.Listener(on_press=on_press, on_release=on_release)

    def recording_worker(q_l, q_r, recording):
        global q
        print("RECORDING API HIT", flush=True)
        full_data_l = []
        full_data_r = []
        keystrokes = []
        listener = create_listener(keystrokes)
        listener.start()
        keyboard = Controller()
        while recording.value:
            while not (q_l.empty() or q_r.empty()):
                # data_l = ['One', 'Two', 'Three', "Four", "Five", "Six", "Seven", "Eight", "Time"]
                get_q_l = q_l.get()
                get_q_r = q_r.get()
                data_l = list(get_q_l)
                # print("data_l", data_l)
                data_r = list(get_q_r)
                # print("data_r", data_r)
                full_data_l.append(data_l)
                full_data_r.append(data_r)
                q.put(get_q_l[:-1] + get_q_r[:-1])
                # q_r_vis.put(get_q_r)
                # print("q on my side", q_r_vis)

            # print("recording.value is still 1")

        if not recording.value:
            # save data
            keyboard.press(Key.esc)
            keyboard.release(Key.esc)
            listener.join()
            print(keystrokes)
            with h5py.File(
                "temp/stream.h5",
                "w",
            ) as f:
                f.create_dataset("left_emg", data=full_data_l)
                f.create_dataset("right_emg", data=full_data_r)
                string_dt = h5py.string_dtype(encoding="utf-8")
                dt = np.dtype(
                    [("time1", np.float64), ("time2", np.float64), ("key", string_dt)]
                )
                keystroke_data = np.array([tuple(row) for row in keystrokes], dtype=dt)
                f.create_dataset("keystrokes", data=keystroke_data)

        print("ENDED THE START API")

    @app.route("/create-folder", methods=["POST"])
    @cross_origin()
    def create_folder():
        global DATA_STORAGE
        data = request.get_json()
        if not data:
            return jsonify({"message": "no data"}), 400
        os.makedirs("../data/" + str(data), exist_ok=True)
        DATA_STORAGE = "../data/" + str(data) + "/"

        return jsonify({"success": True}), 200

    @app.route("/start-connection", methods=["GET"])
    @cross_origin()
    def start_connection():
        global p_l, p_r
        # L_MAC = [16, 68, 221, 232, 61, 253] left
        # R_MAC = [193, 174, 37, 33, 189, 206] right
        L_MAC = [176, 102, 48, 60, 192, 228]
        R_MAC = [67, 145, 190, 132, 38, 228]

        p_l = multiprocessing.Process(
            target=worker,
            args=(q_l, L_MAC, "/dev/ttyACM1"),
        )
        p_l.start()

        p_r = multiprocessing.Process(
            target=worker,
            args=(q_r, R_MAC, "/dev/ttyACM2"),
        )
        p_r.start()

        # p_vis_l = multiprocessing.Process(
        #     target=run, args=(q,)
        # )
        # p_vis_l.start()

        return jsonify({"success": True}), 200

    @app.route("/start-recording", methods=["GET"])
    @cross_origin()
    def start_recording():
        global p_recording
        if not recording.value:
            recording.value = 1
            p_recording = multiprocessing.Process(
                target=recording_worker,
                args=(q_l, q_r, recording),
            )
            p_recording.start()
            print("STARTED RECORDING END OF API", flush=True)
            return jsonify({"success": True}), 200
        else:
            print("start recording already in progress", flush=True)
            return jsonify({"success": False, "message": "already recording"}), 200

    @app.route("/end-recording", methods=["GET"])
    @cross_origin()
    def end_recording():
        global p_recording, p_l, p_r, p_vis_l
        if recording.value:
            recording.value = 0
            p_recording.join()
            p_l.join()
            p_r.join()
            p_vis_l.join()
            print("END RECORDING API HIT", flush=True)
            return jsonify({"success": True}), 200
        else:
            print("here")
            return (
                jsonify({"success": False, "message": "no recording was ever started"}),
                200,
            )

    @app.route("/save-metadata", methods=["POST"])
    @cross_origin()
    def save_metadata():
        data = request.get_json()
        if not data:
            return jsonify({"message": "no data"}), 400

        print(data)
        with open(
            DATA_STORAGE + "metadata.json",
            "w",
        ) as file:
            json.dump(data, file, indent=4)

        # move stream data to folder
        shutil.move(
            "temp/stream.h5",
            DATA_STORAGE + "stream.h5",
        )
        print("DATA STORAGE IS", DATA_STORAGE)

        return jsonify({"success": True}), 200

    app.run(debug=True, port=5001, use_reloader=False)


if __name__ == "__main__":

    q = multiprocessing.Queue()
    key_q = multiprocessing.Queue()
    start_time = multiprocessing.Value("d", time.time())
    flask_thread = threading.Thread(target=start_flask, args=(start_time,), daemon=True)
    flask_thread.start()
    run(q, start_time)

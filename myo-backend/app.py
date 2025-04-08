import multiprocessing
import time
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

from pynput import keyboard
from pynput.keyboard import Controller, Key
import h5py
import numpy as np
import json

# import connection scripts
from connectMyo import worker

from collections import defaultdict

app = Flask(__name__)
# CORS(app, origins=["http://localhost:3000"])
CORS(app, resources={r"/*": {"origins": "*"}})
app.config["CORS_HEADERS"] = "Content-Type"


DATA_STORAGE = "../data/jason_2025-4-8/"
SESSION_NUMBER = 1


q_l = multiprocessing.Queue()
q_r = multiprocessing.Queue()


p_l = None
p_r = None

manager = None
# recording = None
p_recording = None
recording = multiprocessing.Value("i", 0)


# [start time, end time, 'k']
def create_listener(key_log):

    key_start_times = defaultdict(int)
    key_start_times["Key.enter"] = time.time()  # edge case

    def on_press(key):
        try:
            key_name = key.char
        except AttributeError:
            key_name = str(key)

        key_start_times[key_name] = time.time()

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
            data_l = list(q_l.get())
            print("data_l", data_l)
            data_r = list(q_r.get())
            print("data_r", data_r)
            full_data_l.append(data_l)
            full_data_r.append(data_r)
        # print("recording.value is still 1")

    if not recording.value:
        # save data
        keyboard.press(Key.esc)
        keyboard.release(Key.esc)
        listener.join()
        print(keystrokes)
        with h5py.File(
            DATA_STORAGE + "stream_" + str(SESSION_NUMBER) + ".h5", "w"
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


@app.route("/start-connection", methods=["GET"])
@cross_origin()
def start_connection():
    global p_l, p_r
    L_MAC = [16, 68, 221, 232, 61, 253]
    R_MAC = [193, 174, 37, 33, 189, 206]

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
    global p_recording, p_l, p_r
    if recording.value:
        recording.value = 0
        p_recording.join()
        p_l.join()
        p_r.join()
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
    print("HI")
    data = request.get_json()
    if not data:
        return jsonify({"message": "no data"}), 400

    print(data)
    with open(DATA_STORAGE + "metadata_" + str(SESSION_NUMBER) + ".json", "w") as file:
        json.dump(data, file, indent=4)  # indent makes the json more readable
    return jsonify({"success": True}), 200


if __name__ == "__main__":

    app.run(debug=True, port=5001, use_reloader=False)

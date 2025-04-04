import multiprocessing

# import time
from flask import Flask, jsonify
from flask_cors import CORS, cross_origin

# import keyboard
# import h5py

# import connection scripts
from connectMyo import worker

app = Flask(__name__)
# CORS(app, origins=["http://localhost:3000"])
CORS(app, resources={r"/*": {"origins": "*"}})
app.config["CORS_HEADERS"] = "Content-Type"

q_l = multiprocessing.Queue()
q_r = multiprocessing.Queue()


@app.route("/start-connection", methods=["GET"])
@cross_origin()
def start_connection():
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
    print("RECORDING API HIT", flush=True)
    carryOn = True
    full_data_l = []
    full_data_r = []
    while carryOn:
        while not (q_l.empty() and q_r.empty()):
            # data_l = ['One', 'Two', 'Three', "Four", "Five", "Six", "Seven", "Eight", "Time"]
            data_l = list(q_l.get())
            print("data_l", data_l)
            data_r = list(q_r.get())
            full_data_l.append(data_l)
            full_data_r.append(data_r)
        # at some point, set carryOn to false (when the frontend is done)

    # if not carryOn:
    #     # save data
    #     pass
    return jsonify({"success": True}), 200


if __name__ == "__main__":
    app.run(debug=True, port=5001)

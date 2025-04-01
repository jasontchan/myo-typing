import multiprocessing
from flask import Flask, jsonify

# import connection scripts
from connectMyo import worker

app = Flask(__name__)


@app.route("/start-connection", methods=["GET"])
def start_connection():
    q = multiprocessing.Queue()
    p = multiprocessing.Process(
        target=worker,
        args=(q,),
    )
    p.start()


if __name__ == "__main__":
    app.run(port=5000)

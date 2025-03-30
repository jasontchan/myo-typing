from flask import Flask, jsonify

# import connection scripts

app = Flask(__name__)


@app.route("/start-recording", methods=["GET"])
def start_recording():
    return


if __name__ == "__main__":
    app.run()

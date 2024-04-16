from flask import Flask, jsonify, render_template
import serial
from flask_cors import CORS
import threading
import time

app = Flask(__name__)
CORS(app)

# In-memory storage for roll and pitch data
orientation_data = {"roll": 0, "pitch": 0}

# Serial port configuration
ser = serial.Serial("COM7", 9600)  # Modify the port and baud rate as per your setup

@app.route("/")
def home():
    return render_template("index.html")

def read_serial_data():
    global orientation_data
    while True:
        try:
            # Assuming data is sent as comma-separated values: roll,pitch
            data = ser.readline().decode().strip().split(',')
            roll = float(data[0])
            pitch = float(data[1])
            orientation_data["roll"] = roll
            orientation_data["pitch"] = pitch
            print(f"Received: ({roll}, {pitch})")
        except Exception as e:
            print("Error reading serial data:", e)
        time.sleep(0.005)

# Starting a background thread to read serial data continuously
def start_background_thread():
    thread = threading.Thread(target=read_serial_data)
    thread.daemon = True  # Daemonize thread
    thread.start()

start_background_thread()

@app.route("/api/get-orientation-data/")
def get_orientation_data():
    return jsonify(orientation_data)

if __name__ == "__main__":
    # start_background_thread()
    app.run(debug=True, port=5000)

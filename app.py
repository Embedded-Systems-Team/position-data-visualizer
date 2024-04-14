from flask import Flask, jsonify, render_template, send_from_directory
import serial
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

# In-memory storage for roll and pitch data
orientation_data = {"roll": 0, "pitch": 0}

# Serial port configuration
ser = serial.Serial("COM6", 9600)  # Modify the port and baud rate as per your setup

@app.route("/")
def home():
    return render_template("index.html")

def read_serial_data():
    global orientation_data
    try:
        # Assuming data is sent as comma-separated values: roll,pitch
        data = ser.readline().decode().strip().split(',')
        roll = float(data[0])
        pitch = float(data[1])
        orientation_data["roll"] = roll
        orientation_data["pitch"] = pitch
    except Exception as e:
        print("Error reading serial data:", e)

@app.route("/api/get-orientation-data/")
def get_orientation_data():
    read_serial_data()
    return jsonify(orientation_data)

# @app.route('/textures/<path:filename>')
# def send_texture(filename):
#     return send_from_directory('static/textures', filename)

# @app.route('/static/<path:path>')
# def send_static(path):
#     return send_from_directory('static', path)

if __name__ == "__main__":
    app.run(debug=True)

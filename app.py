from flask import Flask, jsonify, render_template
import serial

app = Flask(__name__)

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

if __name__ == "__main__":
    app.run(debug=True)

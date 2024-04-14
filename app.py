from flask import Flask, jsonify, render_template
import serial

app = Flask(__name__)

# In-memory storage for position data
position_data = {"x": 0, "y": 0, "z": 0}

# Serial port configuration
ser = serial.Serial('COM6', 9600)  # Modify the port and baud rate as per your setup

@app.route("/")
def home():
    return render_template("index.html")

# Method to read data from serial port
def read_serial_data():
    global position_data
    try:
        # Assuming data is sent as comma-separated values: x,y,z
        data = ser.readline().decode().strip().split(',')
        print(f"data={data}")
        x = float(data[0])
        y = float(data[1])
        z = float(data[2])
        print(f"Serial data: ({x}, {y}, {z})")
        position_data["x"] = x
        position_data["y"] = y
        position_data["z"] = z
    except Exception as e:
        print("Error reading serial data:", e)

# Route to update position data (optional)
@app.route("/update-position/")
def update_position():
    read_serial_data()
    return {"message": "Position data updated successfully"}

# Route to get position data
@app.route("/api/get-position-data/")
def get_position_data():
    read_serial_data()
    return jsonify(position_data)

if __name__ == "__main__":
    app.run(debug=True)

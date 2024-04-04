from flask import Flask, request, render_template_string, jsonify

app = Flask(__name__)

# In-memory storage for position data
position_data = {"x": 0, "y": 0, "z": 0, "time": "N/A"}

@app.route("/")
def home():
    return render_template_string("""
        <h1>Position Data Viewer</h1>
        <div id="positionData">
            <p><strong>X Position:</strong> <span id="xPos">0</span></p>
            <p><strong>Y Position:</strong> <span id="yPos">0</span></p>
            <p><strong>Z Position:</strong> <span id="zPos">0</span></p>
            <p><strong>Time:</strong> <span id="time">N/A</span></p>
        </div>
        <script>
            function fetchData() {
                fetch("/api/get-position-data/")
                    .then(response => response.json())
                    .then(data => {
                        document.getElementById("xPos").textContent = data.x;
                        document.getElementById("yPos").textContent = data.y;
                        document.getElementById("zPos").textContent = data.z;
                        document.getElementById("time").textContent = data.time;
                    })
                    .catch(error => console.error("Error fetching data:", error));
            }

            // Fetch data every 0.5 seconds
            setInterval(fetchData, 500);

            // Fetch data immediately on page load
            fetchData();
        </script>
        """)


@app.route("/api/position-data/", methods=["POST"])
def update_position():
    global position_data
    data = request.json
    position_data["x"] = data.get("x", position_data["x"])
    position_data["y"] = data.get("y", position_data["y"])
    position_data["z"] = data.get("z", position_data["z"])
    position_data["time"] = data.get("time", position_data["time"])
    return {"message": "Position data updated successfully"}


@app.route("/api/get-position-data/")
def get_position_data():
    return jsonify(position_data)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)

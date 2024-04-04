from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

# In-memory storage for position data
position_data = {"x": 0, "y": 0, "z": 0}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/position-data/", methods=["POST"])
def update_position():
    global position_data
    data = request.json
    position_data["x"] = data.get("x", position_data["x"])
    position_data["y"] = data.get("y", position_data["y"])
    position_data["z"] = data.get("z", position_data["z"])
    return {"message": "Position data updated successfully"}

@app.route("/api/get-position-data/")
def get_position_data():
    return jsonify(position_data)

if __name__ == "__main__":
    app.run(debug=True)

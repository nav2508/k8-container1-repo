from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

# Define Persistent Volume storage path
PERSISTENT_STORAGE = "/Navya_PV_dir"

# Ensure the directory exists
os.makedirs(PERSISTENT_STORAGE, exist_ok=True)

# Store File API
@app.route('/store-file', methods=['POST'])
def store_file():
    data = request.get_json()

    # Validate JSON input
    if "file" not in data or "data" not in data:
        return jsonify({"file": None, "error": "Invalid JSON input."}), 400

    file_path = os.path.join(PERSISTENT_STORAGE, data["file"])

    try:
        # Write data to file
        with open(file_path, "w") as f:
            f.write(data["data"])
        return jsonify({"file": data["file"], "message": "Success."}), 200
    except Exception:
        return jsonify({"file": data["file"], "error": "Error while storing the file to the storage."}), 500

# Calculate API (Sends request to Container 2)
@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()

    # Validate JSON input
    if "file" not in data or "product" not in data:
        return jsonify({"file": None, "error": "Invalid JSON input."}), 400

    file_path = os.path.join(PERSISTENT_STORAGE, data["file"])

    # Check if file exists
    if not os.path.exists(file_path):
        return jsonify({"file": data["file"], "error": "File not found."}), 404

    # Send request to Container 2
    container2_url = "http://container2-service:5001/compute"
    response = requests.post(container2_url, json=data)

    return response.json(), response.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

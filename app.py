from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

# Define Persistent Volume storage path
PERSISTENT_STORAGE = "/Navya_PV_dir"

# Ensure the directory exists
os.makedirs(PERSISTENT_STORAGE, exist_ok=True)

print("Test log added")
# Store File API
@app.route('/store-file', methods=['POST'])
def store_file():
    data = request.get_json()

    # Validate JSON input
    if "file" not in data or "data" not in data:
        return jsonify({"file": None, "error": "Invalid JSON input."}), 400

    file_path = os.path.join(PERSISTENT_STORAGE, data["file"])

    try:
       
        lines = data["data"].split("\n")
        clean_lines = [",".join([col.strip() for col in line.split(",")]) for line in lines]

        # Write corrected CSV
        with open(file_path, "w") as f:
            f.write("\n".join(clean_lines))

        return jsonify({"file": data["file"], "message": "Success."}), 200

    except Exception:
        return jsonify({"file": data["file"], "error": "Error while storing the file to the storage."}), 500


# Calculate API (Sends request to Container 2)
# Calculate API (Sends request to Container 2)
@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    
    print(f" Incoming Request to /calculate: {data}")  
    
    if not data or not isinstance(data, dict):
        print(" No JSON body received!")
        return jsonify({"file": None, "error": "Invalid JSON input.", "sum": 0}), 400

    
    if "file" not in data or not isinstance(data["file"], str) or not data["file"].strip():
        print("Missing or empty file name!")  
        return jsonify({"file": None, "error": "Invalid JSON input.", "sum": 0}), 400

    if "product" not in data or not isinstance(data["product"], str) or not data["product"].strip():
        print("Missing or empty product name!")  
        return jsonify({"file": data["file"], "error": "Invalid JSON input.", "sum": 0}), 400

    file_name = data["file"].strip()
    product_name = data["product"].strip()
    file_path = os.path.join(PERSISTENT_STORAGE, file_name)

   
    if not os.path.exists(file_path):
        print(f" File Not Found: {file_path}")  
        return jsonify({"file": file_name, "error": "File not found.", "sum": 0}), 404

    
    container2_url = "http://container2-service:5001/compute"
    
    print(f"Sending Request to {container2_url}: {data}") 
    
    try:
        response = requests.post(container2_url, json={"file": file_name, "product": product_name})
        response_json = response.json()
        print(f"Response from Container2: {response.status_code}, {response_json}")  

        return response_json, response.status_code
    except Exception as e:
        print(f" Error sending request to Container2: {e}")  
        return jsonify({"file": file_name, "error": "Failed to connect to container2-service.", "sum": 0}), 500



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

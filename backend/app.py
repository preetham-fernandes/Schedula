from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route("/upload-files/", methods=["POST"])
def upload_files():
    file1 = request.files.get("file1")
    file2 = request.files.get("file2")

    if not file1 or not file2:
        return jsonify({"error": "Both files are required"}), 400

    # Read the content of the files
    file1_content = file1.read().decode('utf-8')
    file2_content = file2.read().decode('utf-8')

    # Process the files (dummy logic here)
    schedule = {"schedule": "Sample schedule data"}  # Replace with actual logic
    conflicts = "Sample conflicts"  # Replace with actual logic

    return jsonify({
        "schedule": schedule,
        "conflicts": conflicts
    })

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

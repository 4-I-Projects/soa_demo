from flask import Flask, jsonify, request

app = Flask(__name__)

# Fake data: student_id -> GPA
gpa_data = {
    "sv001": 3.75,
    "sv002": 2.8,
    "sv003": 1.9,
}

@app.route("/gpa/<student_id>")
def get_gpa(student_id):
    gpa = gpa_data.get(student_id, None)
    if gpa is None:
        return jsonify({"error": "Student not found"}), 404
    return jsonify({"student_id": student_id, "gpa": gpa})

@app.route("/gpa/<student_id>", methods=["POST"])
def update_gpa(student_id):
    data = request.get_json()
    gpa = data.get("gpa")
    if gpa is None:
        return jsonify({"error": "Missing GPA"}), 400
    gpa_data[student_id] = gpa
    return jsonify({"student_id": student_id, "gpa": gpa})

if __name__ == "__main__":
    app.run(port=5001, debug=True)

from flask import Flask, jsonify, request

app = Flask(__name__)

# Fake data: student_id -> conduct score
conduct_data = {
    "sv001": 95,
    "sv002": 72,
    "sv003": 40,
}

@app.route("/conduct/<student_id>")
def get_conduct(student_id):
    conduct = conduct_data.get(student_id, None)
    if conduct is None:
        return jsonify({"error": "Student not found"}), 404
    return jsonify({"student_id": student_id, "conduct": conduct})

@app.route("/conduct/<student_id>", methods=["POST"])
def update_conduct(student_id):
    data = request.get_json()
    conduct = data.get("conduct")
    if conduct is None:
        return jsonify({"error": "Missing conduct score"}), 400
    conduct_data[student_id] = conduct
    return jsonify({"student_id": student_id, "conduct": conduct})

if __name__ == "__main__":
    app.run(port=5002, debug=True)

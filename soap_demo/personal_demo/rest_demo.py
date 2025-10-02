from flask import Flask, jsonify, request

app = Flask(__name__)

# Fake data
users = [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]
posts = [{"id": 1, "title": "REST Intro"}, {"id": 2, "title": "Flask Demo"}]

# 1 + 2. Client-Server & Stateless
@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    token = request.headers.get("Authorization")
    if token != "Bearer secret-token":
        return jsonify({"error": "Unauthorized"}), 401
    user = next((u for u in users if u["id"] == user_id), None)
    return jsonify(user) if user else (jsonify({"error": "Not found"}), 404)

# 3. Cacheable
@app.route("/posts", methods=["GET"])
def get_posts():
    resp = jsonify(posts)
    resp.headers["Cache-Control"] = "public, max-age=60"  # cache 60s
    return resp

# 4. Uniform Interface (CRUD for users)
@app.route("/users", methods=["POST"])
def create_user():
    data = request.json
    new_id = len(users) + 1
    new_user = {"id": new_id, "name": data["name"]}
    users.append(new_user)
    return jsonify(new_user), 201

@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.json
    for u in users:
        if u["id"] == user_id:
            u["name"] = data["name"]
            return jsonify(u)
    return jsonify({"error": "Not found"}), 404

@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    global users
    users = [u for u in users if u["id"] != user_id]
    return "", 204

# 6. Code on Demand
@app.route("/script.js", methods=["GET"])
def send_script():
    js_code = "alert('Hello from REST API!');"
    return js_code, 200, {"Content-Type": "application/javascript"}

if __name__ == "__main__":
    app.run(port=5000, debug=True)

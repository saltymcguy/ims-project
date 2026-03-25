from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import bcrypt
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

def db_connect():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        passwd=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME", "warehouse"),
    )

@app.route("/")
def home():
    return "IMS API is running"

@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    try:
        db = db_connect()
    except Exception as e:
        return jsonify({"error": "Database connection failed"}), 500
    c = db.cursor(dictionary=True)
    c.execute("SELECT * FROM users WHERE username=%s", (data["username"],))
    user = c.fetchone()
    c.close(); db.close()
    if not user:
        return jsonify({"error": "User not found"}), 404
    if not bcrypt.checkpw(
    data["password"].encode(),
    user["password_hash"].encode() if isinstance(user["password_hash"], str) else user["password_hash"]):
        return jsonify({"error": "Invalid password"}), 401
    return jsonify({"user_id": user["user_id"], "username": user["username"], "role": user["role"]})

@app.route("/api/register", methods=["POST"])
def register():
    data = request.json
    try:
        db = db_connect()
    except Exception as e:
        return jsonify({"error": "Database connection failed"}), 500
    c = db.cursor(dictionary=True)
    c.execute("SELECT * FROM users WHERE username=%s", (data["username"],))
    if c.fetchone():
        c.close(); db.close()
        return jsonify({"error": "User already exists"}), 409
    hashed = bcrypt.hashpw(data["password"].encode(), bcrypt.gensalt()).decode()
    c.execute(
        "INSERT INTO users (username,password_hash,role) VALUES (%s,%s,%s)",
        (data["username"], hashed, "staff"),
    )
    db.commit()
    c.close(); db.close()
    return jsonify({"message": f"User '{data['username']}' registered successfully"}), 201

@app.route("/api/inventory", methods=["GET"])
def get_inventory():
    try:
        db = db_connect()
    except Exception as e:
        return jsonify({"error": "Database connection failed"}), 500
    c = db.cursor(dictionary=True)
    c.execute("SELECT * FROM inventory")
    items = c.fetchall()
    for item in items:
        if isinstance(item.get("last_updated"), datetime):
            item["last_updated"] = item["last_updated"].isoformat()
    c.close(); db.close()
    return jsonify(items)

@app.route("/api/inventory", methods=["POST"])
def add_item():
    data = request.json
    try:
        db = db_connect()
    except Exception as e:
        return jsonify({"error": "Database connection failed"}), 500
    c = db.cursor()
    c.execute(
        "INSERT INTO inventory (item_name,quantity,location) VALUES (%s,%s,%s)",
        (data["name"], data["quantity"], data["location"]),
    )
    db.commit()
    item_id = c.lastrowid
    _log(c, item_id, data["user_id"], "add", data["quantity"])
    c.close(); db.close()
    return jsonify({"message": "Item added", "item_id": item_id}), 201

@app.route("/api/inventory/<int:item_id>", methods=["PUT"])
def update_item(item_id):
    data = request.json
    try:
        db = db_connect()
    except Exception as e:
        return jsonify({"error": "Database connection failed"}), 500
    c = db.cursor()
    c.execute("UPDATE inventory SET quantity=%s WHERE item_id=%s", (data["quantity"], item_id))
    db.commit()
    _log(item_id, data["user_id"], "adjust", data["quantity"])
    c.close(); db.close()
    return jsonify({"message": "Quantity updated"})

@app.route("/api/inventory/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    data = request.json
    try:
        db = db_connect()
    except Exception as e:
        return jsonify({"error": "Database connection failed"}), 500
    c = db.cursor()
    _log(item_id, data["user_id"], "remove", 0)
    c.execute("DELETE FROM inventory WHERE item_id=%s", (item_id,))
    db.commit()
    c.close(); db.close()
    return jsonify({"message": "Item deleted"})

@app.route("/api/transactions", methods=["GET"])
def get_transactions():
    try:
        db = db_connect()
    except Exception as e:
        return jsonify({"error": "Database connection failed"}), 500
    c = db.cursor(dictionary=True)
    c.execute("""
        SELECT t.transaction_id, i.item_name, u.username,
               t.change_type, t.quantity_change, t.timestamp
        FROM transactions t
        JOIN inventory i ON t.item_id = i.item_id
        JOIN users u ON t.user_id = u.user_id
        ORDER BY t.timestamp DESC
    """)
    logs = c.fetchall()
    for log in logs:
        if isinstance(log.get("timestamp"), datetime):
            log["timestamp"] = log["timestamp"].isoformat()
    c.close(); db.close()
    return jsonify(logs) 

@app.route("/api/users", methods=["GET"])
def get_users():
    try:
        db = db_connect()
    except Exception as e:
        return jsonify({"error": "Database connection failed"}), 500
    c = db.cursor(dictionary=True)
    c.execute("SELECT user_id, username, role FROM users")
    users = c.fetchall()
    c.close(); db.close()
    return jsonify(users)

@app.route("/api/users/<int:user_id>/role", methods=["PUT"])
def change_role(user_id):
    data = request.json
    try:
        db = db_connect()
    except Exception as e:
        return jsonify({"error": "Database connection failed"}), 500
    c = db.cursor()
    c.execute("UPDATE users SET role=%s WHERE user_id=%s", (data["role"], user_id))
    db.commit()
    c.close(); db.close()
    return jsonify({"message": "Role updated"})

@app.route("/api/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    try:
        db = db_connect()
    except Exception as e:
        return jsonify({"error": "Database connection failed"}), 500
    c = db.cursor()
    c.execute("DELETE FROM users WHERE user_id=%s", (user_id,))
    db.commit()
    c.close(); db.close()
    return jsonify({"message": "User deleted"})

def _log(item_id, user_id, change_type, quantity_change):
    db = db_connect()
    c = db.cursor()
    c.execute(
        "INSERT INTO transactions (item_id, user_id, change_type, quantity_change) VALUES (%s, %s, %s, %s)",
        (item_id, user_id, change_type, quantity_change),
    )
    db.commit()
    c.close()
    db.close()
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

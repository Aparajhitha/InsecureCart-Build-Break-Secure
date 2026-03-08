from flask import Flask, request, jsonify
import sqlite3
import uuid
import bcrypt
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity
)

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "super-secret-key"

jwt = JWTManager(app)

# 🚨 Still insecure design (in-memory token)
active_tokens = {}

def get_db_connection():
    conn = sqlite3.connect("insecurecart.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def home():
    return {"message": "Welcome to InsecureCart API"}


# ----------------------------
# REGISTER (SQLi FIXED)
# ----------------------------
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data["username"]
    password = data["password"]

    # 🔐 Hash password
    hashed_password = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    )

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
        (username, hashed_password.decode("utf-8"), "user")
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "User registered successfully"})


# ----------------------------
# LOGIN (SQLi FIXED)
# ----------------------------
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data["username"]
    password = data["password"]

    conn = get_db_connection()
    cursor = conn.cursor()

    user = cursor.execute(
        "SELECT * FROM users WHERE username = ?",
        (username,)
    ).fetchone()

    conn.close()

    if user and bcrypt.checkpw(
    password.encode("utf-8"),
    user["password"].encode("utf-8")
    ):
        access_token = create_access_token(identity=str(user["id"]))

        return jsonify({
        "message": "Login successful",
        "access_token": access_token
        })

    else:
        return jsonify({"message": "Invalid credentials"}), 401

# ----------------------------
# ADD TO CART (SQLi FIXED)
# ----------------------------
@app.route("/cart/add", methods=["POST"])
def add_to_cart():
    data = request.get_json()

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO cart (user_id, product_id, quantity) VALUES (?, ?, ?)",
        (data["user_id"], data["product_id"], data["quantity"])
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Product added to cart"})


# ----------------------------
# VIEW CART (Authorization FIXED)
# ----------------------------
@app.route("/cart/<int:user_id>", methods=["GET"])
@jwt_required()
def view_cart(user_id):
    current_user = int(get_jwt_identity())

    if current_user != user_id:
        return jsonify({"error": "Forbidden"}), 403

    conn = get_db_connection()
    cursor = conn.cursor()

    items = cursor.execute(
        "SELECT * FROM cart WHERE user_id = ?",
        (user_id,)
    ).fetchall()

    conn.close()

    return jsonify([dict(item) for item in items])


# ----------------------------
# LIST USERS (SQLi FIXED BUT STILL BAD DESIGN)
# ----------------------------
@app.route("/users", methods=["GET"])
def list_users():
    username = request.args.get("username", "")

    conn = get_db_connection()
    cursor = conn.cursor()

    users = cursor.execute(
        "SELECT id, username, role FROM users WHERE username LIKE ?",
        (f"%{username}%",)
    ).fetchall()

    conn.close()

    return jsonify([dict(user) for user in users])


# ----------------------------
# CHECKOUT (Business Logic STILL FLAWED)
# ----------------------------
@app.route("/checkout", methods=["POST"])
def checkout():

    data = request.get_json()

    user_id = data["user_id"]
    product_id = data["product_id"]
    quantity = data["quantity"]

    # Business logic validation
    if quantity <= 0:
        return jsonify({"error": "Invalid quantity"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    product = cursor.execute(
        "SELECT price FROM products WHERE id = ?",
        (product_id,)
    ).fetchone()

    if not product:
        return jsonify({"error": "Product not found"}), 404

    price = product["price"]
    total = price * quantity

    conn.close()

    return jsonify({
        "user_id": user_id,
        "product_id": product_id,
        "quantity": quantity,
        "total_amount": total
    })


if __name__ == "__main__":
    app.run(debug=True)

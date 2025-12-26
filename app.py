from flask import Flask, render_template, request, jsonify
from database import get_db_connection, init_db
from predictor import predict_fraud

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register", methods=["POST"])
def register():
    username = request.form.get("username")
    password = request.form.get("password")

    if not username or not password:
        return "Missing username or password"

    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO users "
            "(username, password, balance) "
            "VALUES (?, ?, ?)",
            (username, password, 100000),
        )
        conn.commit()
    except Exception:
        conn.close()
        return "User already exists"
    conn.close()
    return "Success"


@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    if not username or not password:
        return "Missing username or password"

    conn = get_db_connection()
    cur = conn.cursor()
    user = cur.execute(
        "SELECT * FROM users "
        "WHERE username = ? AND password = ?",
        (username, password),
    ).fetchone()
    conn.close()

    if user:
        return "Success"
    return "Invalid login"


@app.route("/check", methods=["POST"])
def check_transaction():
    data = request.json
    sender = data.get("sender")
    receiver = data.get("receiver")
    amount = float(data.get("amount", 0))
    frequency = int(data.get("frequency", 0))

    status = predict_fraud(amount, frequency)

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO transactions "
        "(sender, receiver, amount, frequency, status) "
        "VALUES (?, ?, ?, ?, ?)",
        (sender, receiver, amount, frequency, status),
    )

    if status == "Safe":
        cur.execute(
            "UPDATE users "
            "SET balance = balance - ? "
            "WHERE username = ?",
            (amount, sender),
        )
        cur.execute(
            "UPDATE users "
            "SET balance = balance + ? "
            "WHERE username = ?",
            (amount, receiver),
        )

    conn.commit()
    conn.close()
    return jsonify({"status": status})


@app.route("/wallets")
def wallets():
    conn = get_db_connection()
    users = conn.execute(
        "SELECT username, balance FROM users"
    ).fetchall()
    conn.close()
    return jsonify({u["username"]: u["balance"] for u in users})


@app.route("/transactions")
def transactions():
    conn = get_db_connection()
    txns = conn.execute(
        "SELECT * FROM transactions ORDER BY id DESC"
    ).fetchall()
    conn.close()
    return jsonify([dict(row) for row in txns])


if __name__ == "__main__":
    init_db()
    app.run(debug=True)









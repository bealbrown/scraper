from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)
DATABASE_FILENAME = "names.db"


def get_db_connection():
    conn = sqlite3.connect(DATABASE_FILENAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    conn.execute("""CREATE TABLE IF NOT EXISTS names (id INTEGER PRIMARY KEY, name TEXT NOT NULL)""")

    names = ["Alice", "Bob", "Charlie", "Diana"]
    conn.executemany("INSERT INTO names (name) VALUES (?)", [(name,) for name in names])

    conn.commit()
    conn.close()


@app.route("/get_name", methods=["GET"])
def get_name():
    conn = get_db_connection()
    name = conn.execute("SELECT name FROM names LIMIT 1").fetchone()
    conn.close()
    if name:
        return jsonify({"name": name["name"]})
    else:
        return jsonify({"message": "No names left"}), 404


@app.route("/name_finished", methods=["POST"])
def name_finished():
    if not request.json or "name" not in request.json:
        return jsonify({"error": "Bad request, name is required"}), 400

    name = request.json["name"]
    conn = get_db_connection()
    result = conn.execute("DELETE FROM names WHERE name = ?", (name,)).rowcount
    conn.commit()
    conn.close()
    if result > 0:
        return jsonify({"message": f"{name} removed"}), 200
    else:
        return jsonify({"error": "Name not found"}), 404


if __name__ == "__main__":
    init_db()  # Initialize the database and table
    app.run(debug=True)

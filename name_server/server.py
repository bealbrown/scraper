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
    # Check if the table already exists
    cursor = conn.cursor()
    cursor.execute("""SELECT name FROM sqlite_master WHERE type='table' AND name='names';""")
    exists = cursor.fetchone()

    # Create the table if it doesn't exist
    conn.execute("""CREATE TABLE IF NOT EXISTS names (id INTEGER PRIMARY KEY, name TEXT NOT NULL)""")

    # If the table didn't exist, add initial names
    if not exists:
        add_initial_names(conn)

    conn.commit()
    conn.close()


def add_initial_names(conn):
    try:
        with open("input_names.txt", "r") as file:
            names = [(line.strip(),) for line in file if line.strip()]
        conn.executemany("INSERT INTO names (name) VALUES (?)", names)
        conn.commit()
    except FileNotFoundError:
        print("The file 'input_names.txt' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


@app.route("/get_name", methods=["GET"])
def get_name():
    conn = get_db_connection()
    # Start a transaction
    conn.execute("BEGIN")
    try:
        # Fetch the first name and then put it at the end of the db, so other servers don't get it also
        name_row = conn.execute("SELECT id, name FROM names ORDER BY id LIMIT 1").fetchone()
        if name_row:
            name = name_row["name"]
            # Delete the fetched name
            conn.execute("DELETE FROM names WHERE id = ?", (name_row["id"],))
            # Re-insert the name at the end
            conn.execute("INSERT INTO names (name) VALUES (?)", (name,))
            # Commit the changes
            conn.commit()
            return jsonify({"name": name})
        else:
            # Rollback if no name was found
            conn.rollback()
            return jsonify({"message": "No names left"}), 404
    except Exception as e:
        # Rollback in case of any error
        conn.rollback()
        return jsonify({"error": "An error occurred while processing the name"}), 500
    finally:
        conn.close()


@app.route("/name_finished", methods=["POST"])
def name_finished():
    if not request.json or "name" not in request.json:
        return jsonify({"error": "Bad request, name is required"}), 400

    name = request.json["name"]
    conn = get_db_connection()

    print("removing", name, "which was completed")
    result = conn.execute("DELETE FROM names WHERE name = ?", (name,)).rowcount
    conn.commit()
    conn.close()
    if result > 0:
        return jsonify({"message": f"{name} removed"}), 200
    else:
        return jsonify({"error": "Name not found"}), 404


if __name__ == "__main__":
    init_db()  # Initialize the database and table
    app.run(host="0.0.0.0", port=80, debug=True)

import os
import time

import psycopg2
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        database=os.getenv("DB_NAME", "tasksdb"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "postgres"),
        port=os.getenv("DB_PORT", "5432")
    )


def initialize_database():
    for attempt in range(10):
        try:
            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id SERIAL PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    completed BOOLEAN DEFAULT FALSE
                );
            """)

            cursor.execute("SELECT COUNT(*) FROM tasks;")
            count = cursor.fetchone()[0]

            if count == 0:
                cursor.execute("""
                    INSERT INTO tasks (title, completed)
                    VALUES
                    ('Learn AWS', TRUE),
                    ('Deploy application to EKS', FALSE);
                """)

            connection.commit()
            cursor.close()
            connection.close()

            print("Database initialized successfully.")
            return

        except Exception as error:
            print(f"Database connection attempt {attempt + 1}/10 failed: {error}")
            time.sleep(3)

    raise RuntimeError("Could not connect to PostgreSQL.")


@app.route("/")
def home():
    return jsonify({
        "application": "Cloud-Native Task API",
        "status": "running"
    })


@app.route("/health")
def health():
    try:
        connection = get_connection()
        connection.close()

        return jsonify({
            "status": "healthy",
            "database": "connected"
        })

    except Exception as error:
        return jsonify({
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(error)
        }), 500


@app.route("/tasks")
def get_tasks():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, title, completed
        FROM tasks
        ORDER BY id;
    """)

    rows = cursor.fetchall()

    tasks = [
        {
            "id": row[0],
            "title": row[1],
            "completed": row[2]
        }
        for row in rows
    ]

    cursor.close()
    connection.close()

    return jsonify(tasks)


if __name__ == "__main__":
    initialize_database()
    app.run(host="0.0.0.0", port=5000)

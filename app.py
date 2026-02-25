import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allows your frontend to communicate with this API

DB_FILE = 'database.db'

def init_db():
    """Creates the database and table if they don't exist."""
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS comments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                comment TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
    print("Database initialized.")

# --- API ROUTES ---

@app.route('/comment', methods=['POST'])
def add_comment():
    data = request.get_json()
    
    # Simple Validation
    name = data.get('name')
    comment = data.get('comment')
    
    if not name or not comment:
        return jsonify({"error": "Name and comment are required"}), 400

    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO comments (name, comment) VALUES (?, ?)", 
                (name, comment)
            )
            conn.commit()
        return jsonify({"message": "Comment added successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/comment', methods=['GET'])
def get_comments():
    try:
        with sqlite3.connect(DB_FILE) as conn:
            conn.row_factory = sqlite3.Row  # Allows us to access columns by name
            cursor = conn.cursor()
            # Fetch all, newest first
            cursor.execute("SELECT * FROM comments ORDER BY created_at DESC")
            rows = cursor.fetchall()
            
            # Convert rows to a list of dictionaries
            comments = [dict(row) for row in rows]
            
        return jsonify(comments), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    init_db()  # Ensure table exists before starting
    app.run(debug=True, port=5000)
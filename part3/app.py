from flask import Flask, request, jsonify, render_template, send_from_directory
import mysql.connector
import os

app = Flask(__name__, template_folder='')
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = '272004'
DB_NAME = 'todo_app'

def ensure_database_exists():
    """
    Checks if the database exists. If it doesn't, creates it, the tables, and inserts initial data.
    """
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()

        # Check if the database exists
        cursor.execute("SHOW DATABASES")
        databases = [db[0] for db in cursor.fetchall()]
        if DB_NAME in databases:
            print(f"Database '{DB_NAME}' already exists.")
        else:
            print(f"Database '{DB_NAME}' not found. Creating database...")
            # cursor.execute(f"CREATE DATABASE {DB_NAME}")
            # cursor.execute(f"USE {DB_NAME}")
            
            # Read the SQL script
            with open('create_db.sql', 'r') as file:
                sql_script = file.read()
            
            # Execute the script (split by ';' for multiple commands)
            for statement in sql_script.split(';'):
                if statement.strip():
                    cursor.execute(statement)
            print(f"Database '{DB_NAME}' and tables created successfully with initial data.")
        # Ensure that data is inserted even if the table exists
        conn.database = DB_NAME
        cursor.execute("SELECT COUNT(*) FROM todo")
        if cursor.fetchone()[0] == 0:  # If the table is empty
            cursor.executemany(
                "INSERT INTO todo (description, status) VALUES (%s, %s)",
                [
                    ('SS1 Assignment 1', 'Done'),
                    ('SS1 Assignment 2', 'Doing'),
                    ('SS1 Final', 'Doing')
                ]
            )
            conn.commit()
            print("Initial data inserted into 'todo' table.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()


db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '272004',
    'database': 'todo_app'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<path:filename>')
def serve_static_file(filename):
    return send_from_directory(os.getcwd(), filename)

@app.route('/api/list', methods=['GET'])
def api_list():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM todo ORDER BY id DESC")
    todo_list = cursor.fetchall()
    conn.close()
    return jsonify(todo_list)

@app.route('/api/add', methods=['POST'])
def add_todo():
    try:
        data = request.get_json()
        description = data.get('itemDescription')
        status = 'Doing' 

        if not description:
            return jsonify({'error': 'Description is required'}), 400

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO todo (description, status) VALUES (%s, %s)', (description, status))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'message': 'Todo item created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/update', methods=['GET']) 
def update_todo():
    item_id = request.args.get('id')
    if not item_id:
        return jsonify({'error': 'Item ID is required'}), 400 

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM todo WHERE id = %s', (item_id,))
    todo_item = cursor.fetchone()

    if not todo_item:
        return jsonify({'error': 'Todo item not found'}), 404
    
    new_status = 'Done' if todo_item['status'] == 'Doing' else 'Doing'
    cursor.execute('UPDATE todo SET status = %s WHERE id = %s', (new_status, item_id))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'message': f'Todo item {item_id} updated successfully to status {new_status}'}), 200

@app.route('/api/delete', methods=['DELETE'])
def delete_todo():
    item_id = request.args.get('id')
    if not item_id:
        return jsonify({'error': 'Item ID is required'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM todo WHERE id = %s', (item_id,))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'message': f'Todo item {item_id} deleted successfully'}), 200

if __name__ == '__main__':
    ensure_database_exists()
    app.run(debug=True)
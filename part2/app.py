from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = '272004'
DB_NAME = 'todo_app'

def checkDatabase():
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

        cursor.execute("SHOW DATABASES")
        databases = [db[0] for db in cursor.fetchall()]
        if DB_NAME in databases:
            print(f"Database '{DB_NAME}' already exists.")
        else:
            print(f"Database '{DB_NAME}' not found. Creating database...")
            with open('create_db.sql', 'r') as file:
                sql_script = file.read()
            
            for statement in sql_script.split(';'):
                if statement.strip():
                    cursor.execute(statement)
            print(f"Database '{DB_NAME}' and tables created successfully with initial data.")
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


def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='272004',
        database='todo_app'
    )

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM todo')
    todoList = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', todoList=todoList)

@app.route('/add', methods=['POST'])
def add_item():
    description = request.form['itemDescription']
    status = 'Doing'

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO todo (description, status) VALUES (%s, %s)', (description, status))
    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('index'))

@app.route('/update/<int:item_id>', methods=['POST'])
def update_item(item_id):
    description = request.form['itemDescription']
    done = 'done' in request.form
    new_status = 'Done' if done else 'Doing'

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE todo SET description = %s, status = %s WHERE id = %s',
                   (description, new_status, item_id))
    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('index'))

@app.route('/delete/<int:item_id>')
def delete_item(item_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM todo WHERE id = %s', (item_id,))
    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('index'))

if __name__ == '__main__':
    checkDatabase()
    app.run(debug=True)
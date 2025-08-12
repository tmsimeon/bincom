import psycopg2

# Database connection details
HOST = "localhost"
PORT = 5432
USER = "postgres"
PASSWORD = "bincom"  # Change to your postgres password
DB_NAME = "bincom_db"
TABLE_NAME = "todos"

# Connect to default postgres database
def connect_default():
    return psycopg2.connect(
        host=HOST, port=PORT, user=USER, password=PASSWORD, dbname="postgres"
    )

# Connect to our new database
def connect_db():
    return psycopg2.connect(
        host=HOST, port=PORT, user=USER, password=PASSWORD, dbname=DB_NAME
    )

# Create database
def create_database():
    conn = connect_default()
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(f"DROP DATABASE IF EXISTS {DB_NAME};")
    cur.execute(f"CREATE DATABASE {DB_NAME};")
    cur.close()
    conn.close()
    print(f"Database '{DB_NAME}' created successfully.")

# Create table
def create_table():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            id SERIAL PRIMARY KEY,
            task TEXT NOT NULL,
            done BOOLEAN DEFAULT FALSE
        );
    """)
    conn.commit()
    cur.close()
    conn.close()
    print(f"Table '{TABLE_NAME}' created successfully.")

# Insert task (CREATE)
def insert_task(task):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute(f"INSERT INTO {TABLE_NAME} (task) VALUES (%s)", (task,))
    conn.commit()
    cur.close()
    conn.close()
    print(f"Task '{task}' added.")

# Get tasks (READ)
def get_tasks():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {TABLE_NAME}")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

# Update task (UPDATE)
def mark_task_done(task_id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute(f"UPDATE {TABLE_NAME} SET done = TRUE WHERE id = %s", (task_id,))
    conn.commit()
    cur.close()
    conn.close()
    print(f"Task {task_id} marked as done.")

# Delete task (DELETE)
def delete_task(task_id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute(f"DELETE FROM {TABLE_NAME} WHERE id = %s", (task_id,))
    conn.commit()
    cur.close()
    conn.close()
    print(f"Task {task_id} deleted.")

# Main program
if __name__ == "__main__":
    create_database()
    create_table()

    # Create
    insert_task("Bincom assignment 3")
    insert_task("bincom crud operations with postgres")

    # Read
    print("Tasks:", get_tasks())

    # Update
    mark_task_done(1)
    print("Tasks after update:", get_tasks())

    # Delete
    delete_task(2)
    print("Tasks after delete:", get_tasks())

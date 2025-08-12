import psycopg2

# Admin credentials (must already have postgres installed)
ADMIN_USER = "postgres"
ADMIN_PASSWORD = "bincom"  # change this to your postgres password
ADMIN_HOST = "localhost"
ADMIN_PORT = "5432"

# New database details
NEW_DB = "todo_db"
NEW_USER = "todo_user"
NEW_PASSWORD = "todo_pass"

# Step 1: Connect as postgres admin and create DB + user
def setup_database():
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user=ADMIN_USER,
            password=ADMIN_PASSWORD,
            host=ADMIN_HOST,
            port=ADMIN_PORT
        )
        conn.autocommit = True
        cur = conn.cursor()

        # Create user
        cur.execute(f"CREATE USER {NEW_USER} WITH PASSWORD '{NEW_PASSWORD}';")

        # Create database
        cur.execute(f"CREATE DATABASE {NEW_DB} OWNER {NEW_USER};")

        print("Database and user created successfully.")

        cur.close()
        conn.close()
    except Exception as e:
        print("Error creating DB/user:", e)

# Step 2: Connect as new user and create todos table
def create_table():
    try:
        conn = psycopg2.connect(
            dbname=NEW_DB,
            user=NEW_USER,
            password=NEW_PASSWORD,
            host=ADMIN_HOST,
            port=ADMIN_PORT
        )
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS todos (
                id SERIAL PRIMARY KEY,
                task TEXT NOT NULL,
                done BOOLEAN DEFAULT FALSE
            );
        """)
        conn.commit()
        print("✅ Table created.")

        cur.close()
        conn.close()
    except Exception as e:
        print("Error creating table:", e)

# Step 3: Add a new task
def add_task(task):
    conn = psycopg2.connect(
        dbname=NEW_DB,
        user=NEW_USER,
        password=NEW_PASSWORD,
        host=ADMIN_HOST,
        port=ADMIN_PORT
    )
    cur = conn.cursor()
    cur.execute("INSERT INTO todos (task) VALUES (%s);", (task,))
    conn.commit()
    cur.close()
    conn.close()

# Step 4: List tasks
def list_tasks():
    conn = psycopg2.connect(
        dbname=NEW_DB,
        user=NEW_USER,
        password=NEW_PASSWORD,
        host=ADMIN_HOST,
        port=ADMIN_PORT
    )
    cur = conn.cursor()
    cur.execute("SELECT id, task, done FROM todos;")
    for row in cur.fetchall():
        print(row)
    cur.close()
    conn.close()

# Step 5: Mark task as done
def mark_done(task_id):
    conn = psycopg2.connect(
        dbname=NEW_DB,
        user=NEW_USER,
        password=NEW_PASSWORD,
        host=ADMIN_HOST,
        port=ADMIN_PORT
    )
    cur = conn.cursor()
    cur.execute("UPDATE todos SET done = TRUE WHERE id = %s;", (task_id,))
    conn.commit()
    cur.close()
    conn.close()

# Main execution
if __name__ == "__main__":
    setup_database()
    create_table()

    # Example usage
    add_task("Learn Python with PostgreSQL")
    add_task("Build a to-do app")
    list_tasks()
    mark_done(1)
    print("\nAfter marking task 1 as done:")
    list_tasks()

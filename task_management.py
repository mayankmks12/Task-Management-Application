import mysql.connector
from mysql.connector import Error
import datetime

# Database connection functions
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='username',         # Replace with your MariaDB username
            password='password',      # Replace with your MariaDB password
            database='task_management'     # Ensure this database exists
        )
        if connection.is_connected():
            print("Connected to MariaDB database")
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

def close_connection(connection):
    if connection and connection.is_connected():
        connection.close()
        print("Connection closed")

# CRUD functions
def add_user(username, email):
    connection = create_connection()
    if connection is None:
        print("Failed to connect to the database. Please check your connection settings.")
        return

    cursor = connection.cursor()
    sql = "INSERT INTO users (username, email) VALUES (%s, %s)"
    cursor.execute(sql, (username, email))
    connection.commit()
    print(f"User {username} added with ID {cursor.lastrowid}")
    close_connection(connection)

def add_task(title, description, assigned_user, due_date):
    connection = create_connection()
    if connection is None:
        print("Failed to connect to the database. Please check your connection settings.")
        return

    cursor = connection.cursor()
    sql = """
    INSERT INTO tasks (title, description, assigned_user, due_date)
    VALUES (%s, %s, %s, %s)
    """
    cursor.execute(sql, (title, description, assigned_user, due_date))
    connection.commit()
    print(f"Task '{title}' added with ID {cursor.lastrowid}")
    close_connection(connection)

def update_task_status(task_id, status):
    connection = create_connection()
    if connection is None:
        print("Failed to connect to the database. Please check your connection settings.")
        return

    cursor = connection.cursor()
    sql = "UPDATE tasks SET status = %s WHERE id = %s"
    cursor.execute(sql, (status, task_id))
    connection.commit()
    print(f"Task ID {task_id} updated to status '{status}'")
    close_connection(connection)

def list_tasks():
    connection = create_connection()
    if connection is None:
        print("Failed to connect to the database. Please check your connection settings.")
        return

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()
    print("All Tasks:")
    for row in rows:
        print(row)
    close_connection(connection)

def delete_task(task_id):
    connection = create_connection()
    if connection is None:
        print("Failed to connect to the database. Please check your connection settings.")
        return

    cursor = connection.cursor()
    sql = "DELETE FROM tasks WHERE id = %s"
    cursor.execute(sql, (task_id,))
    connection.commit()
    print(f"Task ID {task_id} deleted")
    close_connection(connection)

# CLI functions
def display_menu():
    print("\nTask Management System")
    print("1. Add User")
    print("2. Add Task")
    print("3. Update Task Status")
    print("4. List All Tasks")
    print("5. Delete Task")
    print("6. Exit")

def main():
    while True:
        display_menu()
        choice = input("Choose an option (1-6): ")

        if choice == '1':
            username = input("Enter username: ")
            email = input("Enter email: ")
            add_user(username, email)

        elif choice == '2':
            title = input("Enter task title: ")
            description = input("Enter task description: ")
            assigned_user = int(input("Enter user ID to assign the task to: "))
            due_date_str = input("Enter due date (YYYY-MM-DD): ")
            try:
                due_date = datetime.datetime.strptime(due_date_str, '%Y-%m-%d').date()
                add_task(title, description, assigned_user, due_date)
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD.")

        elif choice == '3':
            task_id = int(input("Enter task ID to update: "))
            status = input("Enter new status (pending, in-progress, completed): ")
            if status in ['pending', 'in-progress', 'completed']:
                update_task_status(task_id, status)
            else:
                print("Invalid status. Please choose from 'pending', 'in-progress', or 'completed'.")

        elif choice == '4':
            list_tasks()

        elif choice == '5':
            task_id = int(input("Enter task ID to delete: "))
            delete_task(task_id)

        elif choice == '6':
            print("Exiting the Task Management System.")
            break

        else:
            print("Invalid option. Please choose a number from 1 to 6.")

if __name__ == "__main__":
    main()

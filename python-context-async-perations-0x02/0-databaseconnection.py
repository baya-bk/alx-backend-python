import sqlite3


class DatabaseConnection:
    """
    Custom class-based context manager to handle SQLite database connection.
    """

    def __init__(self, db_name="users.db"):
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        return self.cursor  # Return the cursor for executing queries

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        if exc_type:
            print(f"An error occurred: {exc_val}")
        # Returning False means exceptions are not suppressed
        return False


# Example usage
if __name__ == "__main__":
    with DatabaseConnection() as cursor:
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        for row in results:
            print(row)

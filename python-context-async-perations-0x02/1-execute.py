import sqlite3


class ExecuteQuery:
    """
    Custom context manager that executes a given SQL query
    with provided parameters and manages database connection.
    """

    def __init__(self, query, params=(), db_name="users.db"):
        self.query = query
        self.params = params
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.result = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.query, self.params)
        self.result = self.cursor.fetchall()
        return self.result  # Return the query result

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        if exc_type:
            print(f"Error during query execution: {exc_val}")
        return False


# Example usage
if __name__ == "__main__":
    with ExecuteQuery("SELECT * FROM users WHERE age > ?", (25,)) as results:
        for row in results:
            print(row)

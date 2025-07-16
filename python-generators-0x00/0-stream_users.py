#!/usr/bin/python3
import seed

def stream_users():
    """Generator that yields one user row at a time from user_data table"""
    connection = seed.connect_to_prodev()
    if not connection:
        return

    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")

    for row in cursor:
        yield row

    cursor.close()
    connection.close()

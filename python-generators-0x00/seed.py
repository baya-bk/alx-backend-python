import mysql.connector
import csv
import uuid

def connect_db():
    try:
        return mysql.connector.connect(
            host='localhost',
            user='root',
            password='your_mysql_password'  # change this accordingly
        )
    except mysql.connector.Error as err:
        print(f"Connection failed: {err}")
        return None

def create_database(connection):
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
    cursor.close()

def connect_to_prodev():
    try:
        return mysql.connector.connect(
            host='localhost',
            user='root',
            password='your_mysql_password',  # change this
            database='ALX_prodev'
        )
    except mysql.connector.Error as err:
        print(f"Connection to ALX_prodev failed: {err}")
        return None

def create_table(connection):
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_data (
            user_id VARCHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL NOT NULL,
            INDEX(user_id)
        );
    """)
    connection.commit()
    print("Table user_data created successfully")
    cursor.close()

def insert_data(connection, file_path):
    cursor = connection.cursor()
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            user_id = str(uuid.uuid4())
            name = row['name']
            email = row['email']
            age = row['age']
            cursor.execute("""
                INSERT INTO user_data (user_id, name, email, age)
                VALUES (%s, %s, %s, %s)
            """, (user_id, name, email, age))
    connection.commit()
    cursor.close()



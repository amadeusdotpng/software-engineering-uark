# Must install psycopg2 package on machine
# sudo apt-get install python3-psycopg2
import psycopg2
from psycopg2 import sql

if __name__ == '__main__':
    # Connection parameters
    DB_NAME = "photon"
    DB_USER = "student"
    DB_PASS = "student"
    DB_HOST = "localhost"

    try:
        # Connect to database
        conn = psycopg2.connect(
            dbname = DB_NAME,
            user = DB_USER,
            password = DB_PASS,
            host = DB_HOST,
        )
        print("Successfully connected to database.")

        cursor = conn.cursor() # Create cursor

        # Create table if not already present
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS players (
                id INTEGER PRIMARY KEY,
                codename VARCHAR(255)
            );
        ''')
        
        # Insert data
        cursor.execute('''
            INSERT INTO players (id, codename) VALUES
            (1, 'Scooby'),
            (2, 'Doo')
        ''')

        conn.commit() # Commit changes

        # Fetch and display data from table
        cursor.execute("SELECT * FROM players;")
        rows = cursor.fetchall()
        for row in rows:
            print(row)

    except Exception as error:
        print(f"Error connecting to PostgreSQL daatabase: {error}")

    finally:
        if conn:
            conn.close()
        if cursor:
            cursor.close()
        print("Connection closed.")
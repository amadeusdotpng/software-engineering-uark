# Must install psycopg2 package on machine
# sudo apt-get install python3-psycopg2
import psycopg2
from psycopg2 import sql

if __name__ == '__main__':
    # Connect to database
    try:
        conn = psycopg2.connect(
            dbname = "photon",
            user = "student",
            password = "student",
            host = "localhost",
        )
        cursor = conn.cursor()

        print("Successfully connected to database.")
        
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"Connected to - {version}")

    except Exception as error:
        print(f"Error connecting to PostgreSQL daatabase: {error}")

    finally:
        if conn:
            conn.close()
            print("Connection closed.")
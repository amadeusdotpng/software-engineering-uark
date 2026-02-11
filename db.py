import psycopg2
from psycopg2 import sql

try:
    conn = psycopg2.connect(
        dbname = "photon",
        user = "student",
        password = "student",
        host = "localhost",
    )

except Exception as error:
    print(f"Error connecting to PostgreSQL daatabase: {error}")

finally:
    if conn:
        conn.close()
        print("Connection closed.")
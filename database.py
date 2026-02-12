# Must install psycopg2 package on machine
# sudo apt-get install python3-psycopg2
import psycopg2
from psycopg2 import sql

class PlayerDatabase:
    def __init__(self):
        try:
            # Connect to database
            self.conn = psycopg2.connect(
                dbname = "photon",
                user = "student",
                password = "student",
                host = "localhost",
            )
            # Create cursor
            self.cursor = self.conn.cursor()
        except Exception as error:
            print(f"Error connecting to the database: {error}")

    # Add new entry to table
    def add_player(self, id, codename):
        self.cursor.execute('''
            INSERT INTO players (id, codename)
            VALUES (%s, %s);
        ''', (id, codename))
        self.conn.commit()

    # Delete entry in table
    def delete_player(self, id, codename):
        self.cursor.execute('''
            DELETE FROM players
            WHERE id = %s AND codename = %s;
        ''', (id, codename))
        self.conn.commit()

    # Fetch and display all entries in table
    def display_players(self):
        self.cursor.execute("SELECT * FROM players;")
        rows = self.cursor.fetchall()

        for row in rows:
            print(row)

    # Close cursor and connection
    def close(self):
        if self.conn:
            self.conn.close()
        if self.cursor:
            self.cursor.close()


if __name__ == '__main__':
    test_db = PlayerDatabase()

    # Test cases
    try:
        # test_db.add_player(3, 'foo')
        test_db.delete_player(3, 'foo')
        test_db.display_players()
    except Exception as error:
        print(f"Error connecting to database: {error}")
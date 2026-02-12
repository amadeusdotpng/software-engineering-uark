# Must install psycopg2 package on machine
# sudo apt-get install python3-psycopg2
import psycopg2
from psycopg2 import sql

# Database is named photon and contains one table called players
# The table has two columns: id and codename
# id is an integer and codename is a string

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
    def delete_player(self, id):
        self.cursor.execute('''
            DELETE FROM players
            WHERE id = %s;
        ''', (id,))
        self.conn.commit()

    # Fetch an entry in table
    def get_player(self, id):
        self.cursor.execute('''
            SELECT * FROM players
            WHERE id = %s;
        ''', (id,))
        return self.cursor.fetchone()
    
    # Check database to see if a player with a given ID already exists
    def player_exists(self, id):
        self.cursor.execute('''
            SELECT EXISTS (
                SELECT 1 FROM players WHERE id = %s
            );
        ''', (id,))
        return self.cursor.fetchone()[0]
    
    # Update an existing player's codename
    def update_player(self, id, new_codename):
        self.cursor.execute('''
            UPDATE players
            SET codename = %s
            WHERE id = %s;
        ''', (new_codename, id))
        self.conn.commit()

    # Fetch and display all entries in table
    def display_players(self):
        self.cursor.execute("SELECT * FROM players;")
        rows = self.cursor.fetchall()

        for data in rows:
            print(f"ID: {data[0]}\tCodename: {data[1]}")

    # Close cursor and connection
    def close(self):
        if self.conn:
            self.conn.close()
        if self.cursor:
            self.cursor.close()

if __name__ == '__main__':
    test_db = PlayerDatabase()

    try:
        # Test cases
        if test_db.player_exists(1):
            player = test_db.get_player(1)
            print(f"Player {player[0]} is named {player[1]}.")

        test_db.display_players()

        test_db.close()
    except Exception as error:
        print(f"Error connecting to database: {error}")
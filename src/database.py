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

    # Returns corresponding codename given an ID
    def get_codename(self, id):
        self.cursor.execute('''
            SELECT codename FROM players
            WHERE id = %s;
        ''', (id,))
        return self.cursor.fetchone()[0]
    
    # Returns True if a player with a given ID already exists in the database
    def player_exists(self, id):
        self.cursor.execute('''
            SELECT EXISTS (
                SELECT 1 FROM players WHERE id = %s
            );
        ''', (id,))
        return self.cursor.fetchone()[0]

    # Fetch an entry in table
    def get_player(self, id):
        self.cursor.execute('''
            SELECT * FROM players
            WHERE id = %s;
        ''', (id,))
        return self.cursor.fetchone() # Returns a tuple formatted (id, codename)
    
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

# if __name__ == '__main__':
#     test_db = PlayerDatabase()

#     # Example test case of how the program flow is supposed to go
#     try:
#         # Prompt user for player ID
#         player_id = int(input("Enter the player ID: "))
#         codename = None

#         # Query database to see if it exists
#         if test_db.player_exists(player_id):
#             # If it does, retrieve the codename
#             codename = test_db.get_codename(player_id)
#         else:
#             # If it doesn't, prompt user for codename
#             print("Player does not exist.")
#             codename = input("Enter a codename: ")
            
#             # Add new entry into the database
#             test_db.add_player(player_id, codename)

#         # Print player info
#         print(f"ID: {player_id}\tCodename: {codename}")

#         # Display all players
#         print("\nDisplaying all players:")
#         test_db.display_players()
#     except Exception as error:
#         print(f"Error connecting to database: {error}")
    
#     # Close database
#     test_db.close()
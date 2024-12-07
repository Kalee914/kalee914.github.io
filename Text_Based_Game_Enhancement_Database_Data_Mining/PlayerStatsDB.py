#database

import sqlite3

class PlayerStatsDB:
    #initialize
    def __init__(self, db_name="player_stats.db"): #database name = player_stats
        self.conn = sqlite3.connect(db_name) #connecting to sqlite
        self.cursor = self.conn.cursor() #creating a cursor object using the cursor() method
        self.create_table() #create table function

        #create table function
    def create_table(self):
            # create table if tnot already exist
        table = """ CREATE TABLE IF NOT EXISTS 
        player_stats(
        gamer_tag TEXT PRIMARY KEY,
        wins INTEGER DEFAULT 0,
        losses INTEGER DEFAULT 0
        )"""
        self.cursor.execute(table)
        self.conn.commit() #commiting change in database

        #add player function
    def add_player(self,gamer_tag):
        self.cursor.execute("""
        INSERT OR IGNORE INTO player_stats(gamer_tag) VALUES (?) 
        """, (gamer_tag,)) #add player if player is not already exist
        self.conn.commit()

        # update win or losses function
    def update_stats(self, gamer_tag, win=True):
        column = "wins" if win else "losses"
        self.cursor.execute(f"""
        UPDATE player_stats
        SET {column} = {column} + 1
        WHERE gamer_tag =?
        """, (gamer_tag,)) # if win is true add win, false add losses
        self.conn.commit()

        # retrieve player stats
    def get_player_stats(self, gamer_tag):
        self.cursor.execute(""" 
        SELECT wins, losses 
        FROM player_stats
        WHERE gamer_tag = ?
        """, (gamer_tag,))
        result = self.cursor.fetchone()
        # Check if result is None (player not found)
        if result:
            wins, losses = result
            print("*" * 100)
            print(">>>>>>>>>> PLAYER STATS REPORT <<<<<<<<<<<")
            print(f"Player stats for {gamer_tag}: wins: {wins}, losses: {losses}")
            # calculate average
            avg_wins, avg_losses = self.calculate_avg(gamer_tag)
            print(f"Average stats for {gamer_tag}: Avg wins: {avg_wins}, Avg losses: {avg_losses}")
            print("*" * 100)

        else:
            print(f"current stats for {gamer_tag}: No stats found")

        # calculate average function
    def calculate_avg(self, gamer_tag):
        self.cursor.execute("""
        SELECT wins, losses
        FROM player_stats
        WHERE gamer_tag = ?
        """, (gamer_tag,))
        result = self.cursor.fetchone()
        if result:
            wins, losses = result
            total_games = wins + losses
            if total_games == 0:
                return 0, 0 # No game played
            avg_wins = wins / total_games
            avg_losses = losses / total_games
        return avg_wins, avg_losses


        #Close connection
    def close(self):
        self.conn.close()



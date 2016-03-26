#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM matches")
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM players")
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM players")
    player_count = c.fetchone()[0]
    conn.close()
    return player_count


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    c = conn.cursor()
    c.execute("INSERT INTO players (name) VALUES (%s)", (name,))
    conn.commit()
    conn.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn = connect()
    c = conn.cursor()

    # Use a left join to list players with 0 matches
    c.execute("""SELECT p.id, p.name,
        SUM(case when m.winner = p.id then 1 else 0 end) as wins,
        SUM(case when m.winner = p.id  OR m.loser = p.id then 1 else 0 end)
        AS matches
        FROM players AS p LEFT JOIN matches AS m
        ON (m.winner = p.id OR m.loser = p.id)
        GROUP BY p.id, p.name
        ORDER BY wins DESC""")
    player_standings = list(c)
    conn.close()
    return player_standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """

    conn = connect()
    c = conn.cursor()
    c.execute("INSERT INTO matches (winner, loser) VALUES (%s, %s)", (winner,
                                                                      loser))
    conn.commit()
    conn.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """

    player_pairs = []

    conn = connect()
    c = conn.cursor()
    # Get pairs through the minimalistic beauty of stored procedure
    c.execute("""SELECT * FROM pairings_view""")

    data = list(c)
    num_of_results = c.rowcount
    conn.close()

    for i in range(0, num_of_results, 2):
        pair = (data[i][0], data[i][1], data[i+1][0], data[i+1][1])
        player_pairs.append(pair)

    return player_pairs


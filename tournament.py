#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach

def connect(database_name="tournament"):
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        conn = psycopg2.connect("dbname={}".format(database_name))
        cursor = conn.cursor()
        return conn, cursor
    except:
        print("Unable to connect to Database!")


def deleteMatches():
    """Remove all the match records from the database."""
    conn, cursor = connect()
    cursor.execute("DELETE FROM matches;")
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn, cursor = connect()
    cursor.execute("DELETE FROM players;")
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    conn, cursor = connect()
    cursor.execute("SELECT count(id) AS number FROM players;")
    count = cursor.fetchone()[0]
    conn.close()
    return count


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    conn, cursor = connect()
    name = bleach.clean(name)
    cursor.execute("INSERT INTO players (name) VALUES (%s);", (name,))
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
    conn, cursor = connect()
    query = """SELECT wincounter.id, wincounter.name, wincounter.wins, matchcounter.matches_played
                FROM wincounter, matchcounter
                WHERE wincounter.id = matchcounter.id
                ORDER BY wincounter.wins;"""
    cursor.execute(query)
    standings = cursor.fetchall()
    conn.close()
    return standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn, cursor = connect()
    winner = bleach.clean(winner)
    loser = bleach.clean(loser)
    cursor.execute("INSERT INTO matches (winner_id, loser_id) VALUES (%s,%s);", (winner,loser,))
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
    conn, cursor = connect()
    x = countPlayers()
    pairings = []
    n = 0
    while n < x:
        cursor.execute("SELECT id, name FROM wincounter ORDER BY wins LIMIT 2 OFFSET %s;" % n)
        y = cursor.fetchall()
        pairings.append(y[0] + y[1])
        n = n + 2
    conn.close()
    return pairings

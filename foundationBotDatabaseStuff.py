'''----------------------------------------------------------------------------\
| ||\\    //||       /|¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯\ |
| || \\  // ||  (o_ / |                  SUPPLEMENTARY FILE                  | |
| ||  \\//  ||  //\/  |                         ----                         | |
| ||   \/   ||  V_/_  |                    DATABASE STUFF                    | |
| ||        ||        |‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗/ |
\----------------------------------------------------------------------------'''

import sqlite3
from sqlite3 import Error

# create a connection to the SQLite database
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn

# --------------------------------- LEADERBOARD ---------------------------------- #

# create leaderboard table
def create_leaderboard_table(conn):
    try:
        cur = conn.cursor()
        sql = 'CREATE TABLE IF NOT EXISTS Leaderboard ( \
               id integer PRIMARY KEY, \
               userid integer NOT NULL UNIQUE, \
               postcount integer NOT NULL, \
               score integer NOT NULL \
               );'
        cur.execute(sql)
    except Error as e:
        print(e)

# create leaderboard entry
def create_leaderboard_entry(conn, leaderboardEntry):
    sql = 'INSERT INTO Leaderboard (userid,postcount,score) SELECT ?,?,? WHERE NOT EXISTS(SELECT * FROM Leaderboard WHERE userid=?)'
    cur = conn.cursor()
    cur.execute(sql, leaderboardEntry)
    conn.commit()
    return cur.rowcount

# update leaderboard entry
def update_leaderboard_entry(conn, leaderboardEntry):
    sql='UPDATE Leaderboard SET postcount = ?, score = ? WHERE userid = ?'
    cur = conn.cursor()
    cur.execute(sql, leaderboardEntry)
    conn.commit()

# get the whole leaderboard
def get_leaderboard(conn):
    cur = conn.cursor()
    cur.execute('SELECT * FROM Leaderboard')
    rows = cur.fetchall()
    return rows

# ----------------------------------- RANKING ------------------------------------ #

# create ranking table
def create_ranking_table(conn):
    try:
        cur = conn.cursor()
        sql = 'CREATE TABLE IF NOT EXISTS Ranks ( \
               id integer PRIMARY KEY, \
               userid integer NOT NULL UNIQUE, \
               experience integer NOT NULL, \
               estate string NOT NULL, \
               rank integer NOT NULL \
               );'
        cur.execute(sql)
    except Error as e:
        print(e)

# create ranking entry
def create_ranking_entry(conn, rankingEntry):
    sql = 'INSERT INTO Ranks (userid,experience,estate,rank) SELECT ?,?,?,? WHERE NOT EXISTS(SELECT * FROM Ranks WHERE userid=?)'
    cur = conn.cursor()
    cur.execute(sql, rankingEntry)
    conn.commit()
    return cur.rowcount

# update ranking entry
def update_ranking_entry(conn, rankingEntry):
    sql='UPDATE Ranks SET experience = ?, estate = ?, rank = ? WHERE userid = ?'
    cur = conn.cursor()
    cur.execute(sql, rankingEntry)
    conn.commit()

# get the whole ranking table
def get_ranking_table(conn):
    cur = conn.cursor()
    cur.execute('SELECT * FROM Ranks')
    rows = cur.fetchall()
    return rows

# ----------------------------------- SETTINGS ----------------------------------- #

# create settings table
def create_settings_table(conn):
    try:
        cur = conn.cursor()
        sql = 'CREATE TABLE IF NOT EXISTS Settings ( \
               id integer PRIMARY KEY, \
               setting string NOT NULL UNIQUE, \
               value string \
               );'
        cur.execute(sql)
    except Error as e:
        print(e)

def init_settings(conn):
    sql = 'INSERT INTO Settings (setting,value) SELECT ?,? WHERE NOT EXISTS(SELECT * FROM Settings WHERE setting=?)'
    cur = conn.cursor()
    cur.execute(sql, ('botActive','False','botActive'))
    cur.execute(sql, ('pinsChannel',None,'pinsChannel'))
    cur.execute(sql, ('pinsRoles',None,'pinsRoles'))
    cur.execute(sql, ('leaderboardEmoji',None,'leaderboardEmoji'))
    cur.execute(sql, ('leaderboardChannel',None,'leaderboardChannel'))
    cur.execute(sql, ('moddingChannel',None,'moddingChannel'))
    cur.execute(sql, ('rankingChannel',None,'rankingChannel'))
    cur.execute(sql, ('rankingMessage',None,'rankingMessage'))
    cur.execute(sql, ('labourEmoji',None,'labourEmoji'))
    cur.execute(sql, ('clergyEmoji',None,'clergyEmoji'))
    cur.execute(sql, ('kingdomEmoji',None,'kingdomEmoji'))
    cur.execute(sql, ('defaultRole',None,'defaultRole'))
    cur.execute(sql, ('labourRole1',None,'labourRole1'))
    cur.execute(sql, ('labourRole2',None,'labourRole2'))
    cur.execute(sql, ('labourRole3',None,'labourRole3'))
    cur.execute(sql, ('labourRole4',None,'labourRole4'))
    cur.execute(sql, ('clergyRole1',None,'clergyRole1'))
    cur.execute(sql, ('clergyRole2',None,'clergyRole2'))
    cur.execute(sql, ('clergyRole3',None,'clergyRole3'))
    cur.execute(sql, ('clergyRole4',None,'clergyRole4'))
    cur.execute(sql, ('kingdomRole1',None,'kingdomRole1'))
    cur.execute(sql, ('kingdomRole2',None,'kingdomRole2'))
    cur.execute(sql, ('kingdomRole3',None,'kingdomRole3'))
    cur.execute(sql, ('kingdomRole4',None,'kingdomRole4'))
    cur.execute(sql, ('highestRole',None,'highestRole'))
    cur.execute(sql, ('expLevel1',None,'expLevel1'))
    cur.execute(sql, ('expLevel2',None,'expLevel2'))
    cur.execute(sql, ('expLevel3',None,'expLevel3'))
    cur.execute(sql, ('expLevel4',None,'expLevel4'))
    cur.execute(sql, ('expLevelH',None,'expLevelH'))
    conn.commit()
    
# update setting
def update_setting(conn, settingsEntry):
    sql = 'UPDATE Settings SET value = ? WHERE setting = ?'
    cur = conn.cursor()
    cur.execute(sql, settingsEntry)
    conn.commit()
    
# get settings
def get_settings(conn):
    cur = conn.cursor()
    cur.execute('SELECT * FROM Settings')
    rows = cur.fetchall()
    return rows
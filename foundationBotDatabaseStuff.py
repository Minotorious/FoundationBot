'''----------------------------------------------------------------------------\
| ||\\    //||       /|¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯\ |
| || \\  // ||  (o_ / |                  SUPPLEMENTARY FILE                  | |
| ||  \\//  ||  //\/  |                         ----                         | |
| ||   \/   ||  V_/_  |                    DATABASE STUFF                    | |
| ||        ||        |‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗/ |
\----------------------------------------------------------------------------'''

import sqlite3
from sqlite3 import Error

# import logger
from foundationBotLogger import *
logger = Logger()

# create a connection to the SQLite database
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        logger.getLogger().error(e)
    return conn

# --------------------------------- LEADERBOARD ---------------------------------- #

# create screenshot leaderboard table
def create_screenshot_leaderboard_table(conn):
    try:
        cur = conn.cursor()
        sql = 'CREATE TABLE IF NOT EXISTS ScreenshotLeaderboard ( \
               id integer PRIMARY KEY, \
               screenshotid integer NOT NULL UNIQUE, \
               score integer NOT NULL \
               );'
        cur.execute(sql)
        logger.getLogger().info('ScreenshotLeaderboard Table Created Successfully')
    except Error as e:
        logger.getLogger().error(e)

# create screenshots leaderboard entry
def create_screenshot_leaderboard_entry(conn, sle):
    sql = 'INSERT INTO ScreenshotLeaderboard (screenshotid,score) SELECT ?,? WHERE NOT EXISTS(SELECT * FROM ScreenshotLeaderboard WHERE screenshotid=?)'
    cur = conn.cursor()
    cur.execute(sql, sle)
    conn.commit()
    return cur.rowcount

# update screenshots leaderboard entry
def update_screenshot_leaderboard_entry(conn, sle):
    sql='UPDATE ScreenshotLeaderboard SET score = ? WHERE screenshotid = ?'
    cur = conn.cursor()
    cur.execute(sql, sle)
    conn.commit()

# get screenshots leaderboard
def get_screenshot_leaderboard(conn):
    cur = conn.cursor()
    cur.execute('SELECT * FROM ScreenshotLeaderboard')
    rows = cur.fetchall()
    return rows

# clear screenshot leaderboard
def clear_screenshot_leaderboard(conn):
    sql='DROP TABLE ScreenshotLeaderboard'
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()

# create messages leaderboard table
def create_messages_leaderboard_table(conn):
    try:
        cur = conn.cursor()
        sql = 'CREATE TABLE IF NOT EXISTS MessagesLeaderboard ( \
               id integer PRIMARY KEY, \
               userid integer NOT NULL UNIQUE, \
               score integer NOT NULL \
               );'
        cur.execute(sql)
        logger.getLogger().info('MessagesLeaderboard Table Created Successfully')
    except Error as e:
        logger.getLogger().error(e)

# create messages leaderboard entry
def create_messages_leaderboard_entry(conn, mle):
    sql = 'INSERT INTO MessagesLeaderboard (userid,score) SELECT ?,? WHERE NOT EXISTS(SELECT * FROM MessagesLeaderboard WHERE userid=?)'
    cur = conn.cursor()
    cur.execute(sql, mle)
    conn.commit()
    return cur.rowcount

# update messages leaderboard entry
def update_messages_leaderboard_entry(conn, mle):
    sql='UPDATE MessagesLeaderboard SET score = ? WHERE userid = ?'
    cur = conn.cursor()
    cur.execute(sql, mle)
    conn.commit()

# get messages leaderboard
def get_messages_leaderboard(conn):
    cur = conn.cursor()
    cur.execute('SELECT * FROM MessagesLeaderboard')
    rows = cur.fetchall()
    return rows

# clear messages leaderboard
def clear_messages_leaderboard(conn):
    sql='DROP TABLE MessagesLeaderboard'
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()

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
               rank integer NOT NULL, \
               gender string NOT NULL \
               );'
        cur.execute(sql)
        logger.getLogger().info('Ranking Table Created Successfully')
    except Error as e:
        logger.getLogger().error(e)

# create ranking entry
def create_ranking_entry(conn, rankingEntry):
    sql = 'INSERT INTO Ranks (userid,experience,estate,rank,gender) SELECT ?,?,?,?,? WHERE NOT EXISTS(SELECT * FROM Ranks WHERE userid=?)'
    cur = conn.cursor()
    cur.execute(sql, rankingEntry)
    conn.commit()
    return cur.rowcount

# update ranking entry
def update_ranking_entry(conn, rankingEntry):
    sql='UPDATE Ranks SET experience = ?, estate = ?, rank = ?, gender = ? WHERE userid = ?'
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
        logger.getLogger().info('Settings Table Created Successfully')
    except Error as e:
        logger.getLogger().error(e)

def init_settings(conn):
    sql = 'INSERT INTO Settings (setting,value) SELECT ?,? WHERE NOT EXISTS(SELECT * FROM Settings WHERE setting=?)'
    cur = conn.cursor()
    cur.execute(sql, ('botActive','False','botActive'))
    cur.execute(sql, ('guildID',None,'guildID'))
    cur.execute(sql, ('excludedRoles',None,'excludedRoles'))
    cur.execute(sql, ('pinsChannel',None,'pinsChannel'))
    cur.execute(sql, ('pinsRoles',None,'pinsRoles'))
    cur.execute(sql, ('leaderboardEmoji',None,'leaderboardEmoji'))
    cur.execute(sql, ('leaderboardInterval',None,'leaderboardInterval'))
    cur.execute(sql, ('leaderboardChannel',None,'leaderboardChannel'))
    cur.execute(sql, ('screenshotChannel',None,'screenshotChannel'))
    cur.execute(sql, ('screenshotPostTime',None,'screenshotPostTime'))
    cur.execute(sql, ('messagesPostTime',None,'messagesPostTime'))
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
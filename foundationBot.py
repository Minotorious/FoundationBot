'''----------------------------------------------------------------------------\
| ||\\    //||       /|¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯\ |
| || \\  // ||  (o_ / | Run: python3 foundationBot.py                        | |
| ||  \\//  ||  //\/  | In:  TOKEN                                           | |
| ||   \/   ||  V_/_  | Out: foundation.db                                   | |
| ||        ||        |‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗/ |
\----------------------------------------------------------------------------'''

import discord
import sqlite3
from sqlite3 import Error
import os

# Import bot settings object
from botsettings_config import *

# ------------------------------ GENERAL SETTINGS ------------------------------- #

# Special Permissions Required: Manage Messages

# Instantiate bot settings objects
settings = botSettings()

# --------------------------- DISCORD EVENT LISTENERS --------------------------- #

client = discord.Client()

@client.event
async def on_message(message):
    # the bot shouldn't reply to itself
    if message.author == client.user:
        return
    
    # the channel the message was sent in
    channel = message.channel
    
    # check for command character
    if message.content.startswith('/'):
        cmd = message.content
        # leaderboard display command
        if cmd == '/leaderboard':
            currentLeaderboard = get_leaderboard(conn)
            formattedleaderboard = [[0]*5 for i in range(len(currentLeaderboard))]
            for i,entry in enumerate(currentLeaderboard):
                formattedleaderboard[i][0] = currentLeaderboard[i][0] # id primary key
                formattedleaderboard[i][1] = message.guild.get_member(currentLeaderboard[i][1]).display_name # userid
                formattedleaderboard[i][2] = currentLeaderboard[i][2] # postcount
                formattedleaderboard[i][3] = currentLeaderboard[i][3] # score
                formattedleaderboard[i][4] = currentLeaderboard[i][3] / currentLeaderboard[i][2] # ratio
            formattedleaderboard.sort(key=sortKey, reverse = True)
            users = ''
            scores = ''
            ratios = ''
            for entry in formattedleaderboard:
                if entry[3] > 0:
                    users += entry[1] + '\n'
                    scores += str(entry[3]) + '\n'
                    ratios += str(entry[4]) + '\n'
            
            # check if leaderboard has entries
            if len(users) == 0:
                await channel.send('The Leaderboard has no Entries with a non-Zero Score!')
                await message.delete()
            else:
                embed = discord.Embed(
                        title = 'Screenshots Leaderboard',
                        #description = '',
                        colour = discord.Colour.dark_green()
                    )
                embed.add_field(name='Username' , value=users, inline=True)
                embed.add_field(name='Score', value=scores, inline=True)
                embed.add_field(name='Ratio', value=ratios, inline=True)
                embed.set_footer(text='Leaderboard as of ' + message.created_at.strftime('%d/%m/%Y, %H:%M') +  ' UTC')
                await channel.send(embed=embed)
                await message.delete()
        # dxdiag help command
        elif cmd == '/dxdiag':
            embed = discord.Embed(
                    title = 'How do I obtain a dxdiag log?',
                    description = '1) Press the Windows key + R\n'
                                  '2) In the small window that appeared type `dxdiag` and press Enter\n'
                                  '3) In the new window that opened press the `Save All Information` button\n'
                                  '4) Save the dxdiag.txt file and drag and drop it in this channel',
                    colour = discord.Colour.dark_green()
                )
            await channel.send(embed=embed)
            await message.delete()
        # savefiles location help command
        elif cmd == '/savefiles':
            embed = discord.Embed(
                    title = 'Where do I find my save files?',
                    #description = '',
                    colour = discord.Colour.dark_green()
                )
            msgsteam = ('`\\Program Files (x86)\\Steam\\userdata\\ YourSteamID \\690830\\remote\\Foundation\\Save Game`\n'
                        '...Where YourSteamID is your unique Steam ID number')
            msggog = '`%USERPROFILE%\\AppData\\Local\\GOG.com\\Galaxy\\Applications\\51968221750131424\\Storage\\Shared\\Files\\Foundation\\Save Game`'
            msglocal = '`%USERPROFILE%\\Documents\\Polymorph Games\\Foundation\\Save Game`'
            embed.add_field(name='Steam Cloud Local Repository', value=msgsteam, inline=False)
            embed.add_field(name='GoG Cloud Local Repository', value=msggog, inline=False)
            embed.add_field(name='Non-Cloud Saves', value=msglocal, inline=False)
            await channel.send(embed=embed)
            await message.delete()
        # trade help command
        elif cmd == '/trade':
            embed = discord.Embed(
                    title = 'Trade Prerequisites',
                    description = '1) Trade route unlocked from the first tab of trade window\n'
                                  '2) Trade window second tab set to buy or sell, and an amount entered for the wanted resource\n'
                                  '3) Warehouse or Granary with slot assigned for the resource you want to trade\n'
                                  '4) Patience for the trader to show up. He will come approximately once per week',
                    colour = discord.Colour.dark_green()
                )
            await channel.send(embed=embed)
            await message.delete()
        # modding help command
        elif cmd == '/modding':
            embed = discord.Embed(
                    title = 'Modding! Where to begin?',
                    description = 'Foundation API: https://www.polymorph.games/foundation/modding/\n'
                                  'Beginner\'s Guide: https://foundation.mod.io/guides/how-to-mod-in-foundation\n'
                                  'Custom Map Guide: https://youtu.be/qXFk0DNUNUA\n'
                                  'For anything further feel free to ask us! ' + discord.utils.get(channel.guild.channels, id=settings.moddingChannel).mention,
                    colour = discord.Colour.dark_green()
                )
            await channel.send(embed=embed)
            await message.delete()
        # prospecting help command
        elif cmd == '/prospecting':
            embed = discord.Embed(
                    title = 'How to Prospecting?',
                    description = '1) Big rock node inside your domain\n'
                                  '2) Bailiff assigned to the bailiff\'s office\n'
                                  '3) Start prospecting mandate\n'
                                  '4) Click on discovered mineral node to build mines',
                    colour = discord.Colour.dark_green()
                )
            await channel.send(embed=embed)
            await message.delete()
        # immigration help command
        elif cmd == '/immigration':
            embed = discord.Embed(
                    title = 'What affects Immigration?',
                    description = '1) Happiness\n'
                                  '2) Residential Space, note desirability also matters depending on the villager rank!\n'
                                  '3) Employment, note villagers with a job but no workplace still count as unemployed!\n\n'
                                  'For more detailed information see this thread: https://steamcommunity.com/app/690830/discussions/0/1742265965886407909/',
                    colour = discord.Colour.dark_green()
                )
            await channel.send(embed=embed)
            await message.delete()
        # preview build help command
        elif cmd == '/preview':
            embed = discord.Embed(
                    title = 'How do I activate a Preview build?',
                    description = '1) Right click on Foundation on Steam\n'
                                  '2) Select Properties\n'
                                  '3) Navigate to the BETAS tab\n'
                                  '4) Select the preview build from the drop down and press close\n'
                                  '5) The preview build should start downloading automatically',
                    colour = discord.Colour.dark_green()
                )
            await channel.send(embed=embed)
            await message.delete()
        # Villager needs help command
        elif cmd == '/needs':
            villagerneeds = ('```Villager Rank Needs\n'
            '+----------+-------+--------------+-------+---------+--------+--------+\n'
            '|   Rank   | Water | Food Sources | House | Clothes | Church | Luxury |\n'
            '+----------+-------+--------------+-------+---------+--------+--------+\n'
            '| Newcomer |   x   |       1      |       |         |        |        |\n'
            '+----------+-------+--------------+-------+---------+--------+--------+\n'
            '|   Serf   |   x   |       1      | lvl 1 |         |    x   |        |\n'
            '+----------+-------+--------------+-------+---------+--------+--------+\n'
            '| Commoner |   x   |       2      | lvl 2 |    x    |    x   |        |\n'
            '+----------+-------+--------------+-------+---------+--------+--------+\n'
            '|  Citizen |   x   |       2      | lvl 2 |    x    |    x   |    1   |\n'
            '+----------+-------+--------------+-------+---------+--------+--------+```')
            armyneeds = ('```Army Rank Needs\n'
            '+---------+-------+--------------+---------------+---------+--------+--------+\n'
            '|   Rank  | Water | Food Sources |     House     | Clothes | Church | Luxury |\n'
            '+---------+-------+--------------+---------------+---------+--------+--------+\n'
            '|  Novice |   x   |       1      | lvl 1 / Dorms |         |    x   |        |\n'
            '+---------+-------+--------------+---------------+---------+--------+--------+\n'
            '| Soldier |   x   |       1      | lvl 2 / Dorms |    x    |    x   |    1   |\n'
            '+---------+-------+--------------+---------------+---------+--------+--------+\n'
            '|  Knight |   x   |       1      | lvl 2 / Dorms |    x    |    x   |    2   |\n'
            '+---------+-------+--------------+---------------+---------+--------+--------+```')
            clergyneeds = ('```Clergy Rank Needs\n'
            '+------+-------+--------------+-------+---------+--------+--------+\n'
            '| Rank | Water | Food Sources | House | Clothes | Church | Luxury |\n'
            '+------+-------+--------------+-------+---------+--------+--------+\n'
            '| Monk |   x   |       1      | Dorms |         |    x   |        |\n'
            '+------+-------+--------------+-------+---------+--------+--------+```')
            await channel.send(villagerneeds)
            await channel.send(armyneeds)
            await channel.send(clergyneeds)
            await message.delete()
        # keybindings help command
        elif cmd == '/keybindings':
            embed = discord.Embed(
                    title = 'Keybindings',
                    #description = '',
                    colour = discord.Colour.dark_green()
                )
            keys = ('Shift + Left Click\n'
                    'T\n'
                    'Ctrl + Mouse Wheel\n'
                    'Ctrl + U\n'
                    'Ctrl + S\n'
                    '+/-\n'
                    'Space\n'
                    'Backspace\n'
                    'Esc\n'
                    'W/A/S/D\n'
                    'Q/E\n'
                    'R/F\n'
                    'Ctrl + MMB + Mouse move')
            descriptions = ('keep building/part selected\n'
                            'toggle monument part snapping\n'
                            'adjust zoning tool brush size\n'
                            'hide UI\n'
                            'quicksave\n'
                            'change game speed\n'
                            'pause game\n'
                            'close all open windows\n'
                            'close currently focused window\n'
                            'move camera\n'
                            'rotate camera\n'
                            'pitch camera\n'
                            'fast pan camera')
            embed.add_field(name='Key' , value=keys, inline=True)
            embed.add_field(name='Description', value=descriptions, inline=True)
            await channel.send(embed=embed)
            await message.delete()
        # commands help command
        elif cmd == '/help' or cmd == '/commands':
            embed = discord.Embed(
                    title = 'Available Commands',
                    #description = '',
                    colour = discord.Colour.dark_green()
                )
            commands = ('/leaderboard\n'
                        '/dxdiag\n'
                        '/savefiles\n'
                        '/trade\n'
                        '/modding\n'
                        '/prospecting\n'
                        '/immigration\n'
                        '/preview\n'
                        '/needs\n'
                        '/keybindings\n'
                        '/help & /commands')
            descriptions = ('Displays screenshot leaderboard\n'
                            'How to obtain a dxdiag log\n'
                            'Where to find save files\n'
                            'How to trade\n'
                            'How to modding\n'
                            'How to prospecting\n'
                            'What affects immigration\n'
                            'How to activate a preview build\n'
                            'What needs do villagers have\n'
                            'Displays available keybindings\n'
                            'Displays this help message\n')
            embed.add_field(name='Command' , value=commands, inline=True)
            embed.add_field(name='Description', value=descriptions, inline=True)
            await channel.send(embed=embed)
            await message.delete()
    # screenshot leaderboard system
    if channel.id == settings.leaderboardChannel:
        if len(message.attachments) > 0:
            for attachment in message.attachments:
                if attachment.url.endswith('.jpg') \
                or attachment.url.endswith('.jpeg') \
                or attachment.url.endswith('.png'):
                    await message.add_reaction(discord.utils.get(channel.guild.emojis, id=settings.leaderboardEmoji))
                    # check if user is already in the leaderboard
                    if not message.author.id in leaderboard:
                        try:
                            create_leaderboard_entry(conn, (message.author.id, 1, 0))
                            conn.commit()
                            leaderboard.append(message.author.id)
                        except Error as e:
                            print(e)
                            pass
                        finally:
                            break
                    else:
                        # add to postcount since it is not the first post
                        postcount = int(get_leaderboard_user_postcount(conn, message.author.id)[0][0]) # [0][0] for getting the actual value out of list of tuples
                        postcount += 1
                        update_leaderboard_entry_postcount(conn, (postcount, message.author.id))
                        break
        
@client.event
async def on_raw_reaction_add(payload):
    # the bot shouldn't reply to itself
    if payload.member == client.user:
        return
    
    emoji = payload.emoji
    # message pinning system
    if str(emoji) == '📌':
        member = payload.member
        # check the emoji was used by a player with the allowed role to pin
        for role in settings.pinsRoles:
            if discord.utils.get(member.guild.roles, id=role) in member.roles:
                origChannel = client.get_channel(payload.channel_id)
                message = await origChannel.fetch_message(payload.message_id)
                postChannel = client.get_channel(settings.pinsChannel)
                msg = 'https://discordapp.com/channels/' + str(member.guild.id) + '/' + str(origChannel.id) + '/' + str(message.id)
                embed = discord.Embed(
                    description = message.content,
                    colour = discord.Colour.dark_green()
                )
                embed.set_author(name=message.author.display_name + ' on ' + message.created_at.strftime('%d/%m/%Y, %H:%M') +  ' UTC')
                embed.set_footer(text='Pinned by: ' + member.display_name )
                await postChannel.send(msg, embed=embed)
                break

    # screenshot leaderboard system
    elif emoji.id == settings.leaderboardEmoji:
        channel = client.get_channel(payload.channel_id)
        if channel.id == settings.leaderboardChannel:
            message = await channel.fetch_message(payload.message_id)
            # check if the bot has reacted to the screenshot
            async for user in discord.utils.get(message.reactions, emoji=emoji).users():
                if user == client.user:
                    if len(message.attachments) > 0:
                        for attachment in message.attachments:
                            if attachment.url.endswith('.jpg') \
                            or attachment.url.endswith('.jpeg') \
                            or attachment.url.endswith('.png'):
                                # add leaderboard point
                                score = int(get_leaderboard_user_score(conn, message.author.id)[0][0]) # [0][0] for getting the actual value out of list of tuples
                                score += 1
                                update_leaderboard_entry_score(conn, (score, message.author.id))
                                break

@client.event
async def on_raw_reaction_remove(payload):
    emoji = payload.emoji
    # screenshot leaderboard system
    if emoji.id == settings.leaderboardEmoji:
        channel = client.get_channel(payload.channel_id)
        if channel.id == settings.leaderboardChannel:
            message = await channel.fetch_message(payload.message_id)
            # check if the bot has reacted to the screenshot
            async for user in discord.utils.get(message.reactions, emoji=emoji).users():
                if user == client.user:
                    if len(message.attachments) > 0:
                        for attachment in message.attachments:
                            if attachment.url.endswith('.jpg') \
                            or attachment.url.endswith('.jpeg') \
                            or attachment.url.endswith('.png'):
                                # remove leaderboard point
                                score = int(get_leaderboard_user_score(conn, message.author.id)[0][0]) # [0][0] for getting the actual value out of list of tuples
                                if score > 0:
                                    score -= 1
                                else:
                                    score = 0
                                update_leaderboard_entry_score(conn, (score, message.author.id))
                                break

@client.event
async def on_ready():
    print('The bot is ready!')

# -------------------------------- DATABASE STUFF -------------------------------- #

# create a connection to the SQLite database
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn

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
    sql = 'INSERT INTO Leaderboard(userid,postcount,score) VALUES(?,?,?)'
    cur = conn.cursor()
    cur.execute(sql, leaderboardEntry)
    return cur.lastrowid

# update leaderboard entry score
def update_leaderboard_entry_score(conn, leaderboardEntry):
    sql = 'UPDATE Leaderboard SET score = ? WHERE userid = ?'
    cur = conn.cursor()
    cur.execute(sql, leaderboardEntry)
    conn.commit()

# update leaderboard entry postcount
def update_leaderboard_entry_postcount(conn, leaderboardEntry):
    sql = 'UPDATE Leaderboard SET postcount = ? WHERE userid = ?'
    cur = conn.cursor()
    cur.execute(sql, leaderboardEntry)
    conn.commit()

# get the whole leaderboard
def get_leaderboard(conn):
    cur = conn.cursor()
    cur.execute('SELECT * FROM Leaderboard')

    rows = cur.fetchall()
    return rows

# get all users currently in the leaderboard
def get_leaderboard_users(conn):
    cur = conn.cursor()
    cur.execute('SELECT userid FROM Leaderboard')

    rows = cur.fetchall()
    return rows

# get the score of a specific user from the leaderboard
def get_leaderboard_user_score(conn, userid):
    cur = conn.cursor()
    cur.execute('SELECT score FROM Leaderboard WHERE userid = ?', (userid,))

    row = cur.fetchall()
    return row
    
# get the postcount of a specific user from the leaderboard
def get_leaderboard_user_postcount(conn, userid):
    cur = conn.cursor()
    cur.execute('SELECT postcount FROM Leaderboard WHERE userid = ?', (userid,))

    row = cur.fetchall()
    return row

# ---------------------------------- UTILITIES ---------------------------------- #

# for leaderboard list sorting
def sortKey(element):
    return element[4]

# get the bot's unique token from a file
def getToken():
    with open ('TOKEN', 'r') as t:
        TOKEN = t.read()
    return TOKEN

# ---------------------------------- MAIN CODE ---------------------------------- #

def main():
    # create database
    database = os.getcwd() + os.sep + 'foundation.db'
    conn = create_connection(database)
    if conn is not None:
    # create leaderboard table
        create_leaderboard_table(conn)
    else:
        print('Error! cannot create the database connection!')
    # get all users already in the database and convert list of tuples to plain list
    leaderboard = list(sum(get_leaderboard_users(conn), ()))
    # get the bot's unique token
    TOKEN = getToken()
    return conn, leaderboard, TOKEN

if __name__ == '__main__':
    conn, leaderboard, TOKEN = main()
    # start bot
    client.run(TOKEN)
'''----------------------------------------------------------------------------\
| ||\\    //||       /|¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯\ |
| || \\  // ||  (o_ / |                  SUPPLEMENTARY FILE                  | |
| ||  \\//  ||  //\/  |                         ----                         | |
| ||   \/   ||  V_/_  |                  LEADERBOARD SYSTEM                  | |
| ||        ||        |‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗/ |
\----------------------------------------------------------------------------'''

import discord
from discord.ext import commands, tasks
from datetime import datetime, timezone

# Import database methods
from foundationBotDatabaseStuff import *

# import logger
from foundationBotLogger import *
logger = Logger()

# Screenshot Leaderboard Entry Object
class screenshotLeaderboardEntry:
    def __init__(self):
        self.screenshotID = None
        self.score = None

# Messages Leaderboard Entry Object
class messagesLeaderboardEntry:
    def __init__(self):
        self.userID = None
        self.score = None

# Leaderboard System Class
class leaderboardSystem:
    def __init__(self):
        self.screenshotLeaderboard = []
        self.messagesLeaderboard = []
        self.screenshotSaveList = []
        self.messagesSaveList = []
    
    def getScreenshotLeaderboard(self):
        return self.screenshotLeaderboard
    
    def setScreenshotLeaderboard(self, sl):
        self.screenshotLeaderboard = sl
    
    def getScreenshotLeaderboardEntry(self, screenshotID):
        for entry in self.screenshotLeaderboard:
            if entry.screenshotID == screenshotID:
                return entry
    
    def createScreenshotLeaderboardEntry(self, sle):
        self.screenshotLeaderboard.append(sle)
    
    def setScreenshotLeaderboardEntryScore(self, sle):
        for entry in self.screenshotLeaderboard:
            if entry.screenshotID == sle.screenshotID:
                entry.score = sle.score
    
    def getScreenshotSaveList(self):
        return self.screenshotSaveList
    
    def clearScreenshotSaveList(self):
        self.screenshotSaveList = []
    
    def createScreenshotSaveListEntry(self, sle):
        self.screenshotSaveList.append(sle)
    
    def setScreenshotSaveListEntryScore(self, sle):
        for entry in self.screenshotSaveList:
            if entry.screenshotID == sle.screenshotID:
                entry.score = sle.score
    
    def getMessagesLeaderboard(self):
        return self.messagesLeaderboard
    
    def setMessagesLeaderboard(self, ml):
        self.messagesLeaderboard = ml
    
    def getMessagesLeaderboardEntry(self, userID):
        for entry in self.messagesLeaderboard:
            if entry.userID == userID:
                return entry
    
    def createMessagesLeaderboardEntry(self, mle):
        self.messagesLeaderboard.append(mle)
    
    def setMessagesLeaderboardEntryScore(self, mle):
        for entry in self.messagesLeaderboard:
            if entry.userID == mle.userID:
                entry.score = mle.score
    
    def getMessagesSaveList(self):
        return self.messagesSaveList
    
    def clearMessagesSaveList(self):
        self.messagesSaveList = []
    
    def createMessagesSaveListEntry(self, mle):
        self.messagesSaveList.append(mle)
    
    def setMessagesSaveListEntryScore(self, mle):
        for entry in self.messagesSaveList:
            if entry.userID == mle.userID:
                entry.score = mle.score
    
class LeaderboardPost(commands.Cog):
    def __init__(self, bot, conn, settings, leaderboardSystem):
        self.bot = bot
        self.conn = conn
        self.settings = settings
        self.leaderboardSystem = leaderboardSystem
        self.post.start()
    
    @tasks.loop(minutes=1.0)
    async def post(self):
        logger.getLogger().info('Leaderboard Postcheck Loop Started')
        if self.settings.messagesPostTime != None:
            if datetime.now(timezone.utc).timestamp() >= self.settings.messagesPostTime:
                guild = self.bot.get_guild(self.settings.guildID)
                leaderboard = self.leaderboardSystem.getMessagesLeaderboard()
                self.leaderboardSystem.setMessagesLeaderboard([])
                self.leaderboardSystem.clearMessagesSaveList()
                clear_messages_leaderboard(self.conn)
                create_messages_leaderboard_table(self.conn)
                self.settings.messagesPostTime += self.settings.leaderboardInterval*24*3600
                update_setting(self.conn, (self.settings.messagesPostTime,'messagesPostTime'))
                if len(leaderboard) > 0:
                    formattedleaderboard = [[0]*2 for i in range(len(leaderboard))]
                    for i,entry in enumerate(leaderboard):
                        if guild.get_member(entry.userID) != None: # check if user is still in the server
                            formattedleaderboard[i][0] = guild.get_member(entry.userID).display_name # userid converted to display name
                            formattedleaderboard[i][1] = entry.score
                        else:
                            continue
                    formattedleaderboard.sort(key=lambda x: x[1], reverse = True)
                    users = ''
                    scores = ''
                    for i,entry in enumerate(formattedleaderboard):
                        if i < 10:
                            users += entry[0] + '\n'
                            scores += str(entry[1]) + '\n'
                        else:
                            break
                    embed = discord.Embed(
                            title = 'Messages Leaderboard Week ' + str(datetime.now(timezone.utc).isocalendar()[1]),
                            #description = '',
                            colour = discord.Colour.dark_green()
                            )
                    embed.add_field(name='Username' , value=users, inline=True)
                    embed.add_field(name='Score', value=scores, inline=True)
                    await guild.get_channel(self.settings.leaderboardChannel).send(embed=embed)
        
        if self.settings.screenshotPostTime != None:
            if datetime.now(timezone.utc).timestamp() >= self.settings.screenshotPostTime:
                guild = self.bot.get_guild(self.settings.guildID)
                leaderboard = self.leaderboardSystem.getScreenshotLeaderboard()
                self.leaderboardSystem.setScreenshotLeaderboard([])
                self.leaderboardSystem.clearScreenshotSaveList()
                clear_screenshot_leaderboard(self.conn)
                create_screenshot_leaderboard_table(self.conn)
                self.settings.screenshotPostTime += self.settings.leaderboardInterval*24*3600
                update_setting(self.conn, (self.settings.screenshotPostTime,'screenshotPostTime'))
                if len(leaderboard) > 0:
                    winningEntry = leaderboard[0]
                    for entry in leaderboard:
                        if entry.score > winningEntry.score:
                            winningEntry = entry
                    if any(entry.score == winningEntry.score for entry in leaderboard):
                        winningEntries = []
                        for entry in leaderboard:
                            if entry.score == winningEntry.score:
                                winningEntries.append(entry)
                    if self.settings.screenshotChannel != None:
                        for entry in winningEntries:
                            message = await guild.get_channel(self.settings.screenshotChannel).fetch_message(entry.screenshotID)
                            if message.author != None:
                                embed = discord.Embed(
                                        title = 'Screenshot Leaderboard Week ' + str(datetime.now(timezone.utc).isocalendar()[1]),
                                        description = 'Winner: ' + message.author.display_name + ' with ' + str(entry.score) + ' Votes!',
                                        colour = discord.Colour.dark_green()
                                        )
                                for attachment in message.attachments:
                                    embed.set_image(url=attachment.url)
                                    break
                                await guild.get_channel(self.settings.leaderboardChannel).send(embed=embed)
    
    @post.before_loop
    async def before_post(self):
        await self.bot.wait_until_ready()
'''------------------------------Version 1.0.0---------------------------------\
| ||\\    //||       /|¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯\ |
| || \\  // ||  (o_ / | Run: python3 foundationBot.py                        | |
| ||  \\//  ||  //\/  | In:  TOKEN                                           | |
| ||   \/   ||  V_/_  | Out: foundationBot.db, foundationBot.log             | |
| ||        ||        |‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗/ |
\----------------------------------------------------------------------------'''

import discord
from discord.ext import commands
import sqlite3
from sqlite3 import Error
from datetime import timezone
import os

# Import database methods
from foundationBotDatabaseStuff import *

# Import supplementary classes
from foundationBotLeaderboard import *
from foundationBotRanking import *
from foundationBotHelpCommands import *
from foundationBotSettingsCommands import *
from foundationBotUtils import *
from foundationBotLogger import *

# Instantiate settings object
settings = Settings()

# Instantiate supplementary classes
leaderboardSystem = leaderboardSystem()
rankingSystem = rankingSystem()
utils = Utils(settings, rankingSystem)
logger = Logger()

# ----------------------------------- GENERAL ----------------------------------- #

# Special Permissions Required: 
# Manage Roles
# Read Text Channels & See Voice Channels
# Send Messages
# Manage Messages
# Read Message History
# Mention @everyone, @here, and All Roles
# Add Reactions

# intents definition i.e. what events/methods the bot has access to
intents = discord.Intents(
                          guilds = True,
                          members = True, # needs activation on discord dev portal
                          emojis = True,
                          guild_messages = True,
                          guild_reactions = True,
                          
                          bans = False,
                          integrations = False,
                          webhooks = False,
                          invites = False,
                          voice_states = False,
                          presences = False, # needs activation on discord dev portal
                          dm_messages = False,
                          dm_reactions = False,
                          guild_typing = False,
                          dm_typing = False
                         )

# --------------------------- DISCORD EVENT LISTENERS --------------------------- #

bot = commands.Bot(command_prefix='/', help_command=None, intents=intents)

@bot.event
async def on_message(message):
    if settings.botActive is True:
        # the bot shouldn't reply to itself
        if message.author == bot.user:
            return
        
        # the channel the message was sent in
        channel = message.channel
        
        # screenshot leaderboard system
        if not any(role.id == settings.excludedRoles for role in message.author.roles):
            if channel.id == settings.screenshotChannel:
                if settings.screenshotPostTime != None:
                    if message.created_at.replace(tzinfo=timezone.utc).timestamp() > settings.screenshotPostTime - settings.leaderboardInterval*24*3600:
                        if len(message.attachments) > 0:
                            for attachment in message.attachments:
                                if attachment.url.lower().endswith('.jpg') \
                                or attachment.url.lower().endswith('.jpeg') \
                                or attachment.url.lower().endswith('.png'):
                                    sle = screenshotLeaderboardEntry()
                                    sle.screenshotID = message.id
                                    sle.score = 0
                                    leaderboardSystem.createScreenshotLeaderboardEntry(sle)
                                    leaderboardSystem.createScreenshotSaveListEntry(sle)
                                    await message.add_reaction(discord.utils.get(channel.guild.emojis, id=settings.leaderboardEmoji))
                                    break
        
        # messages leaderboard system
        if not any(role.id == settings.excludedRoles for role in message.author.roles):
            if settings.messagesPostTime != None:
                if message.created_at.replace(tzinfo=timezone.utc).timestamp() > settings.messagesPostTime - settings.leaderboardInterval*24*3600:
                    # check if user is already in the messages leaderboard
                    if not any(entry.userID == message.author.id for entry in leaderboardSystem.getMessagesLeaderboard()):
                        mle = messagesLeaderboardEntry()
                        mle.userID = message.author.id
                        mle.score = 1
                        leaderboardSystem.createMessagesLeaderboardEntry(mle)
                        leaderboardSystem.createMessagesSaveListEntry(mle)
                    else:
                        # add to score since it is not the first post
                        mle = leaderboardSystem.getMessagesLeaderboardEntry(message.author.id)
                        if mle != None:
                            mle.score += 1
                            leaderboardSystem.setMessagesLeaderboardEntryScore(mle)
                            if any(entry.userID == message.author.id for entry in leaderboardSystem.getMessagesSaveList()):
                                leaderboardSystem.setMessagesSaveListEntryScore(mle)
                            else:
                                leaderboardSystem.createMessagesSaveListEntry(mle)
        
        # ranking system
        if not any(entry == message.author.id for entry in rankingSystem.getCooldownList()):
            rankingSystem.createCooldownListEntry(message.author.id)
            rsc = RankingSystemCooldown(rankingSystem)
            rsc.cooldown.start(message.author.id)
            if not any(entry.userID == message.author.id for entry in rankingSystem.getRankingTable()):
                dr = message.guild.get_role(settings.defaultRole)
                hr = message.guild.get_role(settings.highestRole)
                rc = message.guild.get_channel(settings.rankingChannel)
                if (dr != None and rc != None and hr != None):
                    re = rankingEntry()
                    re.userID = message.author.id
                    re.experience = 1
                    re.estate = 'Labour'
                    re.rank = settings.defaultRole
                    re.gender = 'Male'
                    rankingSystem.createRankingEntry(re)
                    rankingSystem.createSaveListEntry(re)
                    await message.channel.send('A new villager has arrived! Welcome ' + message.author.mention + '!\n' +
                                               'You are now a **' + dr.name + '** on the **Labour** estate path to greatness!\n' +
                                               'To earn experience towards ranks simply continue being active and talking within the community!\nWill you make it to **' + hr.name + '**? Only time will tell...\n\n'
                                               'Note: You can switch to the **Clergy** or **Kingdom** estate paths at any time by reacting to their respective emojis in ' + rc.mention + 
                                               '. To switch back into the **Labour** estate path simply react to the Labour emoji in the same channel.')
                    await message.author.add_roles(message.author.guild.get_role(settings.defaultRole))
            else:
                re = rankingSystem.getRankingEntry(message.author.id)
                if re != None:
                    re.experience += 1
                    rankCheck, msg = await utils.checkRank(message.author, re)
                    file, embed = utils.createRankEmbed(message.author, re)
                    if rankCheck is True:
                        await message.channel.send(msg, file=file, embed=embed)
                    rankingSystem.setRankingEntryExp(re)
                    if any(entry.userID == message.author.id for entry in rankingSystem.getSaveList()):
                        rankingSystem.setSaveListEntryExp(re)
                    else:
                        rankingSystem.createSaveListEntry(re)
        
    await bot.process_commands(message)

@bot.event
async def on_raw_reaction_add(payload):
    if settings.botActive is True:
        # the bot shouldn't reply to itself
        if payload.member == bot.user:
            return
        
        emoji = payload.emoji
        # message pinning system
        if str(emoji) == '📌':
            member = payload.member
            # check the emoji was used by a player with the allowed role to pin
            for role in settings.pinsRoles:
                if discord.utils.get(member.guild.roles, id=role) in member.roles:
                    origChannel = bot.get_channel(payload.channel_id) 
                    message = await origChannel.fetch_message(payload.message_id)
                    postChannel = bot.get_channel(settings.pinsChannel) 
                    url = message.jump_url
                    embed = discord.Embed(
                        description = message.content,
                        colour = discord.Colour.dark_green()
                    )
                    embed.set_author(name=message.author.display_name + ' on ' + message.created_at.strftime('%d/%m/%Y, %H:%M') +  ' UTC')
                    embed.set_footer(text='Pinned by: ' + member.display_name )
                    await postChannel.send(url, embed=embed)
                    break
        
        # screenshot leaderboard system
        elif emoji.id == settings.leaderboardEmoji:
            channel = bot.get_channel(payload.channel_id)
            if channel.id == settings.screenshotChannel:
                message = await channel.fetch_message(payload.message_id)
                if message.created_at.replace(tzinfo=timezone.utc).timestamp() > settings.screenshotPostTime - settings.leaderboardInterval*24*3600:
                    # check if the bot has reacted to the screenshot
                    async for user in discord.utils.get(message.reactions, emoji=emoji).users():
                        if user == bot.user:
                            if len(message.attachments) > 0:
                                for attachment in message.attachments:
                                    if attachment.url.endswith('.jpg') \
                                    or attachment.url.endswith('.jpeg') \
                                    or attachment.url.endswith('.png'):
                                        # add leaderboard point
                                        le = leaderboardSystem.getScreenshotLeaderboardEntry(message.id)
                                        if le != None:
                                            le.score += 1
                                            leaderboardSystem.setScreenshotLeaderboardEntryScore(le)
                                            if any(entry.screenshotID == message.id for entry in leaderboardSystem.getScreenshotSaveList()):
                                                leaderboardSystem.setScreenshotSaveListEntryScore(le)
                                            else:
                                                leaderboardSystem.createScreenshotSaveListEntry(le)
                                        break
        
        # ranking system estate change
        elif emoji.id == settings.labourEmoji:
            if payload.channel_id == settings.rankingChannel:
                if payload.message_id == settings.rankingMessage:
                    if any(entry.userID == payload.member.id for entry in rankingSystem.getRankingTable()):
                        re = rankingSystem.getRankingEntry(payload.member.id)
                        if re != None:
                            if re.estate != 'Labour':
                                re.estate = 'Labour'
                                rankingSystem.setRankingEntryEstate(re)
                                if any(entry.userID == payload.member.id for entry in rankingSystem.getSaveList()):
                                    rankingSystem.setSaveListEntryEstate(re)
                                else:
                                    rankingSystem.createSaveListEntry(re)
        
        elif emoji.id == settings.clergyEmoji:
            if payload.channel_id == settings.rankingChannel:
                if payload.message_id == settings.rankingMessage:
                    if any(entry.userID == payload.member.id for entry in rankingSystem.getRankingTable()):
                        re = rankingSystem.getRankingEntry(payload.member.id)
                        if re != None:
                            if re.estate != 'Clergy':
                                re.estate = 'Clergy'
                                rankingSystem.setRankingEntryEstate(re)
                                if any(entry.userID == payload.member.id for entry in rankingSystem.getSaveList()):
                                    rankingSystem.setSaveListEntryEstate(re)
                                else:
                                    rankingSystem.createSaveListEntry(re)
        
        elif emoji.id == settings.kingdomEmoji:
            if payload.channel_id == settings.rankingChannel:
                if payload.message_id == settings.rankingMessage:
                    if any(entry.userID == payload.member.id for entry in rankingSystem.getRankingTable()):
                        re = rankingSystem.getRankingEntry(payload.member.id)
                        if re != None:
                            if re.estate != 'Kingdom':
                                re.estate = 'Kingdom'
                                rankingSystem.setRankingEntryEstate(re)
                                if any(entry.userID == payload.member.id for entry in rankingSystem.getSaveList()):
                                    rankingSystem.setSaveListEntryEstate(re)
                                else:
                                    rankingSystem.createSaveListEntry(re)
        
        elif str(emoji) == '♂':
            if payload.channel_id == settings.rankingChannel:
                if payload.message_id == settings.rankingMessage:
                    if any(entry.userID == payload.member.id for entry in rankingSystem.getRankingTable()):
                        re = rankingSystem.getRankingEntry(payload.member.id)
                        if re != None:
                            if re.gender != 'Male':
                                re.gender = 'Male'
                                rankingSystem.setRankingEntryGender(re)
                                if any(entry.userID == payload.member.id for entry in rankingSystem.getSaveList()):
                                    rankingSystem.setSaveListEntryGender(re)
                                else:
                                    rankingSystem.createSaveListEntry(re)
        
        elif str(emoji) == '♀':
            if payload.channel_id == settings.rankingChannel:
                if payload.message_id == settings.rankingMessage:
                    if any(entry.userID == payload.member.id for entry in rankingSystem.getRankingTable()):
                        re = rankingSystem.getRankingEntry(payload.member.id)
                        if re != None:
                            if re.gender != 'Female':
                                re.gender = 'Female'
                                rankingSystem.setRankingEntryGender(re)
                                if any(entry.userID == payload.member.id for entry in rankingSystem.getSaveList()):
                                    rankingSystem.setSaveListEntryGender(re)
                                else:
                                    rankingSystem.createSaveListEntry(re)

@bot.event
async def on_raw_reaction_remove(payload):
    if settings.botActive is True:
        emoji = payload.emoji
        # screenshot leaderboard system
        if emoji.id == settings.leaderboardEmoji:
            channel = bot.get_channel(payload.channel_id)
            if channel.id == settings.screenshotChannel:
                message = await channel.fetch_message(payload.message_id)
                if message.created_at.replace(tzinfo=timezone.utc).timestamp() > settings.screenshotPostTime - settings.leaderboardInterval*24*3600:
                    # check if the bot has reacted to the screenshot
                    async for user in discord.utils.get(message.reactions, emoji=emoji).users():
                        if user == bot.user:
                            if len(message.attachments) > 0:
                                for attachment in message.attachments:
                                    if attachment.url.endswith('.jpg') \
                                    or attachment.url.endswith('.jpeg') \
                                    or attachment.url.endswith('.png'):
                                        # remove leaderboard point
                                        sle = leaderboardSystem.getScreenshotLeaderboardEntry(message.id)
                                        if sle != None:
                                            if sle.score > 0:
                                                sle.score -= 1
                                            else:
                                                sle.score = 0
                                            leaderboardSystem.setScreenshotLeaderboardEntryScore(sle)
                                            if any(entry.screenshotID == message.id for entry in leaderboardSystem.getScreenshotSaveList()):
                                                leaderboardSystem.setScreenshotSaveListEntryScore(sle)
                                            else:
                                                leaderboardSystem.createScreenshotSaveListEntry(sle)
                                        break

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('Insufficient Permissions! Required Permissions: `' + str(error.missing_perms).strip('\'[]') + '`')
    elif isinstance(error, commands.MissingRequiredArgument):
        if ctx.command.parent != None:
            if ctx.command.parent.name == 'set':
                await ctx.send('Missing Required Argument! Consult `/set help` for more information!')
        else:
            await ctx.send('Missing Required Argument! Consult `/help` for more information!')
    elif isinstance(error, commands.errors.CommandNotFound):
        logger.getLogger().error(error)
        pass
    elif isinstance(error, commands.NoPrivateMessage):
        logger.getLogger().error(error)
        pass
    else:
        logger.getLogger().error(error)

@bot.event
async def on_ready():
    logger.getLogger().info('The bot is ready!')
    #await client.change_presence(activity=discord.Game(name='Support @ mino.gg'))

class GeneralCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # player rank display command
    @commands.guild_only()
    @commands.command(description='Displays your current rank')
    async def rank(self, ctx):
        re = rankingSystem.getRankingEntry(ctx.author.id)
        file, embed = utils.createRankEmbed(ctx.author, re)
        await ctx.send(file=file, embed=embed)
    
    @commands.command(description='Test Command')
    async def test(self, ctx):
        prog = utils.progress(1, 2)
        percentage = 50.0
        embed = discord.Embed(
                title = 'Testing Embed for Rank Images',
                colour = discord.Colour.dark_green()
            )
        embed.add_field(name='Progress to Next Rank: ' + str(percentage) + '%', value='curRankName ' + prog + ' nextRankName')
        basepath = os.getcwd() + os.sep + 'levels' + os.sep
        
        await ctx.send('Newcomer')
        genderstr = os.sep + 'male' + os.sep
        file = discord.File(basepath + 'other' + genderstr + 'defaultRole.png', filename='image.png')
        embed.set_thumbnail(url='attachment://image.png')
        await ctx.send(file=file, embed=embed)
        genderstr = os.sep + 'female' + os.sep
        file = discord.File(basepath + 'other' + genderstr + 'defaultRole.png', filename='image.png')
        embed.set_thumbnail(url='attachment://image.png')
        await ctx.send(file=file, embed=embed)
        
        await ctx.send('Labour Path')
        genderstr = os.sep + 'male' + os.sep
        file = discord.File(basepath + 'labour' + genderstr + 'labourRole1.png', filename='image.png')
        embed.set_thumbnail(url='attachment://image.png')
        await ctx.send(file=file, embed=embed)
        file = discord.File(basepath + 'labour' + genderstr + 'labourRole2.png', filename='image.png')
        embed.set_thumbnail(url='attachment://image.png')
        await ctx.send(file=file, embed=embed)
        file = discord.File(basepath + 'labour' + genderstr + 'labourRole3.png', filename='image.png')
        embed.set_thumbnail(url='attachment://image.png')
        await ctx.send(file=file, embed=embed)
        file = discord.File(basepath + 'labour' + genderstr + 'labourRole4.png', filename='image.png')
        embed.set_thumbnail(url='attachment://image.png')
        await ctx.send(file=file, embed=embed)
        genderstr = os.sep + 'female' + os.sep
        file = discord.File(basepath + 'labour' + genderstr + 'labourRole1.png', filename='image.png')
        embed.set_thumbnail(url='attachment://image.png')
        await ctx.send(file=file, embed=embed)
        file = discord.File(basepath + 'labour' + genderstr + 'labourRole2.png', filename='image.png')
        embed.set_thumbnail(url='attachment://image.png')
        await ctx.send(file=file, embed=embed)
        file = discord.File(basepath + 'labour' + genderstr + 'labourRole3.png', filename='image.png')
        embed.set_thumbnail(url='attachment://image.png')
        await ctx.send(file=file, embed=embed)
        file = discord.File(basepath + 'labour' + genderstr + 'labourRole4.png', filename='image.png')
        embed.set_thumbnail(url='attachment://image.png')
        await ctx.send(file=file, embed=embed)
        
        await ctx.send('Clergy Path')
        genderstr = os.sep + 'male' + os.sep
        file = discord.File(basepath + 'clergy' + genderstr + 'clergyRole1.png', filename='image.png')
        embed.set_thumbnail(url='attachment://image.png')
        await ctx.send(file=file, embed=embed)
        file = discord.File(basepath + 'clergy' + genderstr + 'clergyRole2.png', filename='image.png')
        embed.set_thumbnail(url='attachment://image.png')
        await ctx.send(file=file, embed=embed)
        file = discord.File(basepath + 'clergy' + genderstr + 'clergyRole3.png', filename='image.png')
        embed.set_thumbnail(url='attachment://image.png')
        await ctx.send(file=file, embed=embed)
        file = discord.File(basepath + 'clergy' + genderstr + 'clergyRole4.png', filename='image.png')
        embed.set_thumbnail(url='attachment://image.png')
        await ctx.send(file=file, embed=embed)
        
        await ctx.send('Kingdom Path')
        genderstr = os.sep + 'male' + os.sep
        file = discord.File(basepath + 'kingdom' + genderstr + 'kingdomRole1.png', filename='image.png')
        embed.set_thumbnail(url='attachment://image.png')
        await ctx.send(file=file, embed=embed)
        file = discord.File(basepath + 'kingdom' + genderstr + 'kingdomRole2.png', filename='image.png')
        embed.set_thumbnail(url='attachment://image.png')
        await ctx.send(file=file, embed=embed)
        file = discord.File(basepath + 'kingdom' + genderstr + 'kingdomRole3.png', filename='image.png')
        embed.set_thumbnail(url='attachment://image.png')
        await ctx.send(file=file, embed=embed)
        file = discord.File(basepath + 'kingdom' + genderstr + 'kingdomRole4.png', filename='image.png')
        embed.set_thumbnail(url='attachment://image.png')
        await ctx.send(file=file, embed=embed)
        genderstr = os.sep + 'female' + os.sep
        file = discord.File(basepath + 'kingdom' + genderstr + 'kingdomRole1.png', filename='image.png')
        embed.set_thumbnail(url='attachment://image.png')
        await ctx.send(file=file, embed=embed)
        file = discord.File(basepath + 'kingdom' + genderstr + 'kingdomRole2.png', filename='image.png')
        embed.set_thumbnail(url='attachment://image.png')
        await ctx.send(file=file, embed=embed)
        file = discord.File(basepath + 'kingdom' + genderstr + 'kingdomRole3.png', filename='image.png')
        embed.set_thumbnail(url='attachment://image.png')
        await ctx.send(file=file, embed=embed)
        file = discord.File(basepath + 'kingdom' + genderstr + 'kingdomRole4.png', filename='image.png')
        embed.set_thumbnail(url='attachment://image.png')
        await ctx.send(file=file, embed=embed)
        
        await ctx.send('High Lord')
        genderstr = os.sep + 'male' + os.sep
        file = discord.File(basepath + 'other' + genderstr + 'highestRole.png', filename='image.png')
        embed.set_thumbnail(url='attachment://image.png')
        await ctx.send(file=file, embed=embed)
        genderstr = os.sep + 'female' + os.sep
        file = discord.File(basepath + 'other' + genderstr + 'highestRole.png', filename='image.png')
        embed.set_thumbnail(url='attachment://image.png')
        await ctx.send(file=file, embed=embed)

class AdminCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # award exp command
    @commands.guild_only()
    @commands.command(description='Awards a player an amount of server experience')
    @commands.has_guild_permissions(administrator=True)
    async def awardExp(self, ctx, exp: str, memberid: str):
        try:
            member = ctx.guild.get_member(int(memberid))
            if member != None:
                try:
                    exp = int(exp)
                    re = rankingSystem.getRankingEntry(member.id)
                    if re != None:
                        re.experience += exp
                        await ctx.send(ctx.author.mention + ' awarded ' + str(exp) + ' experience points to ' + member.mention)
                        rankingSystem.setRankingEntryExp(re)
                        if any(entry.userID == member.id for entry in rankingSystem.getSaveList()):
                            rankingSystem.setSaveListEntryExp(re)
                        else:
                            rankingSystem.createSaveListEntry(re)
                except ValueError as e:
                    await ctx.send('Invalid Experience Amount! The experience to award should only consist of an integer number!')
            else:
                await ctx.send('Invalid User ID! No member found with the specified ID!')
        except ValueError as e:
            await ctx.send('Invalid User ID! The user id should only consist of an integer number!')

# ---------------------------------- MAIN CODE ---------------------------------- #

def main():
    # create database
    database = os.getcwd() + os.sep + 'foundationBot.db'
    logger.getLogger().info('Database Path: ' + database)
    conn = create_connection(database)
    logger.getLogger().info('Connection Successful')
    if conn is not None:
        # create leaderboard tables
        create_screenshot_leaderboard_table(conn)
        create_messages_leaderboard_table(conn)
        # create ranking table
        create_ranking_table(conn)
        # create settings table
        create_settings_table(conn)
        # initialise settings table
        init_settings(conn)
        settingsList = get_settings(conn)
        settings.setSettings(settingsList)
        logger.getLogger().info('Settings Initialised Successfully')
    else:
        logger.getLogger().error('Error! cannot create the database connection!')
    
    leaderboardraw = get_screenshot_leaderboard(conn)
    leaderboard = []
    for entry in leaderboardraw:
        sle = screenshotLeaderboardEntry()
        sle.screenshotID = entry[1]
        sle.score = entry[2]
        leaderboard.append(sle)
    leaderboardSystem.setScreenshotLeaderboard(leaderboard)
    
    leaderboardraw = get_messages_leaderboard(conn)
    leaderboard = []
    for entry in leaderboardraw:
        mle = messagesLeaderboardEntry()
        mle.userID = entry[1]
        mle.score = entry[2]
        leaderboard.append(mle)
    leaderboardSystem.setMessagesLeaderboard(leaderboard)
    
    rankingtableraw = get_ranking_table(conn)
    rankingtable = []
    for entry in rankingtableraw:
        re = rankingEntry()
        re.userID = entry[1]
        re.experience = entry[2]
        re.estate = entry[3]
        re.rank = entry[4]
        re.gender = entry[5]
        rankingtable.append(re)
    rankingSystem.setRankingTable(rankingtable)
    
    # get the bot's unique token
    TOKEN = utils.getToken()
    return conn, TOKEN

if __name__ == '__main__':
    conn, TOKEN = main()
    
    # add all cog classes
    bot.add_cog(HelpCommands(bot, settings))
    bot.add_cog(GeneralCommands(bot))
    bot.add_cog(AdminCommands(bot))
    bot.add_cog(SettingsCommands(bot, conn, settings))
    bot.add_cog(DatabaseWrite(bot, conn, rankingSystem, leaderboardSystem))
    bot.add_cog(LeaderboardPost(bot, conn, settings, leaderboardSystem))
    
    # start bot
    bot.run(TOKEN)

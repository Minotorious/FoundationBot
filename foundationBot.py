'''------------------------------Version 1.0.0---------------------------------\
| ||\\    //||       /|¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯\ |
| || \\  // ||  (o_ / | Run: python3 foundationBot.py                        | |
| ||  \\//  ||  //\/  | In:  TOKEN                                           | |
| ||   \/   ||  V_/_  | Out: foundation.db                                   | |
| ||        ||        |‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗/ |
\----------------------------------------------------------------------------'''

import discord
from discord.ext import commands, tasks
import sqlite3
from sqlite3 import Error
import os
from math import floor

# Import database methods
from foundationBotDatabaseStuff import *

# Import supplementary classes
from foundationBotLeaderboard import *
from foundationBotRanking import *

# ------------------------------ GENERAL SETTINGS ------------------------------- #

# Special Permissions Required: Manage Roles

# --------------------------- DISCORD EVENT LISTENERS --------------------------- #

bot = commands.Bot(command_prefix='/', help_command=None)

@bot.event
async def on_message(message):
    if settings.botActive is True:
        # the bot shouldn't reply to itself
        if message.author == bot.user:
            return
        
        # the channel the message was sent in
        channel = message.channel
        
        # screenshot leaderboard system
        if channel.id == settings.leaderboardChannel:
            if len(message.attachments) > 0:
                for attachment in message.attachments:
                    if attachment.url.lower().endswith('.jpg') \
                    or attachment.url.lower().endswith('.jpeg') \
                    or attachment.url.lower().endswith('.png'):
                        # check if user is already in the leaderboard
                        if not any(entry.userID == message.author.id for entry in leaderboardSystem.getLeaderboard()):
                            le = leaderboardEntry()
                            le.userID = message.author.id
                            le.score = 0
                            le.postCount = 1
                            leaderboardSystem.createLeaderboardEntry(le)
                            leaderboardSystem.createSaveListEntry(le)
                            await message.add_reaction(discord.utils.get(channel.guild.emojis, id=settings.leaderboardEmoji))
                            break
                        else:
                            # add to postcount since it is not the first post
                            le = leaderboardSystem.getLeaderboardEntry(message.author.id)
                            if le != None:
                                le.postCount += 1
                                leaderboardSystem.setLeaderboardEntryPostCount(le)
                                if any(entry.userID == message.author.id for entry in leaderboardSystem.getSaveList()):
                                    leaderboardSystem.setSaveListEntryPostCount(le)
                                else:
                                    leaderboardSystem.createSaveListEntry(le)
                            await message.add_reaction(discord.utils.get(channel.guild.emojis, id=settings.leaderboardEmoji))
                            break
        
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
                    rankCheck, msg = await checkRank(message.author, re)
                    if rankCheck is True:
                        await message.channel.send(msg)
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
            if channel.id == settings.leaderboardChannel:
                message = await channel.fetch_message(payload.message_id)
                # check if the bot has reacted to the screenshot
                async for user in discord.utils.get(message.reactions, emoji=emoji).users():
                    if user == bot.user:
                        if len(message.attachments) > 0:
                            for attachment in message.attachments:
                                if attachment.url.endswith('.jpg') \
                                or attachment.url.endswith('.jpeg') \
                                or attachment.url.endswith('.png'):
                                    # add leaderboard point
                                    le = leaderboardSystem.getLeaderboardEntry(message.author.id)
                                    if le != None:
                                        le.score += 1
                                        leaderboardSystem.setLeaderboardEntryScore(le)
                                        if any(entry.userID == message.author.id for entry in leaderboardSystem.getSaveList()):
                                            leaderboardSystem.setSaveListEntryScore(le)
                                        else:
                                            leaderboardSystem.createSaveListEntry(le)
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

@bot.event
async def on_raw_reaction_remove(payload):
    if settings.botActive is True:
        emoji = payload.emoji
        # screenshot leaderboard system
        if emoji.id == settings.leaderboardEmoji:
            channel = bot.get_channel(payload.channel_id)
            if channel.id == settings.leaderboardChannel:
                message = await channel.fetch_message(payload.message_id)
                # check if the bot has reacted to the screenshot
                async for user in discord.utils.get(message.reactions, emoji=emoji).users():
                    if user == bot.user:
                        if len(message.attachments) > 0:
                            for attachment in message.attachments:
                                if attachment.url.endswith('.jpg') \
                                or attachment.url.endswith('.jpeg') \
                                or attachment.url.endswith('.png'):
                                    # remove leaderboard point
                                    le = leaderboardSystem.getLeaderboardEntry(message.author.id)
                                    if le != None:
                                        if le.score > 0:
                                            le.score -= 1
                                        else:
                                            le.score = 0
                                        leaderboardSystem.setLeaderboardEntryScore(le)
                                        if any(entry.userID == message.author.id for entry in leaderboardSystem.getSaveList()):
                                            leaderboardSystem.setSaveListEntryScore(le)
                                        else:
                                            leaderboardSystem.createSaveListEntry(le)
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
        pass
    elif isinstance(error, commands.NoPrivateMessage):
        pass
    else:
        print(error)

@bot.event
async def on_ready():
    print('The bot is ready!')

class HelpCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # dxdiag help command
    @commands.command(description='How to obtain a dxdiag log')
    async def dxdiag(self, ctx):
        embed = discord.Embed(
                title = 'How do I obtain a dxdiag log?',
                description = '1) Press the Windows key + R\n'
                              '2) In the small window that appeared type `dxdiag` and press Enter\n'
                              '3) In the new window that opened press the `Save All Information` button\n'
                              '4) Save the dxdiag.txt file and drag and drop it in this channel',
                colour = discord.Colour.dark_green()
            )
        await ctx.send(embed=embed)

    # savefiles location help command
    @commands.command(description='Where to find save files')
    async def savefiles(self, ctx):
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
        await ctx.send(embed=embed)

    # trade help command
    @commands.command(description='How to trading')
    async def trade(self, ctx):
        embed = discord.Embed(
                title = 'Trade Prerequisites',
                description = '1) Trade route unlocked from the first tab of trade window\n'
                              '2) Trade window second tab set to buy or sell, and an amount entered for the wanted resource\n'
                              '3) Warehouse or Granary with slot assigned for the resource you want to trade\n'
                              '4) Patience for the trader to show up. He will come approximately once per week',
                colour = discord.Colour.dark_green()
            )
        await ctx.send(embed=embed)

    # modding help command
    @commands.guild_only()
    @commands.command(description='How to modding')
    async def modding(self, ctx):
        embed = discord.Embed(
                title = 'Modding! Where to begin?',
                description = 'Foundation API: https://www.polymorph.games/foundation/modding/\n'
                              'For anything further feel free to ask us! ' + discord.utils.get(ctx.guild.channels, id=settings.moddingChannel).mention,
                colour = discord.Colour.dark_green()
            )
        await ctx.send(embed=embed)

    # prospecting help command
    @commands.command(description='How to prospecting')
    async def prospecting(self, ctx):
        embed = discord.Embed(
                title = 'How to Prospecting?',
                description = '1) Big rock node inside your domain\n'
                              '2) Bailiff assigned to the bailiff\'s office\n'
                              '3) Start prospecting mandate\n'
                              '4) Click on discovered mineral node to build mines',
                colour = discord.Colour.dark_green()
            )
        await ctx.send(embed=embed)

    # immigration help command
    @commands.command(description='What affects immigration')
    async def immigration(self, ctx):
        embed = discord.Embed(
                title = 'What affects Immigration?',
                description = '1) Happiness\n'
                              '2) Residential Space, note desirability also matters depending on the villager rank!\n'
                              '3) Employment, note villagers with a job but no workplace still count as unemployed!\n\n'
                              'For more detailed information see this thread: https://steamcommunity.com/app/690830/discussions/0/1742265965886407909/',
                colour = discord.Colour.dark_green()
            )
        await ctx.send(embed=embed)

    # preview build help command
    @commands.command(description='How to activate a preview build')
    async def preview(self, ctx):
        embed = discord.Embed(
                title = 'How do I activate a Preview build?',
                description = '1) Right click on Foundation on Steam\n'
                              '2) Select Properties\n'
                              '3) Navigate to the BETAS tab\n'
                              '4) Select the preview build from the drop down and press close\n'
                              '5) The preview build should start downloading automatically',
                colour = discord.Colour.dark_green()
            )
        await ctx.send(embed=embed)

    # villager needs help command
    @commands.command(description='What needs do villagers have')
    async def needs(self, ctx):
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
        '+-------+-------+--------------+-------+---------+--------+--------+\n'
        '|  Rank | Water | Food Sources | House | Clothes | Church | Luxury |\n'
        '+-------+-------+--------------+-------+---------+--------+--------+\n'
        '|  Monk |   x   |       1      | Dorms |         |    x   |        |\n'
        '+-------+-------+--------------+-------+---------+--------+--------+\n'
        '| Prior |   x   |       1      | Dorms |         |    x   |        |\n'
        '+-------+-------+--------------+-------+---------+--------+--------+```')
        await ctx.send(villagerneeds)
        await ctx.send(armyneeds)
        await ctx.send(clergyneeds)

    # keybindings help command
    @commands.command(description='Displays available keybindings')
    async def keybindings(self, ctx):
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
        await ctx.send(embed=embed)

    # commands help command
    @commands.command(aliases=['commands'], description='Displays this help message')
    async def help(self, ctx):
        helpMessage = '```Available Commands\n\n'
        helpCog = bot.get_cog('HelpCommands')
        helpCommands = helpCog.get_commands()
        generalCog = bot.get_cog('GeneralCommands')
        generalCommands = generalCog.get_commands()
        maxLength = 0
        for command in helpCommands:
            length = 0
            if len(command.aliases) > 0:
                for alias in command.aliases:
                    length += len(alias) + 3
                length += len(command.name)
            else:
                length = len(command.name)
            if length > maxLength:
                maxLength = length
        for command in generalCommands:
            length = 0
            if len(command.aliases) > 0:
                for alias in command.aliases:
                    length += len(alias) + 3
                length += len(command.name)
            else:
                length = len(command.name)
            if length > maxLength:
                maxLength = length
        
        helpMessage += 'Help Commands\n'
        for command in helpCommands:
            spaces = ''
            length = 0
            if len(command.aliases) > 0:
                aliasStr = ''
                for alias in command.aliases:
                    length += len(alias) + 3
                    aliasStr += ', /' + alias
                length += len(command.name)
                for _ in range(length,maxLength + 4):
                    spaces += ' '
                helpMessage += '/' + command.name + aliasStr + spaces + command.description + '\n'
            else:
                length = len(command.name)
                for _ in range(length,maxLength + 4):
                    spaces += ' '
                helpMessage += '/' + command.name + spaces + command.description + '\n'
        
        helpMessage += '\nGeneral Commands\n'
        for command in generalCommands:
            spaces = ''
            length = 0
            if len(command.aliases) > 0:
                aliasStr = ''
                for alias in command.aliases:
                    length += len(alias) + 3
                    aliasStr += ', /' + alias
                length += len(command.name)
                for _ in range(length,maxLength + 4):
                    spaces += ' '
                helpMessage += '/' + command.name + aliasStr + spaces + command.description + '\n'
            else:
                length = len(command.name)
                for _ in range(length,maxLength + 4):
                    spaces += ' '
                helpMessage += '/' + command.name + spaces + command.description + '\n'
        
        helpMessage += '```'
        await ctx.send(helpMessage)

class GeneralCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # leaderboard display command
    @commands.guild_only()
    @commands.command(description='Displays screenshot leaderboard')
    async def leaderboard(self, ctx):
        currentLeaderboard = leaderboardSystem.getLeaderboard()
        formattedleaderboard = [[0]*4 for i in range(len(currentLeaderboard))]
        for i,entry in enumerate(currentLeaderboard):
            if ctx.message.guild.get_member(entry.userID) != None: # check if user is still in the server
                formattedleaderboard[i][0] = ctx.message.guild.get_member(entry.userID).display_name # userid converted to display name
                formattedleaderboard[i][1] = entry.postCount
                formattedleaderboard[i][2] = entry.score
                formattedleaderboard[i][3] = entry.score / entry.postCount # ratio
            else:
                continue
        formattedleaderboard.sort(key=sortKey, reverse = True)
        users = ''
        scores = ''
        ratios = ''
        for entry in formattedleaderboard: # might need to limit number of entries to display here
            # check if the user has a non-zero score and at least five posts
            if entry[2] > 0 and entry[1] >= 5:
                users += entry[0] + '\n'
                scores += str(entry[2]) + '\n'
                ratios += str(entry[3]) + '\n'
        
        # check if leaderboard has entries
        if len(users) == 0:
            await ctx.send('The Leaderboard has no Entries! Either no user has a non-Zero score, or no user has reached the minimum post count!')
        else:
            embed = discord.Embed(
                    title = 'Screenshot Leaderboard',
                    #description = '',
                    colour = discord.Colour.dark_green()
                )
            embed.add_field(name='Username' , value=users, inline=True)
            embed.add_field(name='Score', value=scores, inline=True)
            embed.add_field(name='Ratio', value=ratios, inline=True)
            embed.set_footer(text='Leaderboard as of ' + ctx.message.created_at.strftime('%d/%m/%Y, %H:%M') +  ' UTC')
            await ctx.send(embed=embed)

class SettingsCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.group()
    @commands.has_guild_permissions(administrator=True)
    async def set(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('You need to provide a setting to set!')
    
    @set.command(description='Displays the Current Settings')
    async def check(self, ctx):
        embed = discord.Embed(
                title = 'Current Settings',
                #description = '',
                colour = discord.Colour.dark_green()
                )
        settingsList = ('botActive\n'
                        'pinsChannel\n'
                        'pinsRoles\n'
                        'leaderboardEmoji\n'
                        'leaderboardChannel\n'
                        'moddingChannel\n'
                        'rankingChannel\n'
                        'rankingMessage\n\n'
                        'labourEmoji\n'
                        'clergyEmoji\n'
                        'kingdomEmoji\n'
                        'defaultRole\n'
                        'labourRole1\n'
                        'labourRole2\n'
                        'labourRole3\n'
                        'labourRole4\n'
                        'clergyRole1\n'
                        'clergyRole2\n'
                        'clergyRole3\n'
                        'clergyRole4\n'
                        'kingdomRole1\n'
                        'kingdomRole2\n'
                        'kingdomRole3\n'
                        'kingdomRole4\n'
                        'highestRole\n'
                        'expLevel1\n'
                        'expLevel2\n'
                        'expLevel3\n'
                        'expLevel4\n'
                        'expLevelH\n'
                        )

        if settings.pinsChannel != None:
            pinsChannelstr = bot.get_channel(settings.pinsChannel).mention
        else:
            pinsChannelstr = 'Not Set'
        if settings.pinsRoles:
            pinsRolesstr = ''
            for i,role in enumerate(settings.pinsRoles):
                if i == 0:
                    pinsRolesstr += ctx.guild.get_role(role).mention
                else:
                    pinsRolesstr += ', ' + ctx.guild.get_role(role).mention
        else:
            pinsRolesstr = 'Not Set'
        if settings.leaderboardEmoji != None:
            leaderboardEmojistr = str(bot.get_emoji(settings.leaderboardEmoji))
        else:
            leaderboardEmojistr = 'Not Set'
        if settings.leaderboardChannel != None:
            leaderboardChannelstr = bot.get_channel(settings.leaderboardChannel).mention
        else:
            leaderboardChannelstr = 'Not Set'
        if settings.moddingChannel != None:
            moddingChannelstr = bot.get_channel(settings.moddingChannel).mention
        else:
            moddingChannelstr = 'Not Set'
        if settings.rankingChannel != None:
            rankingChannelstr = bot.get_channel(settings.rankingChannel).mention
        else:
            rankingChannelstr = 'Not Set'
        if settings.rankingMessage != None:
            rankingMessage = await bot.get_channel(settings.rankingChannel).fetch_message(settings.rankingMessage)
            rankingMessagestr = rankingMessage.jump_url
        else:
            rankingMessagestr = 'Not Set\n'
        if settings.labourEmoji != None:
            labourEmojistr = str(bot.get_emoji(settings.labourEmoji))
        else:
            labourEmojistr = 'Not Set'
        if settings.clergyEmoji != None:
            clergyEmojistr = str(bot.get_emoji(settings.clergyEmoji))
        else:
            clergyEmojistr = 'Not Set'
        if settings.kingdomEmoji != None:
            kingdomEmojistr = str(bot.get_emoji(settings.kingdomEmoji))
        else:
            kingdomEmojistr = 'Not Set'
        if settings.defaultRole != None:
            defaultRolestr = ctx.guild.get_role(settings.defaultRole).mention
        else:
            defaultRolestr = 'Not Set'
        if settings.labourRole1 != None:
            labourRole1str = ctx.guild.get_role(settings.labourRole1).mention
        else:
            labourRole1str = 'Not Set'
        if settings.labourRole2 != None:
            labourRole2str = ctx.guild.get_role(settings.labourRole2).mention
        else:
            labourRole2str = 'Not Set'
        if settings.labourRole3 != None:
            labourRole3str = ctx.guild.get_role(settings.labourRole3).mention
        else:
            labourRole3str = 'Not Set'
        if settings.labourRole4 != None:
            labourRole4str = ctx.guild.get_role(settings.labourRole4).mention
        else:
            labourRole4str = 'Not Set'
        if settings.clergyRole1 != None:
            clergyRole1str = ctx.guild.get_role(settings.clergyRole1).mention
        else:
            clergyRole1str = 'Not Set'
        if settings.clergyRole2 != None:
            clergyRole2str = ctx.guild.get_role(settings.clergyRole2).mention
        else:
            clergyRole2str = 'Not Set'
        if settings.clergyRole3 != None:
            clergyRole3str = ctx.guild.get_role(settings.clergyRole3).mention
        else:
            clergyRole3str = 'Not Set'
        if settings.clergyRole4 != None:
            clergyRole4str = ctx.guild.get_role(settings.clergyRole4).mention
        else:
            clergyRole4str = 'Not Set'
        if settings.kingdomRole1 != None:
            kingdomRole1str = ctx.guild.get_role(settings.kingdomRole1).mention
        else:
            kingdomRole1str = 'Not Set'
        if settings.kingdomRole2 != None:
            kingdomRole2str = ctx.guild.get_role(settings.kingdomRole2).mention
        else:
            kingdomRole2str = 'Not Set'
        if settings.kingdomRole3 != None:
            kingdomRole3str = ctx.guild.get_role(settings.kingdomRole3).mention
        else:
            kingdomRole3str = 'Not Set'
        if settings.kingdomRole4 != None:
            kingdomRole4str = ctx.guild.get_role(settings.kingdomRole4).mention
        else:
            kingdomRole4str = 'Not Set'
        if settings.highestRole != None:
            highestRolestr = ctx.guild.get_role(settings.highestRole).mention
        else:
            highestRolestr = 'Not Set'
        if settings.expLevel1 != None:
            expLevel1str = str(settings.expLevel1)
        else:
            expLevel1str = 'Not Set'
        if settings.expLevel2 != None:
            expLevel2str = str(settings.expLevel2)
        else:
            expLevel2str = 'Not Set'
        if settings.expLevel3 != None:
            expLevel3str = str(settings.expLevel3)
        else:
            expLevel3str = 'Not Set'
        if settings.expLevel4 != None:
            expLevel4str = str(settings.expLevel4)
        else:
            expLevel4str = 'Not Set'
        if settings.expLevelH != None:
            expLevelHstr = str(settings.expLevelH)
        else:
            expLevelHstr = 'Not Set'
        
        values = (str(settings.botActive) + '\n' +
                  pinsChannelstr + '\n' +
                  pinsRolesstr + '\n' +
                  leaderboardEmojistr + '\n' +
                  leaderboardChannelstr + '\n' +
                  moddingChannelstr + '\n' +
                  rankingChannelstr + '\n' +
                  rankingMessagestr + '\n' +
                  labourEmojistr + '\n' +
                  clergyEmojistr + '\n' +
                  kingdomEmojistr + '\n' +
                  defaultRolestr + '\n' +
                  labourRole1str + '\n' +
                  labourRole2str + '\n' +
                  labourRole3str + '\n' +
                  labourRole4str + '\n' +
                  clergyRole1str + '\n' +
                  clergyRole2str + '\n' +
                  clergyRole3str + '\n' +
                  clergyRole4str + '\n' +
                  kingdomRole1str + '\n' +
                  kingdomRole2str + '\n' +
                  kingdomRole3str + '\n' +
                  kingdomRole4str + '\n' +
                  highestRolestr + '\n' +
                  expLevel1str + '\n' +
                  expLevel2str + '\n' +
                  expLevel3str + '\n' +
                  expLevel4str + '\n' +
                  expLevelHstr + '\n'
                  )
        embed.add_field(name='Setting' , value=settingsList, inline=True)
        embed.add_field(name='Value', value=values, inline=True)
        await ctx.send(embed=embed)
    
    @set.command(description='Sets the Bot Status')
    async def botActive(self, ctx, status: str):
        status = status.lower()
        if status == 'on' or status == 'true'  or status == 'yes':
            update_setting(conn, ('True','botActive'))
            settings.botActive = True
            await ctx.send('botActive set to: `True`')
        elif status == 'off' or status == 'false' or status == 'no':
            update_setting(conn, ('False','botActive'))
            settings.botActive = False
            await ctx.send('botActive set to: `False`')
    
    @set.command(description='Sets the Channel for the Pinning System')
    async def pinsChannel(self, ctx, channel: str):
        try:
            if bot.get_channel(int(channel)) != None:
                update_setting(conn, (channel,'pinsChannel'))
                settings.pinsChannel = int(channel)
                await ctx.send('pinsChannel set to: ' + bot.get_channel(int(channel)).mention)
            else:
                await ctx.send('No channel with the provided ID was found!')
        except ValueError as e:
            await ctx.send('Invalid ID! The channel ID should only consist of an integer number!')
    
    @set.command(description='Sets the Roles to activate the Pinning System')
    async def pinsRoles(self, ctx, *, roles: str):
        roles = roles.split(',')
        rolesList = [0]*len(roles)
        rolesmsg = ''
        savestring = ''
        for i,role in enumerate(roles):
            try:
                role = int(role)
                if ctx.guild.get_role(role) != None:
                    rolesList[i] = role
                    if i == 0:
                        rolesmsg += ctx.guild.get_role(role).mention
                        savestring += str(role)
                    else:
                        rolesmsg += ', ' + ctx.guild.get_role(role).mention
                        savestring += ',' + str(role)
                else:
                    await ctx.send('At least one of the provided role IDs is invalid!')
                    return
            except ValueError as e:
                await ctx.send('At least one of the provided role IDs is invalid!')
                return
        update_setting(conn, (savestring,'pinsRoles'))
        settings.pinsRoles = rolesList
        await ctx.send('pinsRoles set to: ' + rolesmsg)
    
    @set.command(description='Sets the Channel for the Screenshot Leaderboard')
    async def leaderboardChannel(self, ctx, channel: str):
        try:
            if bot.get_channel(int(channel)) != None:
                update_setting(conn, (channel,'leaderboardChannel'))
                settings.leaderboardChannel = int(channel)
                await ctx.send('leaderboardChannel set to: ' + bot.get_channel(int(channel)).mention)
            else:
                await ctx.send('No channel with the provided ID was found!')
        except ValueError as e:
            await ctx.send('Invalid ID! The channel ID should only consist of an integer number!')
    
    @set.command(description='Sets the Emoji to activate the Screenshot Leaderboard')
    async def leaderboardEmoji(self, ctx, emoji: str):
        try:
            if bot.get_emoji(int(emoji)) != None:
                update_setting(conn, (emoji,'leaderboardEmoji'))
                settings.leaderboardEmoji = int(emoji)
                await ctx.send('leaderboardEmoji set to: ' + str(bot.get_emoji(int(emoji))))
            else:
                await ctx.send('No emoji with the provided ID was found!')
        except ValueError as e:
            await ctx.send('Invalid ID! The emoji ID should only consist of an integer number!')
    
    @set.command(description='Sets the Channel for the Modding Help Command')
    async def moddingChannel(self, ctx, channel: str):
        try:
            if bot.get_channel(int(channel)) != None:
                update_setting(conn, (channel,'moddingChannel'))
                settings.moddingChannel = int(channel)
                await ctx.send('moddingChannel set to: ' + bot.get_channel(int(channel)).mention)
            else:
                await ctx.send('No channel with the provided ID was found!')
        except ValueError as e:
            await ctx.send('Invalid ID! The channel ID should only consist of an integer number!')
    
    @set.command(description='Initialises Ranking Emojis on the Ranking Message')
    async def ranking(self, ctx):
        if settings.rankingChannel != None \
        and settings.rankingMessage != None \
        and settings.labourEmoji != None \
        and settings.clergyEmoji != None \
        and settings.kingdomEmoji != None:
            channel = bot.get_channel(settings.rankingChannel)
            message = await channel.fetch_message(settings.rankingMessage)
            await message.add_reaction(discord.utils.get(channel.guild.emojis, id=settings.labourEmoji))
            await message.add_reaction(discord.utils.get(channel.guild.emojis, id=settings.clergyEmoji))
            await message.add_reaction(discord.utils.get(channel.guild.emojis, id=settings.kingdomEmoji))
        else:
            await ctx.send('At least one of the Required Parameters for the Ranking System has not been set, consult `/set check`!')
    
    @set.command(description='Sets the Channel for the Ranking Message')
    async def rankingChannel(self, ctx, channel: str):
        try:
            if bot.get_channel(int(channel)) != None:
                update_setting(conn, (channel,'rankingChannel'))
                settings.rankingChannel = int(channel)
                await ctx.send('rankingChannel set to: ' + bot.get_channel(int(channel)).mention)
                if settings.rankingMessage != None:
                    update_setting(conn, (None,'rankingMessage'))
                    settings.rankingMessage = None
                    await ctx.send('The Ranking Channel was changed and thus the Ranking Message has been reset!\nUse `/set rankingMessage MessageID` to set it again!')
            else:
                await ctx.send('No channel with the provided ID was found!')
        except ValueError as e:
            await ctx.send('Invalid ID! The channel ID should only consist of an integer number!')
    
    @set.command(description='Sets the Message for the Ranking Reactions')
    async def rankingMessage(self, ctx, message: str):
        try:
            actualMessage = await bot.get_channel(settings.rankingChannel).fetch_message(int(message))
            settings.rankingMessage = int(message)
            update_setting(conn, (message,'rankingMessage'))
            await ctx.send('rankingMessage set to: ' + actualMessage.jump_url)
        except ValueError as e:
            await ctx.send('Invalid ID! The message ID should only consist of an integer number!')
    
    @rankingMessage.error
    async def rankingMessage_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            if isinstance(error.original, discord.errors.NotFound):
                await ctx.send('No message with the provided ID was found! Make sure you have set the correct Channel with `/set rankingChannel`!')
    
    @set.command(description='Sets the Emoji for the Labour Ranking Tree')
    async def labourEmoji(self, ctx, emoji: str):
        try:
            if bot.get_emoji(int(emoji)) != None:
                update_setting(conn, (emoji,'labourEmoji'))
                settings.labourEmoji = int(emoji)
                await ctx.send('labourEmoji set to: ' + str(bot.get_emoji(int(emoji))))
            else:
                await ctx.send('No emoji with the provided ID was found!')
        except ValueError as e:
            await ctx.send('Invalid ID! The emoji ID should only consist of an integer number!')
    
    @set.command(description='Sets the Emoji for the Clergy Ranking Tree')
    async def clergyEmoji(self, ctx, emoji: str):
        try:
            if bot.get_emoji(int(emoji)) != None:
                update_setting(conn, (emoji,'clergyEmoji'))
                settings.clergyEmoji = int(emoji)
                await ctx.send('clergyEmoji set to: ' + str(bot.get_emoji(int(emoji))))
            else:
                await ctx.send('No emoji with the provided ID was found!')
        except ValueError as e:
            await ctx.send('Invalid ID! The emoji ID should only consist of an integer number!')
    
    @set.command(description='Sets the Emoji for the Kingdom Ranking Tree')
    async def kingdomEmoji(self, ctx, emoji: str):
        try:
            if bot.get_emoji(int(emoji)) != None:
                update_setting(conn, (emoji,'kingdomEmoji'))
                settings.kingdomEmoji = int(emoji)
                await ctx.send('kingdomEmoji set to: ' + str(bot.get_emoji(int(emoji))))
            else:
                await ctx.send('No emoji with the provided ID was found!')
        except ValueError as e:
            await ctx.send('Invalid ID! The emoji ID should only consist of an integer number!')
    
    @set.command(description='Sets the starting Role for the Ranking System')
    async def defaultRole(self, ctx, role: str):
        try:
            if ctx.guild.get_role(int(role)) != None:
                update_setting(conn, (role,'defaultRole'))
                settings.defaultRole = int(role)
                await ctx.send('defaultRole set to: ' + ctx.guild.get_role(int(role)).mention)
            else:
                await ctx.send('No role with the provided ID was found!')
                return
        except ValueError as e:
            await ctx.send('Invalid ID! The role ID should only consist of an integer number!')
            return
    
    @set.command(description='Sets the level 1 Role for the Labour Ranking Tree')
    async def labourRole1(self, ctx, role: str):
        try:
            if ctx.guild.get_role(int(role)) != None:
                update_setting(conn, (role,'labourRole1'))
                settings.labourRole1 = int(role)
                await ctx.send('labourRole1 set to: ' + ctx.guild.get_role(int(role)).mention)
            else:
                await ctx.send('No role with the provided ID was found!')
                return
        except ValueError as e:
            await ctx.send('Invalid ID! The role ID should only consist of an integer number!')
            return
    
    @set.command(description='Sets the level 2 Role for the Labour Ranking Tree')
    async def labourRole2(self, ctx, role: str):
        try:
            if ctx.guild.get_role(int(role)) != None:
                update_setting(conn, (role,'labourRole2'))
                settings.labourRole2 = int(role)
                await ctx.send('labourRole2 set to: ' + ctx.guild.get_role(int(role)).mention)
            else:
                await ctx.send('No role with the provided ID was found!')
                return
        except ValueError as e:
            await ctx.send('Invalid ID! The role ID should only consist of an integer number!')
            return
    
    @set.command(description='Sets the level 3 Role for the Labour Ranking Tree')
    async def labourRole3(self, ctx, role: str):
        try:
            if ctx.guild.get_role(int(role)) != None:
                update_setting(conn, (role,'labourRole3'))
                settings.labourRole3 = int(role)
                await ctx.send('labourRole3 set to: ' + ctx.guild.get_role(int(role)).mention)
            else:
                await ctx.send('No role with the provided ID was found!')
                return
        except ValueError as e:
            await ctx.send('Invalid ID! The role ID should only consist of an integer number!')
            return
    
    @set.command(description='Sets the level 4 Role for the Labour Ranking Tree')
    async def labourRole4(self, ctx, role: str):
        try:
            if ctx.guild.get_role(int(role)) != None:
                update_setting(conn, (role,'labourRole4'))
                settings.labourRole4 = int(role)
                await ctx.send('labourRole4 set to: ' + ctx.guild.get_role(int(role)).mention)
            else:
                await ctx.send('No role with the provided ID was found!')
                return
        except ValueError as e:
            await ctx.send('Invalid ID! The role ID should only consist of an integer number!')
            return
    
    @set.command(description='Sets the level 1 Role for the Clergy Ranking Tree')
    async def clergyRole1(self, ctx, role: str):
        try:
            if ctx.guild.get_role(int(role)) != None:
                update_setting(conn, (role,'clergyRole1'))
                settings.clergyRole1 = int(role)
                await ctx.send('clergyRole1 set to: ' + ctx.guild.get_role(int(role)).mention)
            else:
                await ctx.send('No role with the provided ID was found!')
                return
        except ValueError as e:
            await ctx.send('Invalid ID! The role ID should only consist of an integer number!')
            return
    
    @set.command(description='Sets the level 2 Role for the Clergy Ranking Tree')
    async def clergyRole2(self, ctx, role: str):
        try:
            if ctx.guild.get_role(int(role)) != None:
                update_setting(conn, (role,'clergyRole2'))
                settings.clergyRole2 = int(role)
                await ctx.send('clergyRole2 set to: ' + ctx.guild.get_role(int(role)).mention)
            else:
                await ctx.send('No role with the provided ID was found!')
                return
        except ValueError as e:
            await ctx.send('Invalid ID! The role ID should only consist of an integer number!')
            return
    
    @set.command(description='Sets the level 3 Role for the Clergy Ranking Tree')
    async def clergyRole3(self, ctx, role: str):
        try:
            if ctx.guild.get_role(int(role)) != None:
                update_setting(conn, (role,'clergyRole3'))
                settings.clergyRole3 = int(role)
                await ctx.send('clergyRole3 set to: ' + ctx.guild.get_role(int(role)).mention)
            else:
                await ctx.send('No role with the provided ID was found!')
                return
        except ValueError as e:
            await ctx.send('Invalid ID! The role ID should only consist of an integer number!')
            return
    
    @set.command(description='Sets the level 4 Role for the Clergy Ranking Tree')
    async def clergyRole4(self, ctx, role: str):
        try:
            if ctx.guild.get_role(int(role)) != None:
                update_setting(conn, (role,'clergyRole4'))
                settings.clergyRole4 = int(role)
                await ctx.send('clergyRole4 set to: ' + ctx.guild.get_role(int(role)).mention)
            else:
                await ctx.send('No role with the provided ID was found!')
                return
        except ValueError as e:
            await ctx.send('Invalid ID! The role ID should only consist of an integer number!')
            return
    
    @set.command(description='Sets the level 1 Role for the Kingdom Ranking Tree')
    async def kingdomRole1(self, ctx, role: str):
        try:
            if ctx.guild.get_role(int(role)) != None:
                update_setting(conn, (role,'kingdomRole1'))
                settings.kingdomRole1 = int(role)
                await ctx.send('kingdomRole1 set to: ' + ctx.guild.get_role(int(role)).mention)
            else:
                await ctx.send('No role with the provided ID was found!')
                return
        except ValueError as e:
            await ctx.send('Invalid ID! The role ID should only consist of an integer number!')
            return
    
    @set.command(description='Sets the level 2 Role for the Kingdom Ranking Tree')
    async def kingdomRole2(self, ctx, role: str):
        try:
            if ctx.guild.get_role(int(role)) != None:
                update_setting(conn, (role,'kingdomRole2'))
                settings.kingdomRole2 = int(role)
                await ctx.send('kingdomRole2 set to: ' + ctx.guild.get_role(int(role)).mention)
            else:
                await ctx.send('No role with the provided ID was found!')
                return
        except ValueError as e:
            await ctx.send('Invalid ID! The role ID should only consist of an integer number!')
            return
    
    @set.command(description='Sets the level 3 Role for the Kingdom Ranking Tree')
    async def kingdomRole3(self, ctx, role: str):
        try:
            if ctx.guild.get_role(int(role)) != None:
                update_setting(conn, (role,'kingdomRole3'))
                settings.kingdomRole3 = int(role)
                await ctx.send('kingdomRole3 set to: ' + ctx.guild.get_role(int(role)).mention)
            else:
                await ctx.send('No role with the provided ID was found!')
                return
        except ValueError as e:
            await ctx.send('Invalid ID! The role ID should only consist of an integer number!')
            return
    
    @set.command(description='Sets the level 4 Role for the Kingdom Ranking Tree')
    async def kingdomRole4(self, ctx, role: str):
        try:
            if ctx.guild.get_role(int(role)) != None:
                update_setting(conn, (role,'kingdomRole4'))
                settings.kingdomRole4 = int(role)
                await ctx.send('kingdomRole4 set to: ' + ctx.guild.get_role(int(role)).mention)
            else:
                await ctx.send('No role with the provided ID was found!')
                return
        except ValueError as e:
            await ctx.send('Invalid ID! The role ID should only consist of an integer number!')
            return
    
    @set.command(description='Sets the Highest Role all Ranking Trees lead to')
    async def highestRole(self, ctx, role: str):
        try:
            if ctx.guild.get_role(int(role)) != None:
                update_setting(conn, (role,'highestRole'))
                settings.highestRole = int(role)
                await ctx.send('highestRole set to: ' + ctx.guild.get_role(int(role)).mention)
            else:
                await ctx.send('No role with the provided ID was found!')
                return
        except ValueError as e:
            await ctx.send('Invalid ID! The role ID should only consist of an integer number!')
            return
    
    @set.command(description='Sets the Experience Required for Level 1')
    async def expLevel1(self, ctx, exp: str):
        try:
            settings.expLevel1 = int(exp)
            update_setting(conn, (exp,'expLevel1'))
            await ctx.send('expLevel1 set to: ' + exp + ' messages')
        except ValueError as e:
            await ctx.send('Invalid Amount of Experience! The experience amount should only consist of an integer number!')
            return
    
    @set.command(description='Sets the Experience Required for Level 2')
    async def expLevel2(self, ctx, exp: str):
        try:
            settings.expLevel2 = int(exp)
            update_setting(conn, (exp,'expLevel2'))
            await ctx.send('expLevel2 set to: ' + exp + ' messages')
        except ValueError as e:
            await ctx.send('Invalid Amount of Experience! The experience amount should only consist of an integer number!')
            return
    
    @set.command(description='Sets the Experience Required for Level 3')
    async def expLevel3(self, ctx, exp: str):
        try:
            settings.expLevel3 = int(exp)
            update_setting(conn, (exp,'expLevel3'))
            await ctx.send('expLevel3 set to: ' + exp + ' messages')
        except ValueError as e:
            await ctx.send('Invalid Amount of Experience! The experience amount should only consist of an integer number!')
            return
    
    @set.command(description='Sets the Experience Required for Level 4')
    async def expLevel4(self, ctx, exp: str):
        try:
            settings.expLevel4 = int(exp)
            update_setting(conn, (exp,'expLevel4'))
            await ctx.send('expLevel4 set to: ' + exp + ' messages')
        except ValueError as e:
            await ctx.send('Invalid Amount of Experience! The experience amount should only consist of an integer number!')
            return
    
    @set.command(description='Sets the Experience Required for the Highest Level')
    async def expLevelH(self, ctx, exp: str):
        try:
            settings.expLevelH = int(exp)
            update_setting(conn, (exp,'expLevelH'))
            await ctx.send('expLevelH set to: ' + exp + ' messages')
        except ValueError as e:
            await ctx.send('Invalid Amount of Experience! The experience amount should only consist of an integer number!')
            return
    
    @set.command(aliases=['commands'], description='Displays this help message')
    async def help(self, ctx):
        helpMessage1 = '```Available Settings Commands\n\n'
        helpMessage2 = '```'
        settingsCog = bot.get_cog('SettingsCommands')
        maxLength = 0
        for command in settingsCog.walk_commands():
            length = 0
            if len(command.aliases) > 0:
                for alias in command.aliases:
                    length += len(alias) + 7
                length += len(command.name)
            else:
                length = len(command.name)
            if length > maxLength:
                maxLength = length
        
        settingsCommands = []
        for command in settingsCog.walk_commands():
            settingsCommands.append(command)
        settingsCommands.pop(0)
        settingsCommands.sort(key=lambda command: command.name)
        
        for i,command in enumerate(settingsCommands):
            if i < floor(len(settingsCommands)/2):
                spaces = ''
                length = 0
                if len(command.aliases) > 0:
                    aliasStr = ''
                    for alias in command.aliases:
                        length += len(alias) + 7
                        aliasStr += ', /set ' + alias
                    length += len(command.name)
                    for _ in range(length,maxLength + 4):
                        spaces += ' '
                    helpMessage1 += '/set ' + command.name + aliasStr + spaces + command.description + '\n'
                else:
                    length = len(command.name)
                    for _ in range(length,maxLength + 4):
                        spaces += ' '
                    helpMessage1 += '/set ' + command.name + spaces + command.description + '\n'
            else:
                spaces = ''
                length = 0
                if len(command.aliases) > 0:
                    aliasStr = ''
                    for alias in command.aliases:
                        length += len(alias) + 7
                        aliasStr += ', /set ' + alias
                    length += len(command.name)
                    for _ in range(length,maxLength + 4):
                        spaces += ' '
                    helpMessage2 += '/set ' + command.name + aliasStr + spaces + command.description + '\n'
                else:
                    length = len(command.name)
                    for _ in range(length,maxLength + 4):
                        spaces += ' '
                    helpMessage2 += '/set ' + command.name + spaces + command.description + '\n'
        
        helpMessage1 += '```'
        helpMessage2 += '```'
        await ctx.send(helpMessage1)
        await ctx.send(helpMessage2)

# ---------------------------------- UTILITIES ---------------------------------- #

class Settings:
    def __init__(self):
        # pinning system parameters
        self.pinsChannel = None
        self.pinsRoles = []
        
        # leaderboard system parameters
        self.leaderboardEmoji = None
        self.leaderboardChannel = None
        
        # ranking system parameters
        self.rankingChannel = None
        self.rankingMessage = None
        self.labourEmoji = None
        self.clergyEmoji = None
        self.kingdomEmoji = None
        self.defaultRole = None
        self.labourRole1 = None
        self.labourRole2 = None
        self.labourRole3 = None
        self.labourRole4 = None
        self.clergyRole1 = None
        self.clergyRole2 = None
        self.clergyRole3 = None
        self.clergyRole4 = None
        self.kingdomRole1 = None
        self.kingdomRole2 = None
        self.kingdomRole3 = None
        self.kingdomRole4 = None
        self.highestRole = None
        self.expLevel1 = None
        self.expLevel2 = None
        self.expLevel3 = None
        self.expLevel4 = None
        self.expLevelH = None
        
        # other parameters
        self.moddingChannel = None
        self.botActive = False

    def setSettings(self, settingsList):
        for setting in settingsList:
            if setting[1] == 'botActive' and setting[2] != None:
                if setting[2] == 'True':
                    self.botActive = True
                else:
                    self.botActive = False
            elif setting[1] == 'pinsChannel' and setting[2] != None:
                self.pinsChannel = int(setting[2])
            elif setting[1] == 'pinsRoles' and setting[2] != None:
                try:
                    roles = setting[2].split(',')
                    for role in roles:
                        self.pinsRoles.append(int(role))
                except AttributeError:
                    self.pinsRoles.append(int(setting[2]))
            elif setting[1] == 'leaderboardChannel' and setting[2] != None:
                self.leaderboardChannel = int(setting[2])
            elif setting[1] == 'leaderboardEmoji' and setting[2] != None:
                self.leaderboardEmoji = int(setting[2])
            elif setting[1] == 'moddingChannel' and setting[2] != None:
                self.moddingChannel = int(setting[2])
            elif setting[1] == 'rankingChannel' and setting[2] != None:
                self.rankingChannel = int(setting[2])
            elif setting[1] == 'rankingMessage' and setting[2] != None:
                self.rankingMessage = int(setting[2])
            elif setting[1] == 'labourEmoji' and setting[2] != None:
                self.labourEmoji = int(setting[2])
            elif setting[1] == 'clergyEmoji' and setting[2] != None:
                self.clergyEmoji = int(setting[2])
            elif setting[1] == 'kingdomEmoji' and setting[2] != None:
                self.kingdomEmoji = int(setting[2])
            elif setting[1] == 'defaultRole' and setting[2] != None:
                self.defaultRole = int(setting[2])
            elif setting[1] == 'labourRole1' and setting[2] != None:
                self.labourRole1 = int(setting[2])
            elif setting[1] == 'labourRole2' and setting[2] != None:
                self.labourRole2 = int(setting[2])
            elif setting[1] == 'labourRole3' and setting[2] != None:
                self.labourRole3 = int(setting[2])
            elif setting[1] == 'labourRole4' and setting[2] != None:
                self.labourRole4 = int(setting[2])
            elif setting[1] == 'clergyRole1' and setting[2] != None:
                self.clergyRole1 = int(setting[2])
            elif setting[1] == 'clergyRole2' and setting[2] != None:
                self.clergyRole2 = int(setting[2])
            elif setting[1] == 'clergyRole3' and setting[2] != None:
                self.clergyRole3 = int(setting[2])
            elif setting[1] == 'clergyRole4' and setting[2] != None:
                self.clergyRole4 = int(setting[2])
            elif setting[1] == 'kingdomRole1' and setting[2] != None:
                self.kingdomRole1 = int(setting[2])
            elif setting[1] == 'kingdomRole2' and setting[2] != None:
                self.kingdomRole2 = int(setting[2])
            elif setting[1] == 'kingdomRole3' and setting[2] != None:
                self.kingdomRole3 = int(setting[2])
            elif setting[1] == 'kingdomRole4' and setting[2] != None:
                self.kingdomRole4 = int(setting[2])
            elif setting[1] == 'highestRole' and setting[2] != None:
                self.highestRole = int(setting[2])
            elif setting[1] == 'expLevel1' and setting[2] != None:
                self.expLevel1 = int(setting[2])
            elif setting[1] == 'expLevel2' and setting[2] != None:
                self.expLevel2 = int(setting[2])
            elif setting[1] == 'expLevel3' and setting[2] != None:
                self.expLevel3 = int(setting[2])
            elif setting[1] == 'expLevel4' and setting[2] != None:
                self.expLevel4 = int(setting[2])
            elif setting[1] == 'expLevelH' and setting[2] != None:
                self.expLevelH = int(setting[2])

# for leaderboard list sorting
def sortKey(element):
    return element[3]

# get the bot's unique token from a file
def getToken():
    with open ('TOKEN', 'r') as t:
        TOKEN = t.read()
    return TOKEN

async def checkRank(member, re):
    if re.experience >= settings.expLevel1 and re.experience < settings.expLevel2:
        if re.estate == 'Labour':
            if not any(role.id == settings.labourRole1 for role in member.roles):
                for role in member.roles:
                    if role.id == settings.defaultRole \
                    or role.id == settings.labourRole2 \
                    or role.id == settings.labourRole3 \
                    or role.id == settings.labourRole4 \
                    or role.id == settings.clergyRole1 \
                    or role.id == settings.clergyRole2 \
                    or role.id == settings.clergyRole3 \
                    or role.id == settings.clergyRole4 \
                    or role.id == settings.kingdomRole1 \
                    or role.id == settings.kingdomRole2 \
                    or role.id == settings.kingdomRole3 \
                    or role.id == settings.kingdomRole4 \
                    or role.id == settings.highestRole:
                        await member.remove_roles(role)
                await member.add_roles(member.guild.get_role(settings.labourRole1))
                re.rank = settings.labourRole1
                rankingSystem.setRankingEntryRank(re)
                if any(entry.userID == member.id for entry in rankingSystem.getSaveList()):
                    rankingSystem.setSaveListEntryRank(re)
                else:
                    rankingSystem.createSaveListEntry(re)
                msg = congratulatoryMessage(member, re)
                return True, msg
            else:
                return False, ''
        if re.estate == 'Clergy':
            if not any(role.id == settings.clergyRole1 for role in member.roles):
                for role in member.roles:
                    if role.id == settings.defaultRole \
                    or role.id == settings.clergyRole2 \
                    or role.id == settings.clergyRole3 \
                    or role.id == settings.clergyRole4 \
                    or role.id == settings.labourRole1 \
                    or role.id == settings.labourRole2 \
                    or role.id == settings.labourRole3 \
                    or role.id == settings.labourRole4 \
                    or role.id == settings.kingdomRole1 \
                    or role.id == settings.kingdomRole2 \
                    or role.id == settings.kingdomRole3 \
                    or role.id == settings.kingdomRole4 \
                    or role.id == settings.highestRole:
                        await member.remove_roles(role)
                await member.add_roles(member.guild.get_role(settings.clergyRole1))
                re.rank = settings.clergyRole1
                rankingSystem.setRankingEntryRank(re)
                if any(entry.userID == member.id for entry in rankingSystem.getSaveList()):
                    rankingSystem.setSaveListEntryRank(re)
                else:
                    rankingSystem.createSaveListEntry(re)
                msg = congratulatoryMessage(member, re)
                return True, msg
            else:
                return False, ''
        if re.estate == 'Kingdom':
            if not any(role.id == settings.kingdomRole1 for role in member.roles):
                for role in member.roles:
                    if role.id == settings.defaultRole \
                    or role.id == settings.kingdomRole2 \
                    or role.id == settings.kingdomRole3 \
                    or role.id == settings.kingdomRole4 \
                    or role.id == settings.labourRole1 \
                    or role.id == settings.labourRole2 \
                    or role.id == settings.labourRole3 \
                    or role.id == settings.labourRole4 \
                    or role.id == settings.clergyRole1 \
                    or role.id == settings.clergyRole2 \
                    or role.id == settings.clergyRole3 \
                    or role.id == settings.clergyRole4 \
                    or role.id == settings.highestRole:
                        await member.remove_roles(role)
                await member.add_roles(member.guild.get_role(settings.kingdomRole1))
                re.rank = settings.kingdomRole1
                rankingSystem.setRankingEntryRank(re)
                if any(entry.userID == member.id for entry in rankingSystem.getSaveList()):
                    rankingSystem.setSaveListEntryRank(re)
                else:
                    rankingSystem.createSaveListEntry(re)
                msg = congratulatoryMessage(member, re)
                return True, msg
            else:
                return False, ''
    elif re.experience >= settings.expLevel2 and re.experience < settings.expLevel3:
        if re.estate == 'Labour':
            if not any(role.id == settings.labourRole2 for role in member.roles):
                for role in member.roles:
                    if role.id == settings.defaultRole \
                    or role.id == settings.labourRole1 \
                    or role.id == settings.labourRole3 \
                    or role.id == settings.labourRole4 \
                    or role.id == settings.clergyRole1 \
                    or role.id == settings.clergyRole2 \
                    or role.id == settings.clergyRole3 \
                    or role.id == settings.clergyRole4 \
                    or role.id == settings.kingdomRole1 \
                    or role.id == settings.kingdomRole2 \
                    or role.id == settings.kingdomRole3 \
                    or role.id == settings.kingdomRole4 \
                    or role.id == settings.highestRole:
                        await member.remove_roles(role)
                await member.add_roles(member.guild.get_role(settings.labourRole2))
                re.rank = settings.labourRole2
                rankingSystem.setRankingEntryRank(re)
                if any(entry.userID == member.id for entry in rankingSystem.getSaveList()):
                    rankingSystem.setSaveListEntryRank(re)
                else:
                    rankingSystem.createSaveListEntry(re)
                msg = congratulatoryMessage(member, re)
                return True, msg
            else:
                return False, ''
        if re.estate == 'Clergy':
            if not any(role.id == settings.clergyRole2 for role in member.roles):
                for role in member.roles:
                    if role.id == settings.defaultRole \
                    or role.id == settings.clergyRole1 \
                    or role.id == settings.clergyRole3 \
                    or role.id == settings.clergyRole4 \
                    or role.id == settings.labourRole1 \
                    or role.id == settings.labourRole2 \
                    or role.id == settings.labourRole3 \
                    or role.id == settings.labourRole4 \
                    or role.id == settings.kingdomRole1 \
                    or role.id == settings.kingdomRole2 \
                    or role.id == settings.kingdomRole3 \
                    or role.id == settings.kingdomRole4 \
                    or role.id == settings.highestRole:
                        await member.remove_roles(role)
                await member.add_roles(member.guild.get_role(settings.clergyRole2))
                re.rank = settings.clergyRole2
                rankingSystem.setRankingEntryRank(re)
                if any(entry.userID == member.id for entry in rankingSystem.getSaveList()):
                    rankingSystem.setSaveListEntryRank(re)
                else:
                    rankingSystem.createSaveListEntry(re)
                msg = congratulatoryMessage(member, re)
                return True, msg
            else:
                return False, ''
        if re.estate == 'Kingdom':
            if not any(role.id == settings.kingdomRole2 for role in member.roles):
                for role in member.roles:
                    if role.id == settings.defaultRole \
                    or role.id == settings.kingdomRole1 \
                    or role.id == settings.kingdomRole3 \
                    or role.id == settings.kingdomRole4 \
                    or role.id == settings.labourRole1 \
                    or role.id == settings.labourRole2 \
                    or role.id == settings.labourRole3 \
                    or role.id == settings.labourRole4 \
                    or role.id == settings.clergyRole1 \
                    or role.id == settings.clergyRole2 \
                    or role.id == settings.clergyRole3 \
                    or role.id == settings.clergyRole4 \
                    or role.id == settings.highestRole:
                        await member.remove_roles(role)
                await member.add_roles(member.guild.get_role(settings.kingdomRole2))
                re.rank = settings.kingdomRole2
                rankingSystem.setRankingEntryRank(re)
                if any(entry.userID == member.id for entry in rankingSystem.getSaveList()):
                    rankingSystem.setSaveListEntryRank(re)
                else:
                    rankingSystem.createSaveListEntry(re)
                msg = congratulatoryMessage(member, re)
                return True, msg
            else:
                return False, ''
    elif re.experience >= settings.expLevel3 and re.experience < settings.expLevel4:
        if re.estate == 'Labour':
            if not any(role.id == settings.labourRole3 for role in member.roles):
                for role in member.roles:
                    if role.id == settings.defaultRole \
                    or role.id == settings.labourRole1 \
                    or role.id == settings.labourRole2 \
                    or role.id == settings.labourRole4 \
                    or role.id == settings.clergyRole1 \
                    or role.id == settings.clergyRole2 \
                    or role.id == settings.clergyRole3 \
                    or role.id == settings.clergyRole4 \
                    or role.id == settings.kingdomRole1 \
                    or role.id == settings.kingdomRole2 \
                    or role.id == settings.kingdomRole3 \
                    or role.id == settings.kingdomRole4 \
                    or role.id == settings.highestRole:
                        await member.remove_roles(role)
                await member.add_roles(member.guild.get_role(settings.labourRole3))
                re.rank = settings.labourRole3
                rankingSystem.setRankingEntryRank(re)
                if any(entry.userID == member.id for entry in rankingSystem.getSaveList()):
                    rankingSystem.setSaveListEntryRank(re)
                else:
                    rankingSystem.createSaveListEntry(re)
                msg = congratulatoryMessage(member, re)
                return True, msg
            else:
                return False, ''
        if re.estate == 'Clergy':
            if not any(role.id == settings.clergyRole3 for role in member.roles):
                for role in member.roles:
                    if role.id == settings.defaultRole \
                    or role.id == settings.clergyRole1 \
                    or role.id == settings.clergyRole2 \
                    or role.id == settings.clergyRole4 \
                    or role.id == settings.labourRole1 \
                    or role.id == settings.labourRole2 \
                    or role.id == settings.labourRole3 \
                    or role.id == settings.labourRole4 \
                    or role.id == settings.kingdomRole1 \
                    or role.id == settings.kingdomRole2 \
                    or role.id == settings.kingdomRole3 \
                    or role.id == settings.kingdomRole4 \
                    or role.id == settings.highestRole:
                        await member.remove_roles(role)
                await member.add_roles(member.guild.get_role(settings.clergyRole3))
                re.rank = settings.clergyRole3
                rankingSystem.setRankingEntryRank(re)
                if any(entry.userID == member.id for entry in rankingSystem.getSaveList()):
                    rankingSystem.setSaveListEntryRank(re)
                else:
                    rankingSystem.createSaveListEntry(re)
                msg = congratulatoryMessage(member, re)
                return True, msg
            else:
                return False, ''
        if re.estate == 'Kingdom':
            if not any(role.id == settings.kingdomRole3 for role in member.roles):
                for role in member.roles:
                    if role.id == settings.defaultRole \
                    or role.id == settings.kingdomRole1 \
                    or role.id == settings.kingdomRole2 \
                    or role.id == settings.kingdomRole4 \
                    or role.id == settings.labourRole1 \
                    or role.id == settings.labourRole2 \
                    or role.id == settings.labourRole3 \
                    or role.id == settings.labourRole4 \
                    or role.id == settings.clergyRole1 \
                    or role.id == settings.clergyRole2 \
                    or role.id == settings.clergyRole3 \
                    or role.id == settings.clergyRole4 \
                    or role.id == settings.highestRole:
                        await member.remove_roles(role)
                await member.add_roles(member.guild.get_role(settings.kingdomRole3))
                re.rank = settings.kingdomRole3
                rankingSystem.setRankingEntryRank(re)
                if any(entry.userID == member.id for entry in rankingSystem.getSaveList()):
                    rankingSystem.setSaveListEntryRank(re)
                else:
                    rankingSystem.createSaveListEntry(re)
                msg = congratulatoryMessage(member, re)
                return True, msg
            else:
                return False, ''
    elif re.experience >= settings.expLevel4 and re.experience < settings.expLevelH:
        if re.estate == 'Labour':
            if not any(role.id == settings.labourRole4 for role in member.roles):
                for role in member.roles:
                    if role.id == settings.defaultRole \
                    or role.id == settings.labourRole1 \
                    or role.id == settings.labourRole2 \
                    or role.id == settings.labourRole3 \
                    or role.id == settings.clergyRole1 \
                    or role.id == settings.clergyRole2 \
                    or role.id == settings.clergyRole3 \
                    or role.id == settings.clergyRole4 \
                    or role.id == settings.kingdomRole1 \
                    or role.id == settings.kingdomRole2 \
                    or role.id == settings.kingdomRole3 \
                    or role.id == settings.kingdomRole4 \
                    or role.id == settings.highestRole:
                        await member.remove_roles(role)
                await member.add_roles(member.guild.get_role(settings.labourRole4))
                re.rank = settings.labourRole4
                rankingSystem.setRankingEntryRank(re)
                if any(entry.userID == member.id for entry in rankingSystem.getSaveList()):
                    rankingSystem.setSaveListEntryRank(re)
                else:
                    rankingSystem.createSaveListEntry(re)
                msg = congratulatoryMessage(member, re)
                return True, msg
            else:
                return False, ''
        if re.estate == 'Clergy':
            if not any(role.id == settings.clergyRole4 for role in member.roles):
                for role in member.roles:
                    if role.id == settings.defaultRole \
                    or role.id == settings.clergyRole1 \
                    or role.id == settings.clergyRole2 \
                    or role.id == settings.clergyRole3 \
                    or role.id == settings.labourRole1 \
                    or role.id == settings.labourRole2 \
                    or role.id == settings.labourRole3 \
                    or role.id == settings.labourRole4 \
                    or role.id == settings.kingdomRole1 \
                    or role.id == settings.kingdomRole2 \
                    or role.id == settings.kingdomRole3 \
                    or role.id == settings.kingdomRole4 \
                    or role.id == settings.highestRole:
                        await member.remove_roles(role)
                await member.add_roles(member.guild.get_role(settings.clergyRole4))
                re.rank = settings.clergyRole4
                rankingSystem.setRankingEntryRank(re)
                if any(entry.userID == member.id for entry in rankingSystem.getSaveList()):
                    rankingSystem.setSaveListEntryRank(re)
                else:
                    rankingSystem.createSaveListEntry(re)
                msg = congratulatoryMessage(member, re)
                return True, msg
            else:
                return False, ''
        if re.estate == 'Kingdom':
            if not any(role.id == settings.kingdomRole4 for role in member.roles):
                for role in member.roles:
                    if role.id == settings.defaultRole \
                    or role.id == settings.kingdomRole1 \
                    or role.id == settings.kingdomRole2 \
                    or role.id == settings.kingdomRole3 \
                    or role.id == settings.labourRole1 \
                    or role.id == settings.labourRole2 \
                    or role.id == settings.labourRole3 \
                    or role.id == settings.labourRole4 \
                    or role.id == settings.clergyRole1 \
                    or role.id == settings.clergyRole2 \
                    or role.id == settings.clergyRole3 \
                    or role.id == settings.clergyRole4 \
                    or role.id == settings.highestRole:
                        await member.remove_roles(role)
                await member.add_roles(member.guild.get_role(settings.kingdomRole4))
                re.rank = settings.kingdomRole4
                rankingSystem.setRankingEntryRank(re)
                if any(entry.userID == member.id for entry in rankingSystem.getSaveList()):
                    rankingSystem.setSaveListEntryRank(re)
                else:
                    rankingSystem.createSaveListEntry(re)
                msg = congratulatoryMessage(member, re)
                return True, msg
            else:
                return False, ''
    elif re.experience >= settings.expLevelH:
        if not any(role.id == settings.highestRole for role in member.roles):
            for role in member.roles:
                if role.id == settings.defaultRole \
                or role.id == settings.labourRole1 \
                or role.id == settings.labourRole2 \
                or role.id == settings.labourRole3 \
                or role.id == settings.labourRole4 \
                or role.id == settings.clergyRole1 \
                or role.id == settings.clergyRole2 \
                or role.id == settings.clergyRole3 \
                or role.id == settings.clergyRole4 \
                or role.id == settings.kingdomRole1 \
                or role.id == settings.kingdomRole2 \
                or role.id == settings.kingdomRole3 \
                or role.id == settings.kingdomRole4:
                    await member.remove_roles(role)
            await member.add_roles(member.guild.get_role(settings.highestRole))
            re.rank = settings.highestRole
            rankingSystem.setRankingEntryRank(re)
            if any(entry.userID == member.id for entry in rankingSystem.getSaveList()):
                rankingSystem.setSaveListEntryRank(re)
            else:
                rankingSystem.createSaveListEntry(re)
            msg = congratulatoryMessage(member, re)
            return True, msg
        else:
            return False, ''
    else:
        return False, ''

def congratulatoryMessage(member, re):
    rank = member.guild.get_role(re.rank)
    if (rank != None):
        msg = 'Congratulations ' + member.mention + '! You have reached the rank of **' + rank.name + '**!'
    return msg

class DatabaseWrite(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.autosave.start()
    
    @tasks.loop(minutes=5.0)
    async def autosave(self):
        leaderboardInsertCheck = 0
        for entry in leaderboardSystem.getSaveList():
            leaderboardInsertCheck = create_leaderboard_entry(conn, (entry.userID,entry.postCount,entry.score,entry.userID))
            if leaderboardInsertCheck == 0:
                update_leaderboard_entry(conn, (entry.postCount,entry.score,entry.userID))
        leaderboardSystem.clearSaveList()
        ranksInsertCheck = 0
        for entry in rankingSystem.getSaveList():
            ranksInsertCheck = create_ranking_entry(conn, (entry.userID,entry.experience,entry.estate,entry.rank,entry.userID))
            if ranksInsertCheck == 0:
                update_ranking_entry(conn, (entry.experience,entry.estate,entry.rank,entry.userID))
        rankingSystem.clearSaveList()
        
    @autosave.before_loop
    async def before_autosave(self):
        await self.bot.wait_until_ready()

# ---------------------------------- MAIN CODE ---------------------------------- #

# Instantiate settings object
settings = Settings()

# Instantiate supplementary classes
leaderboardSystem = leaderboardSystem()
rankingSystem = rankingSystem()

def main():
    # create database
    database = os.getcwd() + os.sep + 'foundation.db'
    conn = create_connection(database)
    if conn is not None:
        # create leaderboard table
        create_leaderboard_table(conn)
        # create ranking table
        create_ranking_table(conn)
        # create settings table
        create_settings_table(conn)
        # initialise settings table
        init_settings(conn)
        settingsList = get_settings(conn)
        settings.setSettings(settingsList)
    else:
        print('Error! cannot create the database connection!')
    
    leaderboardraw = get_leaderboard(conn)
    leaderboard = []
    for entry in leaderboardraw:
        le = leaderboardEntry()
        le.userID = entry[1]
        le.postCount = entry[2]
        le.score = entry[3]
        leaderboard.append(le)
    leaderboardSystem.setLeaderboard(leaderboard)
    
    rankingtableraw = get_ranking_table(conn)
    rankingtable = []
    for entry in rankingtableraw:
        re = rankingEntry()
        re.userID = entry[1]
        re.experience = entry[2]
        re.estate = entry[3]
        re.rank = entry[4]
        rankingtable.append(re)
    rankingSystem.setRankingTable(rankingtable)
    
    # get the bot's unique token
    TOKEN = getToken()
    return conn, TOKEN

if __name__ == '__main__':
    conn, TOKEN = main()
    # start bot
    bot.add_cog(HelpCommands(bot))
    bot.add_cog(GeneralCommands(bot))
    bot.add_cog(SettingsCommands(bot))
    bot.add_cog(DatabaseWrite(bot))
    bot.run(TOKEN)
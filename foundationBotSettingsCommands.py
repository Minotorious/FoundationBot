'''----------------------------------------------------------------------------\
| ||\\    //||       /|¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯\ |
| || \\  // ||  (o_ / |                  SUPPLEMENTARY FILE                  | |
| ||  \\//  ||  //\/  |                         ----                         | |
| ||   \/   ||  V_/_  |                  SETTINGS COMMANDS                   | |
| ||        ||        |‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗/ |
\----------------------------------------------------------------------------'''

import discord
from discord.ext import commands
from datetime import datetime

from foundationBotDatabaseStuff import update_setting

# import logger
from foundationBotLogger import *
logger = Logger()

class SettingsCommands(commands.Cog):
    def __init__(self, bot, conn, settings):
        self.bot = bot
        self.conn = conn
        self.settings = settings
    
    @commands.group()
    @commands.has_guild_permissions(administrator=True)
    async def set(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('You need to provide a setting to set!')
    
    @set.command(description='Displays the Current Settings')
    async def check(self, ctx):
        embed = discord.Embed(
                title = 'Current Settings',
                colour = discord.Colour.dark_green()
                )
        settingsList = ('botActive\n'
                        'guildID\n'
                        'excludedRoles\n'
                        'pinsChannel\n'
                        'pinsRoles\n'
                        'leaderboardEmoji\n'
                        'leaderboardInterval\n'
                        'leaderboardChannel\n'
                        'screenshotChannel\n'
                        'screenshotPostTime\n'
                        'messagesPostTime\n'
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
        
        if self.settings.guildID != None:
            guildIDstr = ctx.bot.get_guild(self.settings.guildID).name
        else:
            guildIDstr = 'Not Set'
        if self.settings.excludedRoles:
            excludedRolesstr = ''
            for i,role in enumerate(self.settings.excludedRoles):
                if i == 0:
                    excludedRolesstr += ctx.guild.get_role(role).mention
                else:
                    excludedRolesstr += ', ' + ctx.guild.get_role(role).mention
        else:
            excludedRolesstr = 'Not Set'
        if self.settings.pinsChannel != None:
            pinsChannelstr = self.bot.get_channel(self.settings.pinsChannel).mention
        else:
            pinsChannelstr = 'Not Set'
        if self.settings.pinsRoles:
            pinsRolesstr = ''
            for i,role in enumerate(self.settings.pinsRoles):
                if i == 0:
                    pinsRolesstr += ctx.guild.get_role(role).mention
                else:
                    pinsRolesstr += ', ' + ctx.guild.get_role(role).mention
        else:
            pinsRolesstr = 'Not Set'
        if self.settings.leaderboardEmoji != None:
            leaderboardEmojistr = str(self.bot.get_emoji(self.settings.leaderboardEmoji))
        else:
            leaderboardEmojistr = 'Not Set'
        if self.settings.leaderboardInterval != None:
            leaderboardIntervalstr = str(self.settings.leaderboardInterval)
        else:
            leaderboardIntervalstr = 'Not Set'
        if self.settings.leaderboardChannel != None:
            leaderboardChannelstr = self.bot.get_channel(self.settings.leaderboardChannel).mention
        else:
            leaderboardChannelstr = 'Not Set'
        if self.settings.screenshotChannel != None:
            screenshotChannelstr = self.bot.get_channel(self.settings.screenshotChannel).mention
        else:
            screenshotChannelstr = 'Not Set'
        if self.settings.screenshotPostTime != None:
            date = datetime.fromtimestamp(self.settings.screenshotPostTime)
            screenshotPostTimestr = str(date.strftime('%d/%m/%Y %H:%M'))
        else:
            screenshotPostTimestr = 'Not Set'
        if self.settings.messagesPostTime != None:
            date = datetime.fromtimestamp(self.settings.messagesPostTime)
            messagesPostTimestr = str(date.strftime('%d/%m/%Y %H:%M'))
        else:
            messagesPostTimestr = 'Not Set'
        if self.settings.moddingChannel != None:
            moddingChannelstr = self.bot.get_channel(self.settings.moddingChannel).mention
        else:
            moddingChannelstr = 'Not Set'
        if self.settings.rankingChannel != None:
            rankingChannelstr = self.bot.get_channel(self.settings.rankingChannel).mention
        else:
            rankingChannelstr = 'Not Set'
        if self.settings.rankingMessage != None:
            rankingMessage = await self.bot.get_channel(self.settings.rankingChannel).fetch_message(self.settings.rankingMessage)
            rankingMessagestr = rankingMessage.jump_url
        else:
            rankingMessagestr = 'Not Set\n'
        if self.settings.labourEmoji != None:
            labourEmojistr = str(self.bot.get_emoji(self.settings.labourEmoji))
        else:
            labourEmojistr = 'Not Set'
        if self.settings.clergyEmoji != None:
            clergyEmojistr = str(self.bot.get_emoji(self.settings.clergyEmoji))
        else:
            clergyEmojistr = 'Not Set'
        if self.settings.kingdomEmoji != None:
            kingdomEmojistr = str(self.bot.get_emoji(self.settings.kingdomEmoji))
        else:
            kingdomEmojistr = 'Not Set'
        if self.settings.defaultRole != None:
            defaultRolestr = ctx.guild.get_role(self.settings.defaultRole).mention
        else:
            defaultRolestr = 'Not Set'
        if self.settings.labourRole1 != None:
            labourRole1str = ctx.guild.get_role(self.settings.labourRole1).mention
        else:
            labourRole1str = 'Not Set'
        if self.settings.labourRole2 != None:
            labourRole2str = ctx.guild.get_role(self.settings.labourRole2).mention
        else:
            labourRole2str = 'Not Set'
        if self.settings.labourRole3 != None:
            labourRole3str = ctx.guild.get_role(self.settings.labourRole3).mention
        else:
            labourRole3str = 'Not Set'
        if self.settings.labourRole4 != None:
            labourRole4str = ctx.guild.get_role(self.settings.labourRole4).mention
        else:
            labourRole4str = 'Not Set'
        if self.settings.clergyRole1 != None:
            clergyRole1str = ctx.guild.get_role(self.settings.clergyRole1).mention
        else:
            clergyRole1str = 'Not Set'
        if self.settings.clergyRole2 != None:
            clergyRole2str = ctx.guild.get_role(self.settings.clergyRole2).mention
        else:
            clergyRole2str = 'Not Set'
        if self.settings.clergyRole3 != None:
            clergyRole3str = ctx.guild.get_role(self.settings.clergyRole3).mention
        else:
            clergyRole3str = 'Not Set'
        if self.settings.clergyRole4 != None:
            clergyRole4str = ctx.guild.get_role(self.settings.clergyRole4).mention
        else:
            clergyRole4str = 'Not Set'
        if self.settings.kingdomRole1 != None:
            kingdomRole1str = ctx.guild.get_role(self.settings.kingdomRole1).mention
        else:
            kingdomRole1str = 'Not Set'
        if self.settings.kingdomRole2 != None:
            kingdomRole2str = ctx.guild.get_role(self.settings.kingdomRole2).mention
        else:
            kingdomRole2str = 'Not Set'
        if self.settings.kingdomRole3 != None:
            kingdomRole3str = ctx.guild.get_role(self.settings.kingdomRole3).mention
        else:
            kingdomRole3str = 'Not Set'
        if self.settings.kingdomRole4 != None:
            kingdomRole4str = ctx.guild.get_role(self.settings.kingdomRole4).mention
        else:
            kingdomRole4str = 'Not Set'
        if self.settings.highestRole != None:
            highestRolestr = ctx.guild.get_role(self.settings.highestRole).mention
        else:
            highestRolestr = 'Not Set'
        if self.settings.expLevel1 != None:
            expLevel1str = str(self.settings.expLevel1)
        else:
            expLevel1str = 'Not Set'
        if self.settings.expLevel2 != None:
            expLevel2str = str(self.settings.expLevel2)
        else:
            expLevel2str = 'Not Set'
        if self.settings.expLevel3 != None:
            expLevel3str = str(self.settings.expLevel3)
        else:
            expLevel3str = 'Not Set'
        if self.settings.expLevel4 != None:
            expLevel4str = str(self.settings.expLevel4)
        else:
            expLevel4str = 'Not Set'
        if self.settings.expLevelH != None:
            expLevelHstr = str(self.settings.expLevelH)
        else:
            expLevelHstr = 'Not Set'
        
        values = (str(self.settings.botActive) + '\n' +
                  guildIDstr + '\n' +
                  excludedRolesstr + '\n' +
                  pinsChannelstr + '\n' +
                  pinsRolesstr + '\n' +
                  leaderboardEmojistr + '\n' +
                  leaderboardIntervalstr + '\n' +
                  leaderboardChannelstr + '\n' +
                  screenshotChannelstr + '\n' +
                  screenshotPostTimestr + '\n' +
                  messagesPostTimestr + '\n' +
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
            update_setting(self.conn, ('True','botActive'))
            self.settings.botActive = True
            await ctx.send('botActive set to: `True`')
        elif status == 'off' or status == 'false' or status == 'no':
            update_setting(self.conn, ('False','botActive'))
            self.settings.botActive = False
            await ctx.send('botActive set to: `False`')
    
    @set.command(description='Sets the Guild ID')
    async def guildID(self, ctx):
        update_setting(self.conn, (str(ctx.guild.id),'guildID'))
        self.settings.guildID = ctx.guild.id
    
    @set.command(description='Sets the Roles to exclude from the Leaderboards')
    async def excludedRoles(self, ctx, *, roles: str):
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
        update_setting(self.conn, (savestring,'excludedRoles'))
        self.settings.excludedRoles = rolesList
        await ctx.send('excludedRoles set to: ' + rolesmsg)
    
    @set.command(description='Sets the Channel for the Pinning System')
    async def pinsChannel(self, ctx, channel: str):
        try:
            if self.bot.get_channel(int(channel)) != None:
                update_setting(self.conn, (channel,'pinsChannel'))
                self.settings.pinsChannel = int(channel)
                await ctx.send('pinsChannel set to: ' + self.bot.get_channel(int(channel)).mention)
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
        update_setting(self.conn, (savestring,'pinsRoles'))
        self.settings.pinsRoles = rolesList
        await ctx.send('pinsRoles set to: ' + rolesmsg)
    
    @set.command(description='Sets the Emoji to activate the Screenshot Leaderboard')
    async def leaderboardEmoji(self, ctx, emoji: str):
        try:
            if self.bot.get_emoji(int(emoji)) != None:
                update_setting(self.conn, (emoji,'leaderboardEmoji'))
                self.settings.leaderboardEmoji = int(emoji)
                await ctx.send('leaderboardEmoji set to: ' + str(self.bot.get_emoji(int(emoji))))
            else:
                await ctx.send('No emoji with the provided ID was found!')
        except ValueError as e:
            await ctx.send('Invalid ID! The emoji ID should only consist of an integer number!')
    
    @set.command(description='Sets the Emoji to activate the Screenshot Leaderboard')
    async def leaderboardInterval(self, ctx, days: str):
        try:
            self.settings.leaderboardInterval = int(days)
            update_setting(self.conn, (days,'leaderboardInterval'))
            await ctx.send('leaderboardInterval set to: ' + days + ' days')
        except ValueError as e:
            await ctx.send('Invalid Number of Days! The number of days should only consist of an integer number!')
    
    @set.command(description='Sets the Channel to post the Leaderboards')
    async def leaderboardChannel(self, ctx, channel: str):
        try:
            if self.bot.get_channel(int(channel)) != None:
                update_setting(self.conn, (channel,'leaderboardChannel'))
                self.settings.leaderboardChannel = int(channel)
                await ctx.send('leaderboardChannel set to: ' + self.bot.get_channel(int(channel)).mention)
            else:
                await ctx.send('No channel with the provided ID was found!')
        except ValueError as e:
            await ctx.send('Invalid ID! The channel ID should only consist of an integer number!')
    
    @set.command(description='Sets the Channel for the Screenshot Leaderboard')
    async def screenshotChannel(self, ctx, channel: str):
        try:
            if self.bot.get_channel(int(channel)) != None:
                update_setting(self.conn, (channel,'screenshotChannel'))
                self.settings.screenshotChannel = int(channel)
                await ctx.send('screenshotChannel set to: ' + self.bot.get_channel(int(channel)).mention)
            else:
                await ctx.send('No channel with the provided ID was found!')
        except ValueError as e:
            await ctx.send('Invalid ID! The channel ID should only consist of an integer number!')
    
    @set.command(description='Sets the Time for the next Screenshot Leaderboard Post')
    async def screenshotPostTime(self, ctx, *, dateTime: str):
        try:
            date = datetime.strptime(dateTime, '%d/%m/%Y %H:%M')
            timeStamp = date.timestamp()
            update_setting(self.conn, (timeStamp,'screenshotPostTime'))
            self.settings.screenshotPostTime = int(timeStamp)
            await ctx.send('screenshotPostTime set to: ' + dateTime + ' UTC. The screenshot leaderboard will be posted according to the leaderboardInterval starting then.')
        except ValueError as e:
            await ctx.send('Invalid dateTime! The dateTime format should be input as: DD/MM/YYYY HH:mm!')
    
    @set.command(description='Sets the Time for the next Messages Leaderboard Post')
    async def messagesPostTime(self, ctx, *, dateTime: str):
        try:
            date = datetime.strptime(dateTime, '%d/%m/%Y %H:%M')
            timeStamp = date.timestamp()
            update_setting(self.conn, (timeStamp,'messagesPostTime'))
            self.settings.messagesPostTime = int(timeStamp)
            await ctx.send('messagesPostTime set to: ' + dateTime + ' UTC. The messages leaderboard will be posted according to the leaderboardInterval starting then.')
        except ValueError as e:
            await ctx.send('Invalid dateTime! The dateTime format should be input as: DD/MM/YYYY HH:mm!')
    
    @set.command(description='Sets the Channel for the Modding Help Command')
    async def moddingChannel(self, ctx, channel: str):
        try:
            if self.bot.get_channel(int(channel)) != None:
                update_setting(self.conn, (channel,'moddingChannel'))
                self.settings.moddingChannel = int(channel)
                await ctx.send('moddingChannel set to: ' + self.bot.get_channel(int(channel)).mention)
            else:
                await ctx.send('No channel with the provided ID was found!')
        except ValueError as e:
            await ctx.send('Invalid ID! The channel ID should only consist of an integer number!')
    
    @set.command(description='Initialises Ranking Emojis on the Ranking Message')
    async def ranking(self, ctx):
        if self.settings.rankingChannel != None \
        and self.settings.rankingMessage != None \
        and self.settings.labourEmoji != None \
        and self.settings.clergyEmoji != None \
        and self.settings.kingdomEmoji != None:
            channel = self.bot.get_channel(self.settings.rankingChannel)
            message = await channel.fetch_message(self.settings.rankingMessage)
            await message.add_reaction(discord.utils.get(channel.guild.emojis, id=self.settings.labourEmoji))
            await message.add_reaction(discord.utils.get(channel.guild.emojis, id=self.settings.clergyEmoji))
            await message.add_reaction(discord.utils.get(channel.guild.emojis, id=self.settings.kingdomEmoji))
            await message.add_reaction('♂')
            await message.add_reaction('♀')
        else:
            await ctx.send('At least one of the Required Parameters for the Ranking System has not been set, consult `/set check`!')
    
    @set.command(description='Sets the Channel for the Ranking Message')
    async def rankingChannel(self, ctx, channel: str):
        try:
            if self.bot.get_channel(int(channel)) != None:
                update_setting(self.conn, (channel,'rankingChannel'))
                self.settings.rankingChannel = int(channel)
                await ctx.send('rankingChannel set to: ' + self.bot.get_channel(int(channel)).mention)
                if self.settings.rankingMessage != None:
                    update_setting(self.conn, (None,'rankingMessage'))
                    self.settings.rankingMessage = None
                    await ctx.send('The Ranking Channel was changed and thus the Ranking Message has been reset!\nUse `/set rankingMessage MessageID` to set it again!')
            else:
                await ctx.send('No channel with the provided ID was found!')
        except ValueError as e:
            await ctx.send('Invalid ID! The channel ID should only consist of an integer number!')
    
    @set.command(description='Sets the Message for the Ranking Reactions')
    async def rankingMessage(self, ctx, message: str):
        try:
            actualMessage = await self.bot.get_channel(self.settings.rankingChannel).fetch_message(int(message))
            self.settings.rankingMessage = int(message)
            update_setting(self.conn, (message,'rankingMessage'))
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
            if self.bot.get_emoji(int(emoji)) != None:
                update_setting(self.conn, (emoji,'labourEmoji'))
                self.settings.labourEmoji = int(emoji)
                await ctx.send('labourEmoji set to: ' + str(self.bot.get_emoji(int(emoji))))
            else:
                await ctx.send('No emoji with the provided ID was found!')
        except ValueError as e:
            await ctx.send('Invalid ID! The emoji ID should only consist of an integer number!')
    
    @set.command(description='Sets the Emoji for the Clergy Ranking Tree')
    async def clergyEmoji(self, ctx, emoji: str):
        try:
            if self.bot.get_emoji(int(emoji)) != None:
                update_setting(self.conn, (emoji,'clergyEmoji'))
                self.settings.clergyEmoji = int(emoji)
                await ctx.send('clergyEmoji set to: ' + str(self.bot.get_emoji(int(emoji))))
            else:
                await ctx.send('No emoji with the provided ID was found!')
        except ValueError as e:
            await ctx.send('Invalid ID! The emoji ID should only consist of an integer number!')
    
    @set.command(description='Sets the Emoji for the Kingdom Ranking Tree')
    async def kingdomEmoji(self, ctx, emoji: str):
        try:
            if self.bot.get_emoji(int(emoji)) != None:
                update_setting(self.conn, (emoji,'kingdomEmoji'))
                self.settings.kingdomEmoji = int(emoji)
                await ctx.send('kingdomEmoji set to: ' + str(self.bot.get_emoji(int(emoji))))
            else:
                await ctx.send('No emoji with the provided ID was found!')
        except ValueError as e:
            await ctx.send('Invalid ID! The emoji ID should only consist of an integer number!')
    
    @set.command(description='Sets the starting Role for the Ranking System')
    async def defaultRole(self, ctx, role: str):
        try:
            if ctx.guild.get_role(int(role)) != None:
                update_setting(self.conn, (role,'defaultRole'))
                self.settings.defaultRole = int(role)
                await ctx.send('defaultRole set to: ' + ctx.guild.get_role(int(role)).mention)
            else:
                await ctx.send('No role with the provided ID was found!')
        except ValueError as e:
            await ctx.send('Invalid ID! The role ID should only consist of an integer number!')
    
    @set.command(description='Sets the level 1 Role for the Labour Ranking Tree')
    async def labourRole1(self, ctx, role: str):
        try:
            if ctx.guild.get_role(int(role)) != None:
                update_setting(self.conn, (role,'labourRole1'))
                self.settings.labourRole1 = int(role)
                await ctx.send('labourRole1 set to: ' + ctx.guild.get_role(int(role)).mention)
            else:
                await ctx.send('No role with the provided ID was found!')
        except ValueError as e:
            await ctx.send('Invalid ID! The role ID should only consist of an integer number!')
    
    @set.command(description='Sets the level 2 Role for the Labour Ranking Tree')
    async def labourRole2(self, ctx, role: str):
        try:
            if ctx.guild.get_role(int(role)) != None:
                update_setting(self.conn, (role,'labourRole2'))
                self.settings.labourRole2 = int(role)
                await ctx.send('labourRole2 set to: ' + ctx.guild.get_role(int(role)).mention)
            else:
                await ctx.send('No role with the provided ID was found!')
        except ValueError as e:
            await ctx.send('Invalid ID! The role ID should only consist of an integer number!')
    
    @set.command(description='Sets the level 3 Role for the Labour Ranking Tree')
    async def labourRole3(self, ctx, role: str):
        try:
            if ctx.guild.get_role(int(role)) != None:
                update_setting(self.conn, (role,'labourRole3'))
                self.settings.labourRole3 = int(role)
                await ctx.send('labourRole3 set to: ' + ctx.guild.get_role(int(role)).mention)
            else:
                await ctx.send('No role with the provided ID was found!')
        except ValueError as e:
            await ctx.send('Invalid ID! The role ID should only consist of an integer number!')
    
    @set.command(description='Sets the level 4 Role for the Labour Ranking Tree')
    async def labourRole4(self, ctx, role: str):
        try:
            if ctx.guild.get_role(int(role)) != None:
                update_setting(self.conn, (role,'labourRole4'))
                self.settings.labourRole4 = int(role)
                await ctx.send('labourRole4 set to: ' + ctx.guild.get_role(int(role)).mention)
            else:
                await ctx.send('No role with the provided ID was found!')
        except ValueError as e:
            await ctx.send('Invalid ID! The role ID should only consist of an integer number!')
    
    @set.command(description='Sets the level 1 Role for the Clergy Ranking Tree')
    async def clergyRole1(self, ctx, role: str):
        try:
            if ctx.guild.get_role(int(role)) != None:
                update_setting(self.conn, (role,'clergyRole1'))
                self.settings.clergyRole1 = int(role)
                await ctx.send('clergyRole1 set to: ' + ctx.guild.get_role(int(role)).mention)
            else:
                await ctx.send('No role with the provided ID was found!')
        except ValueError as e:
            await ctx.send('Invalid ID! The role ID should only consist of an integer number!')
    
    @set.command(description='Sets the level 2 Role for the Clergy Ranking Tree')
    async def clergyRole2(self, ctx, role: str):
        try:
            if ctx.guild.get_role(int(role)) != None:
                update_setting(self.conn, (role,'clergyRole2'))
                self.settings.clergyRole2 = int(role)
                await ctx.send('clergyRole2 set to: ' + ctx.guild.get_role(int(role)).mention)
            else:
                await ctx.send('No role with the provided ID was found!')
        except ValueError as e:
            await ctx.send('Invalid ID! The role ID should only consist of an integer number!')
    
    @set.command(description='Sets the level 3 Role for the Clergy Ranking Tree')
    async def clergyRole3(self, ctx, role: str):
        try:
            if ctx.guild.get_role(int(role)) != None:
                update_setting(self.conn, (role,'clergyRole3'))
                self.settings.clergyRole3 = int(role)
                await ctx.send('clergyRole3 set to: ' + ctx.guild.get_role(int(role)).mention)
            else:
                await ctx.send('No role with the provided ID was found!')
        except ValueError as e:
            await ctx.send('Invalid ID! The role ID should only consist of an integer number!')
    
    @set.command(description='Sets the level 4 Role for the Clergy Ranking Tree')
    async def clergyRole4(self, ctx, role: str):
        try:
            if ctx.guild.get_role(int(role)) != None:
                update_setting(self.conn, (role,'clergyRole4'))
                self.settings.clergyRole4 = int(role)
                await ctx.send('clergyRole4 set to: ' + ctx.guild.get_role(int(role)).mention)
            else:
                await ctx.send('No role with the provided ID was found!')
        except ValueError as e:
            await ctx.send('Invalid ID! The role ID should only consist of an integer number!')
    
    @set.command(description='Sets the level 1 Role for the Kingdom Ranking Tree')
    async def kingdomRole1(self, ctx, role: str):
        try:
            if ctx.guild.get_role(int(role)) != None:
                update_setting(self.conn, (role,'kingdomRole1'))
                self.settings.kingdomRole1 = int(role)
                await ctx.send('kingdomRole1 set to: ' + ctx.guild.get_role(int(role)).mention)
            else:
                await ctx.send('No role with the provided ID was found!')
        except ValueError as e:
            await ctx.send('Invalid ID! The role ID should only consist of an integer number!')
    
    @set.command(description='Sets the level 2 Role for the Kingdom Ranking Tree')
    async def kingdomRole2(self, ctx, role: str):
        try:
            if ctx.guild.get_role(int(role)) != None:
                update_setting(self.conn, (role,'kingdomRole2'))
                self.settings.kingdomRole2 = int(role)
                await ctx.send('kingdomRole2 set to: ' + ctx.guild.get_role(int(role)).mention)
            else:
                await ctx.send('No role with the provided ID was found!')
        except ValueError as e:
            await ctx.send('Invalid ID! The role ID should only consist of an integer number!')
    
    @set.command(description='Sets the level 3 Role for the Kingdom Ranking Tree')
    async def kingdomRole3(self, ctx, role: str):
        try:
            if ctx.guild.get_role(int(role)) != None:
                update_setting(self.conn, (role,'kingdomRole3'))
                self.settings.kingdomRole3 = int(role)
                await ctx.send('kingdomRole3 set to: ' + ctx.guild.get_role(int(role)).mention)
            else:
                await ctx.send('No role with the provided ID was found!')
        except ValueError as e:
            await ctx.send('Invalid ID! The role ID should only consist of an integer number!')
    
    @set.command(description='Sets the level 4 Role for the Kingdom Ranking Tree')
    async def kingdomRole4(self, ctx, role: str):
        try:
            if ctx.guild.get_role(int(role)) != None:
                update_setting(self.conn, (role,'kingdomRole4'))
                self.settings.kingdomRole4 = int(role)
                await ctx.send('kingdomRole4 set to: ' + ctx.guild.get_role(int(role)).mention)
            else:
                await ctx.send('No role with the provided ID was found!')
        except ValueError as e:
            await ctx.send('Invalid ID! The role ID should only consist of an integer number!')
    
    @set.command(description='Sets the Highest Role all Ranking Trees lead to')
    async def highestRole(self, ctx, role: str):
        try:
            if ctx.guild.get_role(int(role)) != None:
                update_setting(self.conn, (role,'highestRole'))
                self.settings.highestRole = int(role)
                await ctx.send('highestRole set to: ' + ctx.guild.get_role(int(role)).mention)
            else:
                await ctx.send('No role with the provided ID was found!')
        except ValueError as e:
            await ctx.send('Invalid ID! The role ID should only consist of an integer number!')
    
    @set.command(description='Sets the Experience Required for Level 1')
    async def expLevel1(self, ctx, exp: str):
        try:
            self.settings.expLevel1 = int(exp)
            update_setting(self.conn, (exp,'expLevel1'))
            await ctx.send('expLevel1 set to: ' + exp + ' messages')
        except ValueError as e:
            await ctx.send('Invalid Amount of Experience! The experience amount should only consist of an integer number!')
    
    @set.command(description='Sets the Experience Required for Level 2')
    async def expLevel2(self, ctx, exp: str):
        try:
            self.settings.expLevel2 = int(exp)
            update_setting(self.conn, (exp,'expLevel2'))
            await ctx.send('expLevel2 set to: ' + exp + ' messages')
        except ValueError as e:
            await ctx.send('Invalid Amount of Experience! The experience amount should only consist of an integer number!')
    
    @set.command(description='Sets the Experience Required for Level 3')
    async def expLevel3(self, ctx, exp: str):
        try:
            self.settings.expLevel3 = int(exp)
            update_setting(self.conn, (exp,'expLevel3'))
            await ctx.send('expLevel3 set to: ' + exp + ' messages')
        except ValueError as e:
            await ctx.send('Invalid Amount of Experience! The experience amount should only consist of an integer number!')
    
    @set.command(description='Sets the Experience Required for Level 4')
    async def expLevel4(self, ctx, exp: str):
        try:
            self.settings.expLevel4 = int(exp)
            update_setting(self.conn, (exp,'expLevel4'))
            await ctx.send('expLevel4 set to: ' + exp + ' messages')
        except ValueError as e:
            await ctx.send('Invalid Amount of Experience! The experience amount should only consist of an integer number!')
    
    @set.command(description='Sets the Experience Required for the Highest Level')
    async def expLevelH(self, ctx, exp: str):
        try:
            self.settings.expLevelH = int(exp)
            update_setting(self.conn, (exp,'expLevelH'))
            await ctx.send('expLevelH set to: ' + exp + ' messages')
        except ValueError as e:
            await ctx.send('Invalid Amount of Experience! The experience amount should only consist of an integer number!')
    
    @set.command(aliases=['commands'], description='Displays this help message')
    async def help(self, ctx):
        helpMessage1 = '```Available Settings Commands\n\n'
        helpMessage2 = '```'
        settingsCog = self.bot.get_cog('SettingsCommands')
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
            if i < len(settingsCommands)/2:
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

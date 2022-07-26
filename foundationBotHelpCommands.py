'''----------------------------------------------------------------------------\
| ||\\    //||       /|¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯\ |
| || \\  // ||  (o_ / |                  SUPPLEMENTARY FILE                  | |
| ||  \\//  ||  //\/  |                         ----                         | |
| ||   \/   ||  V_/_  |                     HELP COMMANDS                    | |
| ||        ||        |‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗/ |
\----------------------------------------------------------------------------'''

import discord
from discord.ext import commands
import os

# import logger
from foundationBotLogger import *
logger = Logger()

class HelpCommands(commands.Cog):
    def __init__(self, bot, settings):
        self.bot = bot
        self.settings = settings

    # crowdin link help command
    @commands.command(aliases=['translate'], description='How to translate Foundation')
    async def crowdin(self, ctx):
        embed = discord.Embed(
                title = 'How can I help translate Foundation?',
                description = '1) Visit https://crowdin.com/project/foundation\n'
                              '2) Create a free account\n'
                              '3) Click on your country\'s flag to join the translation team\n'
                              '4) Wait for approval and you can start translating Foundation!\n'
                              '**If your language is not available let us know to add it!**',
                colour = discord.Colour.dark_green()
            )
        await ctx.send(embed=embed)
        await ctx.message.delete()


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
        await ctx.message.delete()

    # savefiles location help command
    @commands.command(aliases=['savegames'], description='Where to find save files')
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
        await ctx.message.delete()

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
        await ctx.message.delete()

    # modding help command
    @commands.guild_only()
    @commands.command(description='How to modding')
    async def modding(self, ctx):
        if discord.utils.get(ctx.guild.channels, id=self.settings.moddingChannel) != None:
            embed = discord.Embed(
                    title = 'Modding! Where to begin?',
                    description = 'Foundation API: https://www.polymorph.games/foundation/modding/\n'
                                  'For anything further feel free to ask us! ' + discord.utils.get(ctx.guild.channels, id=self.settings.moddingChannel).mention,
                    colour = discord.Colour.dark_green()
                )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                    title = 'Modding! Where to begin?',
                    description = 'Foundation API: https://www.polymorph.games/foundation/modding/\n'
                                  'For anything further feel free to ask us!',
                    colour = discord.Colour.dark_green()
                )
            await ctx.send(embed=embed)
        await ctx.message.delete()

    # prospecting help command
    @commands.command(description='How to prospecting')
    async def prospecting(self, ctx):
        embed = discord.Embed(
                title = 'How to Prospecting?',
                description = '1) Big rock node 3 hexes away from your domain\n'
                              '2) Bailiff assigned to the bailiff\'s office\n'
                              '3) Start prospecting mandate\n'
                              '4) Click on discovered mineral node to build mines',
                colour = discord.Colour.dark_green()
            )
        await ctx.send(embed=embed)
        await ctx.message.delete()

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
        await ctx.message.delete()

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
        await ctx.message.delete()

    # villager needs help command
    @commands.command(description='What needs do villagers have')
    async def needs(self, ctx):
        embed = discord.Embed(
                title = 'What needs do villagers have?',
                #description = '',
                colour = discord.Colour.dark_green()
            )
        file = discord.File(os.getcwd() + os.sep + 'images' + os.sep + 'VillagerNeeds.png', filename='image.png')
        embed.set_image(url='attachment://image.png')
        await ctx.send(file=file, embed=embed)
        await ctx.message.delete()

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
        await ctx.message.delete()

    # commands help command
    @commands.command(aliases=['commands'], description='Displays this help message')
    async def help(self, ctx):
        helpMessage = '```Available Commands\n\n'
        helpCog = self.bot.get_cog('HelpCommands')
        helpCommands = helpCog.get_commands()
        generalCog = self.bot.get_cog('GeneralCommands')
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
        
        if ctx.message.author.guild_permissions.administrator:
            helpMessage += '\nAdmin Commands\n'
            adminCog = self.bot.get_cog('AdminCommands')
            adminCommands = adminCog.get_commands()
            for command in adminCommands:
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
        await ctx.message.delete()

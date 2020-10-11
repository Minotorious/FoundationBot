'''----------------------------------------------------------------------------\
| ||\\    //||       /|¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯\ |
| || \\  // ||  (o_ / |                  SUPPLEMENTARY FILE                  | |
| ||  \\//  ||  //\/  |                         ----                         | |
| ||   \/   ||  V_/_  |                         UTILS                        | |
| ||        ||        |‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗/ |
\----------------------------------------------------------------------------'''

import discord
from discord.ext import commands, tasks
from datetime import datetime, timezone
import os

# Import database methods
from foundationBotDatabaseStuff import *

# import logger
from foundationBotLogger import *
logger = Logger()

# bot settings class
class Settings:
    def __init__(self):
        # pinning system parameters
        self.pinsChannel = None
        self.pinsRoles = []
        
        # leaderboard system parameters
        self.leaderboardEmoji = None
        self.leaderboardInterval = None
        self.leaderboardChannel = None
        self.screenshotChannel = None
        self.screenshotPostTime = None
        self.messagesPostTime = None
        
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
        self.guildID = None
        self.excludedRoles = []

    def setSettings(self, settingsList):
        for setting in settingsList:
            if setting[1] == 'botActive' and setting[2] != None:
                if setting[2] == 'True':
                    self.botActive = True
                else:
                    self.botActive = False
            elif setting[1] == 'guildID' and setting[2] != None:
                self.guildID = int(setting[2])
            elif setting[1] == 'excludedRoles' and setting[2] != None:
                try:
                    roles = setting[2].split(',')
                    for role in roles:
                        self.excludedRoles.append(int(role))
                except AttributeError:
                    self.excludedRoles.append(int(setting[2]))
            elif setting[1] == 'pinsChannel' and setting[2] != None:
                self.pinsChannel = int(setting[2])
            elif setting[1] == 'pinsRoles' and setting[2] != None:
                try:
                    roles = setting[2].split(',')
                    for role in roles:
                        self.pinsRoles.append(int(role))
                except AttributeError:
                    self.pinsRoles.append(int(setting[2]))
            elif setting[1] == 'leaderboardEmoji' and setting[2] != None:
                self.leaderboardEmoji = int(setting[2])
            elif setting[1] == 'leaderboardInterval' and setting[2] != None:
                self.leaderboardInterval = int(setting[2])
            elif setting[1] == 'leaderboardChannel' and setting[2] != None:
                self.leaderboardChannel = int(setting[2])
            elif setting[1] == 'screenshotChannel' and setting[2] != None:
                self.screenshotChannel = int(setting[2])
            elif setting[1] == 'screenshotPostTime' and setting[2] != None:
                self.screenshotPostTime = int(setting[2])
            elif setting[1] == 'messagesPostTime' and setting[2] != None:
                self.messagesPostTime = int(setting[2])
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

class Utils:
    def __init__(self, settings, rankingSystem):
        self.settings = settings
        self.rankingSystem = rankingSystem

    # get the bot's unique token from a file
    def getToken(self):
        with open ('TOKEN', 'r') as t:
            TOKEN = t.read()
        return TOKEN

    # rank progress bar for the ranking embed
    def progress(self, count, total):
        bar_len = 10
        filled_len = int(round(bar_len * count / float(total)))
        bar = '■' * filled_len + '□' * (bar_len - filled_len)
        return bar

    # returning the next rank for the ranking embed
    def getNextRank(self, rankingEntry):
        if rankingEntry.estate == 'Labour':
            if rankingEntry.rank == self.settings.defaultRole:
                return self.settings.labourRole1, self.settings.expLevel1
            elif rankingEntry.rank == self.settings.labourRole1:
                return self.settings.labourRole2, self.settings.expLevel2
            elif rankingEntry.rank == self.settings.labourRole2:
                return self.settings.labourRole3, self.settings.expLevel3
            elif rankingEntry.rank == self.settings.labourRole3:
                return self.settings.labourRole4, self.settings.expLevel4
            elif rankingEntry.rank == self.settings.labourRole4:
                return self.settings.highestRole, self.settings.expLevelH
            elif rankingEntry.rank == self.settings.highestRole:
                return self.settings.highestRole, self.settings.expLevelH
        elif rankingEntry.estate == 'Clergy':
            if rankingEntry.rank == self.settings.defaultRole:
                return self.settings.clergyRole1, self.settings.expLevel1
            elif rankingEntry.rank == self.settings.clergyRole1:
                return self.settings.clergyRole2, self.settings.expLevel2
            elif rankingEntry.rank == self.settings.clergyRole2:
                return self.settings.clergyRole3, self.settings.expLevel3
            elif rankingEntry.rank == self.settings.clergyRole3:
                return self.settings.clergyRole4, self.settings.expLevel4
            elif rankingEntry.rank == self.settings.clergyRole4:
                return self.settings.highestRole, self.settings.expLevelH
            elif rankingEntry.rank == self.settings.highestRole:
                return self.settings.highestRole, self.settings.expLevelH
        elif rankingEntry.estate == 'Kingdom':
            if rankingEntry.rank == self.settings.defaultRole:
                return self.settings.kingdomRole1, self.settings.expLevel1
            elif rankingEntry.rank == self.settings.kingdomRole1:
                return self.settings.kingdomRole2, self.settings.expLevel2
            elif rankingEntry.rank == self.settings.kingdomRole2:
                return self.settings.kingdomRole3, self.settings.expLevel3
            elif rankingEntry.rank == self.settings.kingdomRole3:
                return self.settings.kingdomRole4, self.settings.expLevel4
            elif rankingEntry.rank == self.settings.kingdomRole4:
                return self.settings.highestRole, self.settings.expLevelH
            elif rankingEntry.rank == self.settings.highestRole:
                return self.settings.highestRole, self.settings.expLevelH

    # check and assign correct rank after exp gain
    async def checkRank(self, member, re):
        if re.experience >= self.settings.expLevel1 and re.experience < self.settings.expLevel2:
            if re.estate == 'Labour':
                if not any(role.id == self.settings.labourRole1 for role in member.roles):
                    for role in member.roles:
                        if role.id == self.settings.defaultRole \
                        or role.id == self.settings.labourRole2 \
                        or role.id == self.settings.labourRole3 \
                        or role.id == self.settings.labourRole4 \
                        or role.id == self.settings.clergyRole1 \
                        or role.id == self.settings.clergyRole2 \
                        or role.id == self.settings.clergyRole3 \
                        or role.id == self.settings.clergyRole4 \
                        or role.id == self.settings.kingdomRole1 \
                        or role.id == self.settings.kingdomRole2 \
                        or role.id == self.settings.kingdomRole3 \
                        or role.id == self.settings.kingdomRole4 \
                        or role.id == self.settings.highestRole:
                            await member.remove_roles(role)
                    await member.add_roles(member.guild.get_role(self.settings.labourRole1))
                    re.rank = self.settings.labourRole1
                    self.rankingSystem.setRankingEntryRank(re)
                    if any(entry.userID == member.id for entry in self.rankingSystem.getSaveList()):
                        self.rankingSystem.setSaveListEntryRank(re)
                    else:
                        self.rankingSystem.createSaveListEntry(re)
                    msg = self.congratulatoryMessage(member, re)
                    return True, msg
                else:
                    return False, ''
            if re.estate == 'Clergy':
                if not any(role.id == self.settings.clergyRole1 for role in member.roles):
                    for role in member.roles:
                        if role.id == self.settings.defaultRole \
                        or role.id == self.settings.clergyRole2 \
                        or role.id == self.settings.clergyRole3 \
                        or role.id == self.settings.clergyRole4 \
                        or role.id == self.settings.labourRole1 \
                        or role.id == self.settings.labourRole2 \
                        or role.id == self.settings.labourRole3 \
                        or role.id == self.settings.labourRole4 \
                        or role.id == self.settings.kingdomRole1 \
                        or role.id == self.settings.kingdomRole2 \
                        or role.id == self.settings.kingdomRole3 \
                        or role.id == self.settings.kingdomRole4 \
                        or role.id == self.settings.highestRole:
                            await member.remove_roles(role)
                    await member.add_roles(member.guild.get_role(self.settings.clergyRole1))
                    re.rank = self.settings.clergyRole1
                    self.rankingSystem.setRankingEntryRank(re)
                    if any(entry.userID == member.id for entry in self.rankingSystem.getSaveList()):
                        self.rankingSystem.setSaveListEntryRank(re)
                    else:
                        self.rankingSystem.createSaveListEntry(re)
                    msg = self.congratulatoryMessage(member, re)
                    return True, msg
                else:
                    return False, ''
            if re.estate == 'Kingdom':
                if not any(role.id == self.settings.kingdomRole1 for role in member.roles):
                    for role in member.roles:
                        if role.id == self.settings.defaultRole \
                        or role.id == self.settings.kingdomRole2 \
                        or role.id == self.settings.kingdomRole3 \
                        or role.id == self.settings.kingdomRole4 \
                        or role.id == self.settings.labourRole1 \
                        or role.id == self.settings.labourRole2 \
                        or role.id == self.settings.labourRole3 \
                        or role.id == self.settings.labourRole4 \
                        or role.id == self.settings.clergyRole1 \
                        or role.id == self.settings.clergyRole2 \
                        or role.id == self.settings.clergyRole3 \
                        or role.id == self.settings.clergyRole4 \
                        or role.id == self.settings.highestRole:
                            await member.remove_roles(role)
                    await member.add_roles(member.guild.get_role(self.settings.kingdomRole1))
                    re.rank = self.settings.kingdomRole1
                    self.rankingSystem.setRankingEntryRank(re)
                    if any(entry.userID == member.id for entry in self.rankingSystem.getSaveList()):
                        self.rankingSystem.setSaveListEntryRank(re)
                    else:
                        self.rankingSystem.createSaveListEntry(re)
                    msg = self.congratulatoryMessage(member, re)
                    return True, msg
                else:
                    return False, ''
        elif re.experience >= self.settings.expLevel2 and re.experience < self.settings.expLevel3:
            if re.estate == 'Labour':
                if not any(role.id == self.settings.labourRole2 for role in member.roles):
                    for role in member.roles:
                        if role.id == self.settings.defaultRole \
                        or role.id == self.settings.labourRole1 \
                        or role.id == self.settings.labourRole3 \
                        or role.id == self.settings.labourRole4 \
                        or role.id == self.settings.clergyRole1 \
                        or role.id == self.settings.clergyRole2 \
                        or role.id == self.settings.clergyRole3 \
                        or role.id == self.settings.clergyRole4 \
                        or role.id == self.settings.kingdomRole1 \
                        or role.id == self.settings.kingdomRole2 \
                        or role.id == self.settings.kingdomRole3 \
                        or role.id == self.settings.kingdomRole4 \
                        or role.id == self.settings.highestRole:
                            await member.remove_roles(role)
                    await member.add_roles(member.guild.get_role(self.settings.labourRole2))
                    re.rank = self.settings.labourRole2
                    self.rankingSystem.setRankingEntryRank(re)
                    if any(entry.userID == member.id for entry in self.rankingSystem.getSaveList()):
                        self.rankingSystem.setSaveListEntryRank(re)
                    else:
                        self.rankingSystem.createSaveListEntry(re)
                    msg = self.congratulatoryMessage(member, re)
                    return True, msg
                else:
                    return False, ''
            if re.estate == 'Clergy':
                if not any(role.id == self.settings.clergyRole2 for role in member.roles):
                    for role in member.roles:
                        if role.id == self.settings.defaultRole \
                        or role.id == self.settings.clergyRole1 \
                        or role.id == self.settings.clergyRole3 \
                        or role.id == self.settings.clergyRole4 \
                        or role.id == self.settings.labourRole1 \
                        or role.id == self.settings.labourRole2 \
                        or role.id == self.settings.labourRole3 \
                        or role.id == self.settings.labourRole4 \
                        or role.id == self.settings.kingdomRole1 \
                        or role.id == self.settings.kingdomRole2 \
                        or role.id == self.settings.kingdomRole3 \
                        or role.id == self.settings.kingdomRole4 \
                        or role.id == self.settings.highestRole:
                            await member.remove_roles(role)
                    await member.add_roles(member.guild.get_role(self.settings.clergyRole2))
                    re.rank = self.settings.clergyRole2
                    self.rankingSystem.setRankingEntryRank(re)
                    if any(entry.userID == member.id for entry in self.rankingSystem.getSaveList()):
                        self.rankingSystem.setSaveListEntryRank(re)
                    else:
                        self.rankingSystem.createSaveListEntry(re)
                    msg = self.congratulatoryMessage(member, re)
                    return True, msg
                else:
                    return False, ''
            if re.estate == 'Kingdom':
                if not any(role.id == self.settings.kingdomRole2 for role in member.roles):
                    for role in member.roles:
                        if role.id == self.settings.defaultRole \
                        or role.id == self.settings.kingdomRole1 \
                        or role.id == self.settings.kingdomRole3 \
                        or role.id == self.settings.kingdomRole4 \
                        or role.id == self.settings.labourRole1 \
                        or role.id == self.settings.labourRole2 \
                        or role.id == self.settings.labourRole3 \
                        or role.id == self.settings.labourRole4 \
                        or role.id == self.settings.clergyRole1 \
                        or role.id == self.settings.clergyRole2 \
                        or role.id == self.settings.clergyRole3 \
                        or role.id == self.settings.clergyRole4 \
                        or role.id == self.settings.highestRole:
                            await member.remove_roles(role)
                    await member.add_roles(member.guild.get_role(self.settings.kingdomRole2))
                    re.rank = self.settings.kingdomRole2
                    self.rankingSystem.setRankingEntryRank(re)
                    if any(entry.userID == member.id for entry in self.rankingSystem.getSaveList()):
                        self.rankingSystem.setSaveListEntryRank(re)
                    else:
                        self.rankingSystem.createSaveListEntry(re)
                    msg = self.congratulatoryMessage(member, re)
                    return True, msg
                else:
                    return False, ''
        elif re.experience >= self.settings.expLevel3 and re.experience < self.settings.expLevel4:
            if re.estate == 'Labour':
                if not any(role.id == self.settings.labourRole3 for role in member.roles):
                    for role in member.roles:
                        if role.id == self.settings.defaultRole \
                        or role.id == self.settings.labourRole1 \
                        or role.id == self.settings.labourRole2 \
                        or role.id == self.settings.labourRole4 \
                        or role.id == self.settings.clergyRole1 \
                        or role.id == self.settings.clergyRole2 \
                        or role.id == self.settings.clergyRole3 \
                        or role.id == self.settings.clergyRole4 \
                        or role.id == self.settings.kingdomRole1 \
                        or role.id == self.settings.kingdomRole2 \
                        or role.id == self.settings.kingdomRole3 \
                        or role.id == self.settings.kingdomRole4 \
                        or role.id == self.settings.highestRole:
                            await member.remove_roles(role)
                    await member.add_roles(member.guild.get_role(self.settings.labourRole3))
                    re.rank = self.settings.labourRole3
                    self.rankingSystem.setRankingEntryRank(re)
                    if any(entry.userID == member.id for entry in self.rankingSystem.getSaveList()):
                        self.rankingSystem.setSaveListEntryRank(re)
                    else:
                        self.rankingSystem.createSaveListEntry(re)
                    msg = self.congratulatoryMessage(member, re)
                    return True, msg
                else:
                    return False, ''
            if re.estate == 'Clergy':
                if not any(role.id == self.settings.clergyRole3 for role in member.roles):
                    for role in member.roles:
                        if role.id == self.settings.defaultRole \
                        or role.id == self.settings.clergyRole1 \
                        or role.id == self.settings.clergyRole2 \
                        or role.id == self.settings.clergyRole4 \
                        or role.id == self.settings.labourRole1 \
                        or role.id == self.settings.labourRole2 \
                        or role.id == self.settings.labourRole3 \
                        or role.id == self.settings.labourRole4 \
                        or role.id == self.settings.kingdomRole1 \
                        or role.id == self.settings.kingdomRole2 \
                        or role.id == self.settings.kingdomRole3 \
                        or role.id == self.settings.kingdomRole4 \
                        or role.id == self.settings.highestRole:
                            await member.remove_roles(role)
                    await member.add_roles(member.guild.get_role(self.settings.clergyRole3))
                    re.rank = self.settings.clergyRole3
                    self.rankingSystem.setRankingEntryRank(re)
                    if any(entry.userID == member.id for entry in self.rankingSystem.getSaveList()):
                        self.rankingSystem.setSaveListEntryRank(re)
                    else:
                        self.rankingSystem.createSaveListEntry(re)
                    msg = self.congratulatoryMessage(member, re)
                    return True, msg
                else:
                    return False, ''
            if re.estate == 'Kingdom':
                if not any(role.id == self.settings.kingdomRole3 for role in member.roles):
                    for role in member.roles:
                        if role.id == self.settings.defaultRole \
                        or role.id == self.settings.kingdomRole1 \
                        or role.id == self.settings.kingdomRole2 \
                        or role.id == self.settings.kingdomRole4 \
                        or role.id == self.settings.labourRole1 \
                        or role.id == self.settings.labourRole2 \
                        or role.id == self.settings.labourRole3 \
                        or role.id == self.settings.labourRole4 \
                        or role.id == self.settings.clergyRole1 \
                        or role.id == self.settings.clergyRole2 \
                        or role.id == self.settings.clergyRole3 \
                        or role.id == self.settings.clergyRole4 \
                        or role.id == self.settings.highestRole:
                            await member.remove_roles(role)
                    await member.add_roles(member.guild.get_role(self.settings.kingdomRole3))
                    re.rank = self.settings.kingdomRole3
                    self.rankingSystem.setRankingEntryRank(re)
                    if any(entry.userID == member.id for entry in self.rankingSystem.getSaveList()):
                        self.rankingSystem.setSaveListEntryRank(re)
                    else:
                        self.rankingSystem.createSaveListEntry(re)
                    msg = self.congratulatoryMessage(member, re)
                    return True, msg
                else:
                    return False, ''
        elif re.experience >= self.settings.expLevel4 and re.experience < self.settings.expLevelH:
            if re.estate == 'Labour':
                if not any(role.id == self.settings.labourRole4 for role in member.roles):
                    for role in member.roles:
                        if role.id == self.settings.defaultRole \
                        or role.id == self.settings.labourRole1 \
                        or role.id == self.settings.labourRole2 \
                        or role.id == self.settings.labourRole3 \
                        or role.id == self.settings.clergyRole1 \
                        or role.id == self.settings.clergyRole2 \
                        or role.id == self.settings.clergyRole3 \
                        or role.id == self.settings.clergyRole4 \
                        or role.id == self.settings.kingdomRole1 \
                        or role.id == self.settings.kingdomRole2 \
                        or role.id == self.settings.kingdomRole3 \
                        or role.id == self.settings.kingdomRole4 \
                        or role.id == self.settings.highestRole:
                            await member.remove_roles(role)
                    await member.add_roles(member.guild.get_role(self.settings.labourRole4))
                    re.rank = self.settings.labourRole4
                    self.rankingSystem.setRankingEntryRank(re)
                    if any(entry.userID == member.id for entry in self.rankingSystem.getSaveList()):
                        self.rankingSystem.setSaveListEntryRank(re)
                    else:
                        self.rankingSystem.createSaveListEntry(re)
                    msg = self.congratulatoryMessage(member, re)
                    return True, msg
                else:
                    return False, ''
            if re.estate == 'Clergy':
                if not any(role.id == self.settings.clergyRole4 for role in member.roles):
                    for role in member.roles:
                        if role.id == self.settings.defaultRole \
                        or role.id == self.settings.clergyRole1 \
                        or role.id == self.settings.clergyRole2 \
                        or role.id == self.settings.clergyRole3 \
                        or role.id == self.settings.labourRole1 \
                        or role.id == self.settings.labourRole2 \
                        or role.id == self.settings.labourRole3 \
                        or role.id == self.settings.labourRole4 \
                        or role.id == self.settings.kingdomRole1 \
                        or role.id == self.settings.kingdomRole2 \
                        or role.id == self.settings.kingdomRole3 \
                        or role.id == self.settings.kingdomRole4 \
                        or role.id == self.settings.highestRole:
                            await member.remove_roles(role)
                    await member.add_roles(member.guild.get_role(self.settings.clergyRole4))
                    re.rank = self.settings.clergyRole4
                    self.rankingSystem.setRankingEntryRank(re)
                    if any(entry.userID == member.id for entry in self.rankingSystem.getSaveList()):
                        self.rankingSystem.setSaveListEntryRank(re)
                    else:
                        self.rankingSystem.createSaveListEntry(re)
                    msg = self.congratulatoryMessage(member, re)
                    return True, msg
                else:
                    return False, ''
            if re.estate == 'Kingdom':
                if not any(role.id == self.settings.kingdomRole4 for role in member.roles):
                    for role in member.roles:
                        if role.id == self.settings.defaultRole \
                        or role.id == self.settings.kingdomRole1 \
                        or role.id == self.settings.kingdomRole2 \
                        or role.id == self.settings.kingdomRole3 \
                        or role.id == self.settings.labourRole1 \
                        or role.id == self.settings.labourRole2 \
                        or role.id == self.settings.labourRole3 \
                        or role.id == self.settings.labourRole4 \
                        or role.id == self.settings.clergyRole1 \
                        or role.id == self.settings.clergyRole2 \
                        or role.id == self.settings.clergyRole3 \
                        or role.id == self.settings.clergyRole4 \
                        or role.id == self.settings.highestRole:
                            await member.remove_roles(role)
                    await member.add_roles(member.guild.get_role(self.settings.kingdomRole4))
                    re.rank = self.settings.kingdomRole4
                    self.rankingSystem.setRankingEntryRank(re)
                    if any(entry.userID == member.id for entry in self.rankingSystem.getSaveList()):
                        self.rankingSystem.setSaveListEntryRank(re)
                    else:
                        self.rankingSystem.createSaveListEntry(re)
                    msg = self.congratulatoryMessage(member, re)
                    return True, msg
                else:
                    return False, ''
        elif re.experience >= self.settings.expLevelH:
            if not any(role.id == self.settings.highestRole for role in member.roles):
                for role in member.roles:
                    if role.id == self.settings.defaultRole \
                    or role.id == self.settings.labourRole1 \
                    or role.id == self.settings.labourRole2 \
                    or role.id == self.settings.labourRole3 \
                    or role.id == self.settings.labourRole4 \
                    or role.id == self.settings.clergyRole1 \
                    or role.id == self.settings.clergyRole2 \
                    or role.id == self.settings.clergyRole3 \
                    or role.id == self.settings.clergyRole4 \
                    or role.id == self.settings.kingdomRole1 \
                    or role.id == self.settings.kingdomRole2 \
                    or role.id == self.settings.kingdomRole3 \
                    or role.id == self.settings.kingdomRole4:
                        await member.remove_roles(role)
                await member.add_roles(member.guild.get_role(self.settings.highestRole))
                re.rank = self.settings.highestRole
                self.rankingSystem.setRankingEntryRank(re)
                if any(entry.userID == member.id for entry in self.rankingSystem.getSaveList()):
                    self.rankingSystem.setSaveListEntryRank(re)
                else:
                    self.rankingSystem.createSaveListEntry(re)
                msg = self.congratulatoryMessage(member, re)
                return True, msg
            else:
                return False, ''
        else:
            return False, ''

    # create embed with rank image and progress bar
    def createRankEmbed(self, member, re):
        curRankName = discord.utils.get(member.guild.roles, id=re.rank).name
        nextRank, nextExp = self.getNextRank(re)
        nextRankName = discord.utils.get(member.guild.roles, id=nextRank).name
        if re.rank != self.settings.highestRole:
            prog = self.progress(re.experience, nextExp)
            percentage = round(100.0 * re.experience / float(nextExp), 1)
        else:
            prog = self.progress(nextExp, nextExp)
            percentage = 100.0
        embed = discord.Embed(
                title = curRankName + ' ' + member.display_name,
                colour = discord.Colour.dark_green()
            )
        embed.add_field(name='Progress to Next Rank: ' + str(percentage) + '%', value=curRankName + ' ' + prog + ' ' + nextRankName)
        basepath = os.getcwd() + os.sep + 'levels' + os.sep
        if re.estate == 'Labour':
            if re.gender == 'Male':
                genderstr = os.sep + 'male' + os.sep
            else:
                genderstr = os.sep + 'female' + os.sep
            if re.rank == self.settings.defaultRole:
                file = discord.File(basepath + 'other' + genderstr + 'defaultRole.png', filename='image.png')
                embed.set_thumbnail(url='attachment://image.png')
            elif re.rank == self.settings.labourRole1:
                file = discord.File(basepath + 'labour' + genderstr + 'labourRole1.png', filename='image.png')
                embed.set_thumbnail(url='attachment://image.png')
            elif re.rank == self.settings.labourRole2:
                file = discord.File(basepath + 'labour' + genderstr + 'labourRole2.png', filename='image.png')
                embed.set_thumbnail(url='attachment://image.png')
            elif re.rank == self.settings.labourRole3:
                file = discord.File(basepath + 'labour' + genderstr + 'labourRole3.png', filename='image.png')
                embed.set_thumbnail(url='attachment://image.png')
            elif re.rank == self.settings.labourRole4:
                file = discord.File(basepath + 'labour' + genderstr + 'labourRole4.png', filename='image.png')
                embed.set_thumbnail(url='attachment://image.png')
            elif re.rank == self.settings.highestRole:
                file = discord.File(basepath + 'other' + genderstr + 'highestRole.png', filename='image.png')
                embed.set_thumbnail(url='attachment://image.png')
        elif re.estate == 'Clergy':
            genderstr = os.sep + 'male' + os.sep
            if re.rank == self.settings.defaultRole:
                file = discord.File(basepath + 'other' + genderstr + 'defaultRole.png', filename='image.png')
                embed.set_thumbnail(url='attachment://image.png')
            elif re.rank == self.settings.clergyRole1:
                file = discord.File(basepath + 'clergy' + genderstr + 'clergyRole1.png', filename='image.png')
                embed.set_thumbnail(url='attachment://image.png')
            elif re.rank == self.settings.clergyRole2:
                file = discord.File(basepath + 'clergy' + genderstr + 'clergyRole2.png', filename='image.png')
                embed.set_thumbnail(url='attachment://image.png')
            elif re.rank == self.settings.clergyRole3:
                file = discord.File(basepath + 'clergy' + genderstr + 'clergyRole3.png', filename='image.png')
                embed.set_thumbnail(url='attachment://image.png')
            elif re.rank == self.settings.clergyRole4:
                file = discord.File(basepath + 'clergy' + genderstr + 'clergyRole4.png', filename='image.png')
                embed.set_thumbnail(url='attachment://image.png')
            elif re.rank == self.settings.highestRole:
                file = discord.File(basepath + 'other' + genderstr + 'highestRole.png', filename='image.png')
                embed.set_thumbnail(url='attachment://image.png')
        elif re.estate == 'Kingdom':
            if re.gender == 'Male':
                genderstr = os.sep + 'male' + os.sep
            else:
                genderstr = os.sep + 'female' + os.sep
            if re.rank == self.settings.defaultRole:
                file = discord.File(basepath + 'other' + genderstr + 'defaultRole.png', filename='image.png')
                embed.set_thumbnail(url='attachment://image.png')
            elif re.rank == self.settings.kingdomRole1:
                file = discord.File(basepath + 'kingdom' + genderstr + 'kingdomRole1.png', filename='image.png')
                embed.set_thumbnail(url='attachment://image.png')
            elif re.rank == self.settings.kingdomRole2:
                file = discord.File(basepath + 'kingdom' + genderstr + 'kingdomRole2.png', filename='image.png')
                embed.set_thumbnail(url='attachment://image.png')
            elif re.rank == self.settings.kingdomRole3:
                file = discord.File(basepath + 'kingdom' + genderstr + 'kingdomRole3.png', filename='image.png')
                embed.set_thumbnail(url='attachment://image.png')
            elif re.rank == self.settings.kingdomRole4:
                file = discord.File(basepath + 'kingdom' + genderstr + 'kingdomRole4.png', filename='image.png')
                embed.set_thumbnail(url='attachment://image.png')
            elif re.rank == self.settings.highestRole:
                file = discord.File(basepath + 'other' + genderstr + 'highestRole.png', filename='image.png')
                embed.set_thumbnail(url='attachment://image.png')
        
        return file, embed

    # congratulatory message upon rank up
    def congratulatoryMessage(self, member, re):
        rank = member.guild.get_role(re.rank)
        if (rank != None):
            msg = 'Congratulations ' + member.mention + '! You have reached the rank of **' + rank.name + '**!'
        return msg

class DatabaseWrite(commands.Cog):
    def __init__(self, bot, conn, rankingSystem, leaderboardSystem):
        self.bot = bot
        self.conn = conn
        self.rankingSystem = rankingSystem
        self.leaderboardSystem = leaderboardSystem
        self.autosave.start()
    
    @tasks.loop(minutes=5.0)
    async def autosave(self):
        leaderboardInsertCheck = 0
        for entry in self.leaderboardSystem.getScreenshotSaveList():
            leaderboardInsertCheck = create_screenshot_leaderboard_entry(self.conn, (entry.screenshotID,entry.score,entry.screenshotID))
            if leaderboardInsertCheck == 0:
                update_screenshot_leaderboard_entry(self.conn, (entry.score,entry.screenshotID))
        self.leaderboardSystem.clearScreenshotSaveList()
        for entry in self.leaderboardSystem.getMessagesSaveList():
            leaderboardInsertCheck = create_messages_leaderboard_entry(self.conn, (entry.userID,entry.score,entry.userID))
            if leaderboardInsertCheck == 0:
                update_messages_leaderboard_entry(self.conn, (entry.score,entry.userID))
        self.leaderboardSystem.clearMessagesSaveList()
        ranksInsertCheck = 0
        for entry in self.rankingSystem.getSaveList():
            ranksInsertCheck = create_ranking_entry(self.conn, (entry.userID,entry.experience,entry.estate,entry.rank,entry.gender,entry.userID))
            if ranksInsertCheck == 0:
                update_ranking_entry(self.conn, (entry.experience,entry.estate,entry.rank,entry.gender,entry.userID))
        self.rankingSystem.clearSaveList()
        
    @autosave.before_loop
    async def before_autosave(self):
        await self.bot.wait_until_ready()

class LeaderboardPost(commands.Cog):
    def __init__(self, bot, conn, settings, leaderboardSystem):
        self.bot = bot
        self.conn = conn
        self.settings = settings
        self.leaderboardSystem = leaderboardSystem
        self.post.start()
    
    @tasks.loop(hours=1.0)
    async def post(self):
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

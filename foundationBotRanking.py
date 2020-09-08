'''----------------------------------------------------------------------------\
| ||\\    //||       /|¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯\ |
| || \\  // ||  (o_ / |                  SUPPLEMENTARY FILE                  | |
| ||  \\//  ||  //\/  |                         ----                         | |
| ||   \/   ||  V_/_  |                    RANKING SYSTEM                    | |
| ||        ||        |‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗/ |
\----------------------------------------------------------------------------'''

import asyncio
from discord.ext import tasks

# Ranking System Entry
class rankingEntry:
    def __init__(self):
        self.userID = None
        self.experience = None
        self.estate = None
        self.rank = None

# Ranking System Class
class rankingSystem:
    def __init__(self):
        self.rankingTable = []
        self.cooldownList = []
        self.saveList = []
    
    def getRankingTable(self):
        return self.rankingTable
    
    def setRankingTable(self, r):
        self.rankingTable = r
    
    def getRankingEntry(self, userID):
        for entry in self.rankingTable:
            if entry.userID == userID:
                return entry
        return None
    
    def createRankingEntry(self, re):
        self.rankingTable.append(re)
    
    def setRankingEntryExp(self, re):
        for entry in self.rankingTable:
            if entry.userID == re.userID:
                entry.experience = re.experience
    
    def setRankingEntryEstate(self, re):
        for entry in self.rankingTable:
            if entry.userID == re.userID:
                entry.estate = re.estate
    
    def setRankingEntryRank(self, re):
        for entry in self.rankingTable:
            if entry.userID == re.userID:
                entry.rank = re.rank
    
    def getSaveList(self):
        return self.saveList
    
    def clearSaveList(self):
        self.saveList = []
    
    def createSaveListEntry(self, re):
        self.saveList.append(re)
    
    def setSaveListEntryExp(self, re):
        for entry in self.saveList:
            if entry.userID == re.userID:
                entry.experience = re.experience
    
    def setSaveListEntryEstate(self, re):
        for entry in self.saveList:
            if entry.userID == re.userID:
                entry.estate = re.estate
    
    def setSaveListEntryRank(self, re):
        for entry in self.saveList:
            if entry.userID == re.userID:
                entry.rank = re.rank
    
    def getCooldownList(self):
        return self.cooldownList
        
    def createCooldownListEntry(self,userID):
        self.cooldownList.append(userID)
        
    def removeCooldownListEntry(self, userID):
        try:
            self.cooldownList.remove(userID)
        except ValueError:
            pass
    
class RankingSystemCooldown:
    def __init__(self, rs):
        self.rankingSystem = rs
    
    @tasks.loop(count=1)
    async def cooldown(self, userID):
        print('Cooldown Loop Start: ' + str(userID))
        await asyncio.sleep(60)
        self.rankingSystem.removeCooldownListEntry(userID)
        print('Cooldown Loop End: ' + str(userID))
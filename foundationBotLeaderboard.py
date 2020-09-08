'''----------------------------------------------------------------------------\
| ||\\    //||       /|¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯\ |
| || \\  // ||  (o_ / |                  SUPPLEMENTARY FILE                  | |
| ||  \\//  ||  //\/  |                         ----                         | |
| ||   \/   ||  V_/_  |                  LEADERBOARD SYSTEM                  | |
| ||        ||        |‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗/ |
\----------------------------------------------------------------------------'''

# Leaderboard Entry Object
class leaderboardEntry:
    def __init__(self):
        self.userID = None
        self.score = None
        self.postCount = None

# Leaderboard System Class
class leaderboardSystem:
    def __init__(self):
        self.leaderboard = []
        self.saveList = []
        
    def getLeaderboard(self):
        return self.leaderboard
        
    def setLeaderboard(self, l):
        self.leaderboard = l
        
    def getLeaderboardEntry(self, userID):
        for entry in self.leaderboard:
            if entry.userID == userID:
                return entry
        
    def createLeaderboardEntry(self, le):
        self.leaderboard.append(le)
        
    def setLeaderboardEntryScore(self, le):
        for entry in self.leaderboard:
            if entry.userID == le.userID:
                entry.score = le.score
        
    def setLeaderboardEntryPostCount(self, le):
        for entry in self.leaderboard:
            if entry.userID == le.userID:
                entry.postCount = le.postCount
        
    def getSaveList(self):
        return self.saveList
        
    def clearSaveList(self):
        self.saveList = []
        
    def createSaveListEntry(self, le):
        self.saveList.append(le)
        
    def setSaveListEntryScore(self, le):
        for entry in self.saveList:
            if entry.userID == le.userID:
                entry.score = le.score
        
    def setSaveListEntryPostCount(self, le):
        for entry in self.saveList:
            if entry.userID == le.userID:
                entry.postCount = le.postCount
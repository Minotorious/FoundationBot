'''----------------------------------------------------------------------------\
| ||\\    //||       /|¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯\ |
| || \\  // ||  (o_ / |                  SUPPLEMENTARY FILE                  | |
| ||  \\//  ||  //\/  |                         ----                         | |
| ||   \/   ||  V_/_  |                  LEADERBOARD SYSTEM                  | |
| ||        ||        |‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗/ |
\----------------------------------------------------------------------------'''

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
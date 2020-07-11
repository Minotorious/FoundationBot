class botSettings:
    def __init__(self):
        # pinning system parameters
        self.pinsChannel = 513029879080419349 # channel id where the messages should be pinned
        self.pinsRoles = [ 441307762643959819, 421755121555210261 ] # list of role ids to activate the pinning system
        
        # leaderboard system parameters
        self.leaderboardEmoji = 512002627085795328 # id of the emoji to activate the scoring
        self.leaderboardChannel = 438363717995069463 # channel id in which the scoring works
        
        # other parameters
        self.moddingChannel = 589771859793281054 # channel id of modding_general
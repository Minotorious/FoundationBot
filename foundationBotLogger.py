'''----------------------------------------------------------------------------\
| ||\\    //||       /|¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯\ |
| || \\  // ||  (o_ / |                  SUPPLEMENTARY FILE                  | |
| ||  \\//  ||  //\/  |                         ----                         | |
| ||   \/   ||  V_/_  |                        LOGGER                        | |
| ||        ||        |‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗‗/ |
\----------------------------------------------------------------------------'''

import logging

class Logger:
    def __init__(self):
        self.logger = self.setupLogger()
        
    # logger set up
    def setupLogger(self):
        logger = logging.getLogger('discord')
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler(filename='foundationBot.log', encoding='utf-8', mode='w')
        handler.setFormatter(logging.Formatter(fmt='{asctime}\t\t{levelname}\t{name}\t\t\t{message}',datefmt='%d/%m/%Y %H:%M',style='{'))
        logger.addHandler(handler)
        return logger
        
    def getLogger(self):
        return self.logger
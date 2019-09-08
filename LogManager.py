import logging
from datetime import date,datetime
import xml.etree.ElementTree as ET

class Log:
    logFilename = ""
    loggingLevel = -1
    def initialize(moduleName):
        Log.getFilename()
        logger = logging.getLogger(moduleName)
        if Log.loggingLevel == -1:
            logger.setLevel(logging.DEBUG)  # Starting the logging with debug logs by default
        else:
            logger.setLevel(Log.loggingLevel)

        # create console handler and set level to debug
        ch = logging.FileHandler(Log.logFilename,mode="a")
        if Log.loggingLevel == -1:
            ch.setLevel(logging.DEBUG) # Starting the logging with debug logs by default
        else:
            ch.setLevel(Log.loggingLevel)

        # create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # add formatter to ch
        ch.setFormatter(formatter)

        # add ch to logger
        logger.addHandler(ch)

        return logger

    @classmethod
    def getFilename(cls):
        if Log.logFilename == "":
            now = datetime.now()
            Log.logFilename = "logs\\log_"+datetime.strftime(now,"%d-%m-%Y_%I-%M-%S_%p")+".log"

    @classmethod
    def getLogLevel(cls, level):
        level = level.upper()
        if level == "DEBUG":
            return 10
        elif level == "INFO":
            return 20
        elif level == "WARNING":
            return 30
        elif level == "ERROR":
            return 40
        elif level == "CRITICAL":
            return 50
        else:
            return 0

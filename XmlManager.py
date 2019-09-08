import xml.etree.ElementTree as ET
from Crypt import Crypt
from LogManager import Log
#### Initializations ####
# Initializing logging
logger = Log.initialize('XmlManager')

class XmlManager:
    @classmethod
    def MainConfig(cls):
        logger.info("Initializing Xml configuration")
        try:
            configurationDetails = ET.parse('configuration.xml')    #This file may not exist, introduce fatal error
        except Exception as err:
            logger.critical("Cannot parse configuration.xml")
        ConfigDict={}

        if configurationDetails is not None:
            #Checking the log level
            logger.info("configuration.xml parsed successfully")
            ConfigDict["loggingLevel"] = configurationDetails.find('loggingLevel').text
            if ConfigDict["loggingLevel"] != "DEBUG":
                level = Log.getLogLevel(ConfigDict["loggingLevel"])
                Log.loggingLevel = level
                logger.setLevel(level)
                for handler in logger.handlers:
                    handler.setLevel(level)
            # Check if Email notifications are Enabled
            ConfigDict["EmailNotifications"] = configurationDetails.find('EmailNotifications').text
            ConfigDict["JarvisEmail"] = configurationDetails.find('JarvisEmail').text
            encPassword = configurationDetails.find('JarvisPasscode').text
            ConfigDict["JarvisPasscode"] = encPassword
            # Performing the Password decryption only if Email notifications are enabled
            if ConfigDict["EmailNotifications"] == 'Enabled':
                logger.debug("Performing the Password decryption")
                key = Crypt.loadKeyFile()
                if key is not "KO":
                    logger.debug("Password decryption key is found")
                    c = Crypt()
                    decPassword = c.decrypt(encPassword.strip(),key)
                    if decPassword != "":
                        ConfigDict["JarvisPasscode"] = decPassword
                    else:
                        logger.critical("Error decrypting password") # Raise Fatal Error here
                else:
                    logger.critical("Error fetching key") # Raise Fatal Error here

            ConfigDict["PrimaryCustEmail"] = configurationDetails.find('PrimaryCustEmail').text
            ConfigDict["smtpHost"] = configurationDetails.find('smtpHost').text
            ConfigDict["smtpPort"] = configurationDetails.find('smtpPort').text
            ConfigDict["IdentifierFile"] = configurationDetails.find('IdentifierFile').text
            ConfigDict["BackupDirName"] = configurationDetails.find('BackupDirName').text
            ConfigDict["CheckedPathsFileName"] = configurationDetails.find('CheckedPathsFileName').text
            ConfigDict["BackupSummaryFileName"] = configurationDetails.find('BackupSummaryFileName').text
            ConfigDict["NotificationEmailSubject"] = configurationDetails.find('NotificationEmailSubject').text
            logger.info("Finished reading configuration.xml")
        return ConfigDict

    @classmethod
    def PathManager(cls):
        try:
            handle = open("paths","r")
            contents = handle.read().strip()
        except Exception as err:
            logger.critical("Cannot read the file containing the paths to be backed up")
        finally:
            handle.close()

        if contents is not None:
            paths = contents.split(",")
            return paths

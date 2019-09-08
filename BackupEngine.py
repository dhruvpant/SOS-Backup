# Handling imports
import DriveManager as dm       # Takes care of drive in which backup is supposed to written
import BackupDataManager as bdm # Takes care of data which is supposed to be backed up
from XmlManager import XmlManager
import MailManager as mail
from LogManager import Log

#### Initializations ####
# Initializing Xml configuration management
XmlManager.primaryConfig = XmlManager.MainConfig()
XmlManager.paths = XmlManager.PathManager()

# Initializing logging
logger = Log.initialize('BackupEngine')

#### Initializations ####

# Getting Identified filename
logger.debug("Fetching the name of the identifier file name from xml configuration")
identifier_file_name=XmlManager.primaryConfig["IdentifierFile"]
logger.debug("Fetched the name of the identifier file name from xml configuration")
# Checking all drives for identifier file
logger.debug("Checking all drives for identifier file")
drive = dm.get_usb_drive(identifier_file_name)

if drive!="":
    # Backup drive successfully connected / Identifier file found
    logger.info("Backup drive successfully connected")
    logger.debug("Checking free space in backup drive")
    # Checking the free space available on the backup drive in bytes
    free_space_backup_drive = dm.getFreeSpaceOnBackupDrive(drive)
    # Checking the total diskspace required to write the Backup and if backup creation is possible
    if bdm.can_backup_be_created(free_space_backup_drive) is True:
        logger.info("Sufficient space in backup drive")

        paths = bdm.get_all_paths_to_backup()

        logger.debug("Fetched all paths to backup")
        logger.debug("Getting base directory for creating backups")

        base_directory_for_backup = XmlManager.primaryConfig["BackupDirName"]

        logger.info("Found the base directory for creating backups "+base_directory_for_backup)
        logger.debug("Calling drive manager for creating backup")

        result = dm.executeBackup(drive, base_directory_for_backup, paths)
    else:
        # No Space in backup drive to create backup; log and report this diskspace_required
        logger.error("Insufficient space in the backup drive")
        if XmlManager.primaryConfig["EmailNotifications"] == "Enabled":
            # Email sending is enabled, send email
            logger.debug("Sending email for Insufficient space")
            mail.send("Insufficient space in the backup drive","Failure")
else:
    # If backup drive not connected / identifier file not found
    logger.error("Backup drive not found") # Log error and send email
    if XmlManager.primaryConfig["EmailNotifications"] == "Enabled":
        # Email sending is enabled, send email
        logger.debug("Sending email for unavailability of backup drive")
        mail.send("Backup drive not found","Failure")

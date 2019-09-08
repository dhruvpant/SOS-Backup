from string import ascii_uppercase
from XmlManager import XmlManager
from datetime import datetime
import MailManager as mail
import os
import shutil
import sys
from LogManager import Log
#### Initializations ####
# Initializing logging
logger = Log.initialize('DriveManager')

path_seperator="\\"

def get_usb_drive(identifier_file_name):
    platform_name = get_platform()
    if platform_name is not "Windows":
        path_seperator = "/"
    for drive in ascii_uppercase:
        fullpath=drive+":\\"+identifier_file_name
        if os.path.exists(fullpath):
            return drive + ":\\"
    return ""

def getFreeSpaceOnBackupDrive(driveLetter):
    abc = shutil.disk_usage(driveLetter)
    return abc.free


def get_platform():
    platforms = {
        'linux1' : 'Linux',
        'linux2' : 'Linux',
        'darwin' : 'OS X',
        'win32' : 'Windows'
    }
    if sys.platform not in platforms:
        return sys.platform

    return platforms[sys.platform]

def getTimeStamp():
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    return int(timestamp)

def write_backup_msg_file(bkp_path,paths):
    platform_name = get_platform()
    if platform_name is "Windows":
        sos_filename=bkp_path+"\\\\"+XmlManager.primaryConfig["BackupSummaryFileName"]   # Get this name from the configuration
    else:
        sos_filename=bkp_path+"/"+XmlManager.primaryConfig["BackupSummaryFileName"]

    now = datetime.now()
    sos_bkp_msg = "<h1>Created with SOS Backup</h1><br/><h3>Backup created on "+str(now)+" for the following paths:<h3><br/>"
    for p in paths:
        sos_bkp_msg+=p+"<br/>"

    file_write_status = False
    try:
        file_handle=open(sos_filename,"a+")
        file_handle.write(sos_bkp_msg)
        file_write_status = True
    except Exception as err:
        logger.error("Cannot write SOS message file to the folder")
    finally:
        file_handle.close()

    return sos_bkp_msg

def create_base_backup_directory(backup_path,paths):
    folder_name = str(getTimeStamp())
    base_backup_dir_path = backup_path+path_seperator+folder_name
    bkp_folder_prep_done = ""
    if not os.path.exists(base_backup_dir_path):
        try:
            os.makedirs(base_backup_dir_path)
            sos_bkp_msg = write_backup_msg_file(base_backup_dir_path,paths)
            bkp_folder_prep_done = base_backup_dir_path + "#" + sos_bkp_msg
        except:
            logger.error("Error occured while creating the base backup directory")
            if XmlManager.primaryConfig["EmailNotifications"] == "Enabled":
                # Email sending is enabled, send email
                mail.send("Error occured while creating the base backup directory","Failure")
    return bkp_folder_prep_done

def copy_all_folders(final_bkp_path, paths):
    backup_result = True
    for p in paths:
        try:
            f = final_bkp_path+path_seperator+p.split(path_seperator)[-1]
            shutil.copytree(p, f)
        except:
            logger.error("Some Error occured while copying "+p)
            return False

    return backup_result

def perform_cleanup():
    path_data_file = XmlManager.primaryConfig["CheckedPathsFileName"]  #this file holds all the validated paths to backup for this session, fetch the name of this file from configuration file
    try:
        os.remove(path_data_file)
    except:
        logger.error("Error during cleanup - Failed to delete validated paths file: "+path_data_file)
        if XmlManager.primaryConfig["EmailNotifications"] == "Enabled":
            # Email sending is enabled, send email
            mail.send("Error during cleanup - Failed to delete validated paths file: "+path_data_file,"Failure")

def executeBackup(drive, base_directory_for_backup, paths):
    full_backup_path = drive+path_seperator+base_directory_for_backup+path_seperator;
    final_bkp_path = create_base_backup_directory(full_backup_path, paths)
    if final_bkp_path != "":
        finalPathAndMsg = final_bkp_path.split("#")
        backup_result = copy_all_folders(finalPathAndMsg[0], paths)
        if backup_result is True:
            perform_cleanup()
            # send Email if email sending is Enabled
            if XmlManager.primaryConfig["EmailNotifications"] == "Enabled":
                # Email sending is enabled, send email
                mail.send(finalPathAndMsg[1],"Sucess")
        else:
            logger.error("Cannot copy all folders, some error occured")
            if XmlManager.primaryConfig["EmailNotifications"] == "Enabled":
                # Email sending is enabled, send email
                mail.send("Cannot copy all folders, some error occured","Failure")

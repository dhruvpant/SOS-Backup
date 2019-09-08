import os
from XmlManager import XmlManager
import MailManager as mail
from LogManager import Log

#### Initializations ####
# Initializing logging
logger = Log.initialize('BackupDataManager')

# Include a check for timeout and directory tree size depth for huge folders
def get_size(start_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)

    return total_size

def write_to_text_file(filename, data):
    try:
        handle = open(filename, "a+")
        handle.write(data)
    except FileNotFoundError:
        logger.error("File "+filename+" not found")
        if XmlManager.primaryConfig["EmailNotifications"] == "Enabled":
            # Email sending is enabled, send email
            mail.send("File "+filename+" not found","Failure")
    except:
        logger.error("Error while accessing the file "+filename+". Maybe there is file is read only")
        if XmlManager.primaryConfig["EmailNotifications"] == "Enabled":
            # Email sending is enabled, send email
            mail.send("Error while accessing the file "+filename+". Maybe there is file is read only","Failure")
    finally:
        handle.close()

def get_txt_file_data(filename):
    filedata = ""
    try:
        handle = open(filename, "r")
        file_paths = handle.readlines()
        filedata = file_paths[0]
    except FileNotFoundError:
        logger.error("File "+filename+" not found")
        if XmlManager.primaryConfig["EmailNotifications"] == "Enabled":
            # Email sending is enabled, send email
            mail.send("File "+filename+" not found","Failure")
    except:
        logger.error("Error while accessing the file "+filename)
        if XmlManager.primaryConfig["EmailNotifications"] == "Enabled":
            # Email sending is enabled, send email
            mail.send("Error while accessing the file "+filename,"Failure")
    finally:
        handle.close()
    return filedata

def check_if_path_exists(path):
    return os.path.exists(path)

def get_all_paths_to_backup(check_paths_existence=False):
    paths=[]
    #path_data_file = "validated_paths"  #this file holds all the validated paths to backup for this session, fetch the name of this file from configuration file
    path_data_file = XmlManager.primaryConfig["CheckedPathsFileName"]  #this file holds all the validated paths to backup for this session, fetch the name of this file from configuration file
    if check_paths_existence is True:
        # Fetch all paths required to be backed up from a configuration filename into the below list
        paths = XmlManager.paths      # These paths maybe incorrect, include a check to cater this
        loop_counter = len(paths)
        for path in paths:
            if check_if_path_exists(path) is True and loop_counter > 1:
                path_to_write = path+","
            elif check_if_path_exists(path) is True and loop_counter == 1:
                path_to_write = path

            write_to_text_file(path_data_file, path_to_write)
            loop_counter -=1
    else:
        response = get_txt_file_data(path_data_file)
        if response != "":
            paths = response.split(",")
    return paths


def can_backup_be_created(free_space_backup_drive):
    all_paths = get_all_paths_to_backup(True)
    total_diskspace_required = 0
    for path in all_paths:
        total_diskspace_required=total_diskspace_required+get_size(path)
        # Performing a look ahead check if the drive is full
        if total_diskspace_required-free_space_backup_drive > 0:
            # Insufficient space on backup drive, return false
            return False
    return True

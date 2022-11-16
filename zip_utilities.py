import pathlib
import zipfile
import config
import pandas as pd
import logging
import logging_utility

# Very useful: https://realpython.com/python-zipfile/
# EXAMPLE OF ZIPPING A FOLDER

# def configure_logging(logfile):
    # https: // realpython.com / python - logging /
    # logging.debug('This is a debug message')
    # logging.info('This is an info message')
    # logging.warning('This is a warning message')
    # logging.error('This is an error message')
    # logging.critical('This is a critical message')
    # This does not work:
    #       logging.basicConfig(filename=logfile, filemode='w', format='%(name)s - %(levelname)s - %(message)s')


    # Create a custom logger
    # From https://realpython.com/python-logging/
#    logger_intern=logging.getLogger()
#    logger_intern.setLevel(logging.INFO)
#    file_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
#    file_handler=logging.FileHandler(logfile, 'w')
 #   file_handler.setLevel(logging.INFO)
  #  file_handler.setFormatter(file_format)
#    logger_intern.addHandler(file_handler)
 #   return logger_intern

# TODO: Refactoring to CLASS?: to have as inner property or in constructor
#  the logger, but the benefit is not that big as logger is accessed staticly...



def fetchListDirectoriesFromFile(fileListDirectories):
    file=open(fileListDirectories,'r')
    # return file.readlines()
    #   This works OK!!
    #   return [r'U:\trainM_courses', r'C:\Users\AAL7FE\Desktop\respaldo']
    dataframe = pd.read_csv(fileListDirectories, delimiter=",")
    listDirectories = dataframe["directory"]
    # print(f'Display column with name: directory:\n\r{listDirectories}')
    logging.info("--------- fetchListDirectoriesFromFile -------------")
    logging.info(f'Display column with name: directory -> List of files to process: {listDirectories.to_list()}')
    return listDirectories.to_list()

def zipDirectory(directoryPath):
    # directory = pathlib.Path(config.folder_to_zip)
    directory = pathlib.Path(directoryPath)
    path_to_zip_file = pathlib.Path(str(directory) + '.zip')
    with zipfile.ZipFile(path_to_zip_file, mode="w") as archive:
        for file_path in directory.rglob("*"):
            archive.write(file_path, arcname=file_path.relative_to(directory))
# This works great!!

def printDirZipFile(directoryPath):
    logging.info("--------- printDirZipFile -------------")
    directory = pathlib.Path(directoryPath)
    path_to_zip_file = pathlib.Path(str(directory) + '.zip')
    with zipfile.ZipFile(path_to_zip_file, mode="r") as archive:
        archive.printdir() # this shows file list in console (Not in log file)
        # List files to log file:
        # https: // thispointer.com / python - how - to - get - the - list - of - all - files - in -a - zip - archive /
        #    Unfortunately, info about 'Modified' and 'Size' is not shown -> Try converting printdir to string
        listOfFiles=archive.namelist()
        for file in listOfFiles:
            logging.info(file)



def zipDirectoriesFromFile(fileToDirectoriesFile):
    listDirectories=fetchListDirectoriesFromFile(fileToDirectoriesFile)
    logging.info(f"List of directories to zip: {listDirectories}")
    for directory in listDirectories:
        zipDirectory(directory)
        logging.info(f"Finished zipping: {directory}")
        logging.info(f"Contents of zipped file: {directory}")
        printDirZipFile(directory)
        logging.info("----------------------------------")
    logging.info("All folders zipped correctly")

def main_method():
    try:
        logger = logging_utility.configure_logging(config.log_file)
        logger.info("Testing the logger")
        zipDirectoriesFromFile('directoriesList.txt')
        logger.info("Finished OK")
    except Exception as e:
        logging.exception(e)
    # Check that this works OK:
        # zipDirectory(r'U:\test_intruntime_u')
        # printDirZipFile(r'U:\test_intruntime_u.zip')

# folder_to_zip=r'U:\0_cc-pj-con'
# path_to_zip_file=r'U:\directory.zip'
# print(directory)
# print(path_to_zip_file)

# main_method()
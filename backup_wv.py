import config
import logging
import logging_utility
import gdrive_utility
import zip_utilities

def main_method():
    try:
        logger = logging_utility.configure_logging(config.log_file)
        logger.info("Testing the logger")
        zip_utilities.zipDirectoriesFromFile('directoriesList2.txt')
        listZipsToUpload = findListZipsFromDirectories('directoriesList2.txt')
        logger.info(f'List of zip files to upload: {listZipsToUpload}')
        gdrive = gdrive_utility.login_to_gdrive(config.path_to_credentials_module)
        # gdrive_utility.test_upload_list_files(gdrive, zip_utilities.fetchListDirectoriesFromFile('directoriesListGDrive2.txt'),'1NN6uOxAm-h2DCrlNobo_2hZcGONc2szX')
        gdrive_utility.test_upload_list_files(gdrive, listZipsToUpload, '1NN6uOxAm-h2DCrlNobo_2hZcGONc2szX')
        logger.info("Finished OK")
    except Exception as e:
        logging.exception(e)


def findListZipsFromDirectories(fileWithDirectories):
    listDirectories = zip_utilities.fetchListDirectoriesFromFile(fileWithDirectories)
    listZipsToUpload = []
    for directory in listDirectories:
        listZipsToUpload.append(str(directory) + '.zip')
    return listZipsToUpload


main_method()



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

#-------------------------------------------------------------------
# FUNCTIONS findListZipsFromDirectories, findListZipsFromDirectoriesOptimized, findListZipsFromDirectoriesOptimizedWithLambda
# are equivalent -
def findListZipsFromDirectories(fileWithDirectories):
    listDirectories = zip_utilities.fetchListDirectoriesFromFile(fileWithDirectories)
    listZipsToUpload = []
    for directory in listDirectories:
        listZipsToUpload.append(str(directory) + '.zip')
    print("first version:" + str(listZipsToUpload))
    return listZipsToUpload


def findListZipsFromDirectoriesOptimized(fileWithDirectories):
    listDirectories = zip_utilities.fetchListDirectoriesFromFile(fileWithDirectories)
    # WAY 2: Using one-liner -> UNIQUE IN PYTHON (cool!)
    listZipsToUpload=[i+'.zip' for i in listDirectories]
    print("optimized version:" + str(listZipsToUpload))
    return listZipsToUpload


def findListZipsFromDirectoriesOptimizedWithLambda(fileWithDirectories):
    listDirectories = zip_utilities.fetchListDirectoriesFromFile(fileWithDirectories)
    # WAY 3: Using map and lambda:
    listZipsToUpload=list(map(lambda file:file+'.zip',listDirectories))
    print("optimized version with map and lambda:" + str(listZipsToUpload))
    return listZipsToUpload

# ------------------------------------------------------------------------
main_method()




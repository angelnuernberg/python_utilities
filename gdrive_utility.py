import pandas as pd
import logging
import config

# https://www.youtube.com/watch?v=ZI4XjwbpEwU
# https://github.com/aluna1997/Python_and_PyDrive2/blob/main/GoogleDrivePyDrive.py
# 1. Get credentials:  console.cloud.google.com
# 2. Create a project: python-gdrive  (Location: no organization)
#      -> Select as service: "Google Driver API" -> Enable
#      -> Configure Tab "Oath consent screen": User type = External
#           - app name: "python-gdrive-utility"
#           - user support email: my gmail account
#           - app logo: empty
#           App domain:
#               - Application home page:
#               - Application privacy policy link:
#               - Application terms of service link:
#           Authorized domains: google.com
#           Developer contact information: my gmail account
#           Save and continue
#       -> Configure tab: "scopes" -> leave default settings
#       -> Configure tab: "test users" -> add users= add my gmail
#       -> Back to dashboard
#       -> Credentials: Create Oauth client id -> Application type: "Desktop app"
#               -> Name of client: "Desktop client 1" (default)
#               -> Download the credentials json from google and rename it to client_secrets.json
#  3. Install dependencies:
#        -> pip3 install PyDrive2 (Via package explorer of IDE)
#  4. Run register_to_gdrive.py (Just the first time)
#  5. Configure settings.yaml and execute again register_to_gdrive.py
#        -> Browser opens and you need to log in to google acount and trust app
#        -> After "authentication successful", a file "credentials_module.json" is created
#                   (Contains credentials for automatic authentication)



# client_id=oath_credentials.client_id
# client_secret=oath_credentials.client_secret

from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

path_to_credentials_module = config.path_to_credentials_module

def configure_logging(logfile):
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
    logger_intern=logging.getLogger()
    logger_intern.setLevel(logging.INFO)
    file_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    file_handler=logging.FileHandler(logfile, 'w')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(file_format)
    logger_intern.addHandler(file_handler)
    return logger_intern

def login_to_gdrive(path_to_credentials_module):
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile(path_to_credentials_module)
    if gauth.access_token_expired:
        gauth.Refresh()
        gauth.SaveCredentialsFile(path_to_credentials_module)
        logging.info("--------- Login_to_gdrive -------------")
        logging.info("Logged OK")
    else:
        gauth.Authorize()
    return GoogleDrive(gauth)


def upload_file_to_gdrive(gdrive, file_path, id_folder):
    # gdrive = login_to_gdrive(config.path_to_credentials_module)
    # id_folder='1NN6uOxAm-h2DCrlNobo_2hZcGONc2szX'
    # gDrive folder: backup_wv
    # https: // www.projectpro.io / recipes / upload - files - to - google - drive - using - python
    gfile_to_upload = gdrive.CreateFile({'parents': [{"kind": "drive#fileLink", "id": id_folder}]})
    gfile_to_upload['title'] = file_path.split("\\")[-1]
    gfile_to_upload.SetContentFile(file_path)
    gfile_to_upload.Upload()
    logging.info("--------- upload_file_to_gdrive -------------")
    print(f"File uploaded: {file_path}")
    logging.info(f"File uploaded: {file_path}")

def upload_files_to_gdrive(listOfFilePaths, id_folder):
    gdrive = login_to_gdrive(config.path_to_credentials_module)
    for filepath in listOfFilePaths:
        upload_file_to_gdrive(gdrive,filepath,id_folder)
    logging.info("--------- upload_files_to_gdrive -------------")
    print(f'All files uploaded OK')
    logging.info(f'All files uploaded OK')

def fetchDirectoriesToZip(fileListDirectories):
    file=open(fileListDirectories,'r')
    # return file.readlines()
    #   This works OK!!
    #   return [r'U:\trainM_courses', r'C:\Users\AAL7FE\Desktop\respaldo']
    dataframe = pd.read_csv(fileListDirectories, delimiter=",")
    listDirectories = dataframe["directory"]
    print(f'Display column with name: directory:\n\r{listDirectories}')
    logging.info("--------- fetchDirectoriesToZip -------------")
    logging.info(f'Display column with name: directory:{listDirectories.to_list()}')
    return listDirectories.to_list()

# DESCARGAR UN ARCHIVO DE DRIVE POR ID
def bajar_archivo_por_id(id_drive,ruta_descarga):
    credenciales =login_to_gdrive(config.path_to_credentials_module)
    archivo = credenciales.CreateFile({'id': id_drive})
    nombre_archivo = archivo['title']
    archivo.GetContentFile(ruta_descarga + nombre_archivo)
    print(f'File downloaded OK: {ruta_descarga}{nombre_archivo}')
    logging.info("--------- bajar_archivo_por_id -------------")
    logging.info(f'File downloaded OK: {ruta_descarga}{nombre_archivo}')

# DESCARGAR UN ARCHIVO DE DRIVE POR NOMBRE
def bajar_acrchivo_por_nombre(nombre_archivo,ruta_descarga):
    logging.info("--------- bajar_archivo_por_nombre -------------")
    credenciales = login_to_gdrive(config.path_to_credentials_module)
    lista_archivos = credenciales.ListFile({'q': "title = '" + nombre_archivo + "'"}).GetList()
    if not lista_archivos:
        print('No se encontro el archivo: ' + nombre_archivo)
        logging.info('No se encontro el archivo: ' + nombre_archivo)
        return
    archivo = credenciales.CreateFile({'id': lista_archivos[0]['id']})
    archivo.GetContentFile(ruta_descarga + nombre_archivo)
    print(f'File downloaded OK: {ruta_descarga}{nombre_archivo}')
    logging.info(f'File downloaded OK: {ruta_descarga}{nombre_archivo}')

id_folder = '1NN6uOxAm-h2DCrlNobo_2hZcGONc2szX'  # Id of folder 'backup_wv'
# to get Id_folder, go to 'get link' for the folder, copy the url at browser
#  and extract the id

def test_upload_one_file(gdrive,id_folder):
    # TEST upload one file: works OK
    file_path = 'requirements.txt'
    upload_file_to_gdrive(gdrive,file_path, id_folder)

def test_upload_list_files():
    # TEST upload list of files to Gdrive -> works OK!
    upload_files_to_gdrive(fetchDirectoriesToZip('directoriesListGDrive.txt'),id_folder)

def test_download_file_by_id():
    # TEST download file by id: Works OK!
    id_file='1rZJnwoBvBcJxKJerU0fjdZvTa-N3S2cm'
    # ruta_descarga='' # To download to same directory of script
    ruta_descarga=r'C:/Users/Angel/Desktop/scooter/'
    # ruta_descarga=r'H:/FiestaAbschlussBWM/'
        # Importante: utilizar / para ruta descarga e incluir / al final!
    bajar_archivo_por_id(id_file,ruta_descarga)
    print("finished OK")

def test_bajar_archive_por_nombre():
    nombre_archivo='destino_heidelberg15.zip'
    ruta_descarga=r'H:/FiestaAbschlussBWM/'
    bajar_acrchivo_por_nombre(nombre_archivo,ruta_descarga)


# MAIN:
try:
    logger = configure_logging(config.log_file)
    gdrive = login_to_gdrive(config.path_to_credentials_module)
    test_upload_one_file(gdrive,id_folder)
    test_upload_list_files()
    test_download_file_by_id()
    test_bajar_archive_por_nombre()
    print('Finished OK ')
except Exception as e:
    logging.exception(e)
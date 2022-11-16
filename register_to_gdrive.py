from pydrive2.auth import GoogleAuth

gauth=GoogleAuth()
gauth.LocalWebserverAuth()

# This needs to be done the first time -> a browser opens, you enter your google
# login, you need to confirm to trust the app
# If it worked OK, you get the message "Authentication successful"
# however, this authentication is temporal : to persist credentials, a settings.yaml file needs to be defined
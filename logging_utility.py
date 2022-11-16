import logging

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
    file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s',"%Y-%m-%d %H:%M:%S")
    file_handler=logging.FileHandler(logfile, 'w')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(file_format)
    logger_intern.addHandler(file_handler)
    return logger_intern

 # TODO: Refactoring to CLASS?: I do not see really the point, as the logger is used in other modules
 #  only by configuring it
 # logger = configure_logging(config.log_file)
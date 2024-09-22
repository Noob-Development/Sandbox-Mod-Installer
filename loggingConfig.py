# logging_config.py
import logging

def setupLogging(log_file='SandboxInstallOutput.txt'):
    logger = logging.getLogger('log')
    logger.setLevel(logging.DEBUG)

    # Check if handlers already exist to avoid duplicate logs
    if not logger.handlers:
        cli_handler = logging.StreamHandler()
        file_handler = logging.FileHandler(log_file)

        cli_handler.setLevel(logging.INFO)
        file_handler.setLevel(logging.DEBUG)

        cli_formatter = logging.Formatter('[%(levelname)s] %(message)s', '%H:%M:%S')
        file_formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', '%H:%M:%S')

        cli_handler.setFormatter(cli_formatter)
        file_handler.setFormatter(file_formatter)

        logger.addHandler(cli_handler)
        logger.addHandler(file_handler)

    return logger
import logging
import configProvider
import configparser
from resources import Resources


def getLogger():
    logLevel = configProvider.getConfigEntryOrDefault('Logging', 'APPLICATION_LOG_LEVEL', logging.DEBUG)
    logger = logging.getLogger("DSEGenerator")
    logger.setLevel(logLevel)

    fileHandler = logging.FileHandler(Resources.getLogFile())
    fileHandler.setLevel(logLevel)
    consoleHandler = logging.StreamHandler()
    consoleHandler.setLevel(logLevel)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    fileHandler.setFormatter(formatter)
    consoleHandler.setFormatter(formatter)
    logger.addHandler(fileHandler)
    logger.addHandler(consoleHandler)
    return logger

def getLoggerCtx(context):
    logLevel = configProvider.getConfigEntryOrDefault('Logging', 'APPLICATION_LOG_LEVEL', logging.DEBUG)
    logger = logging.getLogger(context)
    logger.setLevel(logLevel)

    fileHandler = logging.FileHandler(Resources.getLogFile())
    fileHandler.setLevel(logLevel)
    consoleHandler = logging.StreamHandler()
    consoleHandler.setLevel(logLevel)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    fileHandler.setFormatter(formatter)
    consoleHandler.setFormatter(formatter)
    logger.addHandler(fileHandler)
    logger.addHandler(consoleHandler)
    return logger
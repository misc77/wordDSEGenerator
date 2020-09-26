from resources import Resources
import configparser


def getConfigEntry(group, item):
    entry = None
    if group != None and item != None:
        config = configparser.ConfigParser()
        try:
            config.read(Resources.getConfigFile())
        except(FileNotFoundError):
            print("ERROR: File '" + Resources.getConfigFile() + "' NOT found! " + FileNotFoundError.strerror)
            config = None
        if config is not None and group in config:
            entry = config[group].getint(item)
    
    return entry

def getConfigEntryOrDefault(group, item, defaultValue=None):
    entry = None
    entry = getConfigEntry(group, item)
    if entry is None:
        entry = defaultValue

    return entry
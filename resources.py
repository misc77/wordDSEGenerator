from pkg_resources import resource_filename
import wx

class Resources:
    templatePath = "/templates"
    outputPath = "/output"
    configPath = "/config"
    inputPath = "/test/data/input/"
    graphicsPath = "/gfx"
    logPath = "/log"
    configFile = "config.ini"
    headerImage = "header.png"
    dseTemplate = "dse_template_v.xml"
    youtubeTemplate = "youtube_template_v.xml"
    facebookTemplate = "facebook_template_v.xml"
    instagramTemplate = "instagram_template_v.xml"
    twitterTemplate = "twitter_template_v.xml"
    checklistTemplate = "checkliste_template_v.xml"
    logFile = "DSEGenerator.log"
    dsbList = "/data/datenschutzbehoerden.xml"

    @staticmethod
    def getHeaderImage():
        """getHeaderImage: returns filename of Header image
        """
        return Resources.get_filename(Resources.graphicsPath + "/" + Resources.headerImage)

    @staticmethod
    def getDSBList():
        """getDSBList: returns filename of list of datenschutzbehörden
        """
        return Resources.get_filename(Resources.dsbList)

    @staticmethod
    def getDSETemplate(template = dseTemplate, version = "1.0"):
        """getDSETemplate 
        returns the filename of DSE Template for corresponding version.
        
        Keyword Arguments:
            version {str} -- [description] (default: {"1.0"})
        """
        return Resources.get_filename(Resources.templatePath + "/" + Resources.getVersion(template, version))

    @staticmethod
    def getChecklisteTemplate(version = "1.0"):
        return Resources.get_filename(Resources.templatePath + "/" + Resources.getVersion(Resources.checklistTemplate, version))

    @staticmethod
    def get_filename(path):
        try:
            filename = resource_filename(__name__, path)
            return filename
        except(FileNotFoundError):
            wx.MessageBox("Error occured by determining resource! " + FileNotFoundError.strerror(), caption="Error occured!")

    @staticmethod
    def getVersion(filename, version):
        return filename.split(".")[0] + version + "." + filename.split(".")[1]

    @staticmethod
    def getOutputPath():
        relativPath = Resources.outputPath
        filename = resource_filename(__name__, relativPath)
        return filename

    @staticmethod
    def getInputPath():
        relativPath = Resources.inputPath
        filename = resource_filename(__name__, relativPath)
        return filename

    @staticmethod
    def getConfigFile():
        filename = resource_filename(__name__, Resources.configPath + "/" + Resources.configFile)
        return filename

    @staticmethod
    def getLogFile():
        filename = resource_filename(__name__, Resources.logPath + "/" + Resources.logFile)
        return filename

    @staticmethod
    def validVersions(versionA="1.0", versionB="1.0"):
        if versionA == versionB:
            return True
        else:
            return False

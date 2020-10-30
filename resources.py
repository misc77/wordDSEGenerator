from pkg_resources import resource_filename
import wx

class Resources:
    templatePath = "/templates"
    outputPath = "/output"
    configPath = "/config"
    graphicsPath = "/gfx"
    logPath = "/log"
    configFile = "config.ini"
    headerImage = "header.png"
    dseTemplate = "dse_template_v.xml"
    checklistTemplate = "checkliste_template_v.xml"
    logFile = "DSEGenerator.log"

    @staticmethod
    def getHeaderImage():
        """getHeaderImage: returns filename of Header image
        """
        return Resources.get_filename(Resources.graphicsPath + "/" + Resources.headerImage)

    @staticmethod
    def getDSETemplate(version = "1.0"):
        """getDSETemplate 
        returns the filename of DSE Template for corresponding version.
        
        Keyword Arguments:
            version {str} -- [description] (default: {"1.0"})
        """
        return Resources.get_filename(Resources.templatePath + "/" + Resources.getVersion(Resources.dseTemplate, version))

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

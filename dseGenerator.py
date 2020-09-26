import logger

from checklistParser import parseChecklist
from docGenerator import DocGenerator
from resources import Resources

class DSEGenerator():
    def __init__(self):
        self.checklistFile = "C:/Users/misc2/Documents/PyProjects/DSEGenerator/test/data/checkliste.docx"
        self.checklistObject = None

    def startProcessing(self):
        log = logger.getLogger()
        if self.checklistFile != None:
            if self.checklistObject != None:
                checklistObject = parseChecklist( self.checklistFile )
            if checklistObject is not None:
                docGenerator = DocGenerator(checklistObject)
                retval = docGenerator.saveDocument()
                if retval == True:
                    log.info("Document processed successfully!")
                else:
                    log.error("Document hasn't been created! Error occured during processing!")
            else:
                log.error("Checklist Document hasn't been processed!")
        else:
            log.warn("Aborted processing because of missing checklist file: '" + self.checklistFile + "'!")

import logger

from checklistParser import parseChecklist
from docGenerator import DocGenerator
from resources import Resources

class DSEGenerator():
    def __init__(self):
        self.checklistFile = ""
        self.checklistObject = None

    def setChecklistFile(self, file):
        self.checklistFile = file

    def getChecklistFile(self):
        return self.checklistFile

    def setChecklistObject(self, xmlObject):
        self.checklistObject = xmlObject

    def getChecklistObject(self):
        return self.checklistObject


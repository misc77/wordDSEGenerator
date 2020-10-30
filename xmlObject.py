import const

from datetime import date
from filter import Filter

class XMLObject:
        
    def __init__ (self):
        self.elementList = {}
        self.wordVersion = ""
        self.xmlVersion = ""
        self.created = date.today()
        self.filter = Filter()

    def __str__ (self):
        stringRepresentation = "created: " + str(self.created) + " \n"
        stringRepresentation += "wordVersion: " + self.wordVersion + " \n"
        stringRepresentation += "xmlVersion: " + self.xmlVersion + " \n"
        stringRepresentation += "content: " + str(self.elementList)
        return stringRepresentation        

    def setElementList(self, elementList):
        self.elementList = elementList

    def addElement(self, elementName, element):
        self.elementList[elementName] = element

    def addElementEntry(self, elementName, key, value):
        self.elementList[elementName][key] = value 
      
    def getElement(self, elementName):
        return self.elementList[elementName]

    def getElementList(self):
        return self.elementList

    def getValue(self, elementName, key):
        return self.catchNull(self.elementList[elementName][key])

    def getText(self, elementName, key):
        return self.catchNull(self.elementList[elementName][key].split("\n")[1])

    def getValueByPos(self, position):
        return self.elementList[position]

    def getListToString(self, elementName, key, prefix, postfix, delimiter):
        keyList = ""
        element = ""
        for e in self.elementList[elementName][key]:
            element = self.filter.applyTextFilter(e)
            if element != None and len(element) > 0:
                keyList += prefix + element + postfix + delimiter
        if keyList.endswith(delimiter):
            keyList = keyList[0:len(keyList)-1]
        return keyList

    def getKeyList(self, elementName, key):
        return self.catchNull(self.getListToString(elementName, key, "", "", ", "))

    def getFormattedKeyList(self, elementName, key):
        return self.catchNull(self.getListToString(elementName, key, "• ", "", "\n"))

    def catchNull(self, text):
        if text == None or len(text) == 0:
            text = const.NULL_STRING
        return text
        
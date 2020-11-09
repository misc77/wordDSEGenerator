import const

from datetime import date
from filter import Filter

class OutputDoc:
    def __init__ (self, name, template, cond ):
        self.template = template
        self.cond = cond 
        self.name = name
    
    def setDoc( self, name, template, cond):
        self.template = template
        self.name = name
        self.cond = cond

    def getTemplate(self):
        return self.template

    def getName(self):
        return self.name
    
    def getCond(self):
        return self.cond

class XMLObject:
        
    def __init__ (self):
        self.elementList = {}
        self.template = ""
        self.created = date.today()
        self.filter = Filter()
        self.outputDocs = []

    def __str__ (self):
        stringRepresentation = "created: " + str(self.created) + " \n"
        stringRepresentation += "template: " + self.template + " \n"
        stringRepresentation += "content: " + str(self.elementList)
        return stringRepresentation        

    def setTemplate(self, template):
        self.template = template

    def getTemplate(self):
        return self.template

    def setElementList(self, elementList):
        self.elementList = elementList

    def addElement(self, elementName, element):
        self.elementList[elementName] = element

    def addElementEntry(self, elementName, key, value):
        self.elementList[elementName][key] = value
    
    def addOutputDoc(self, name, template, cond):
        doc = OutputDoc(name, template, cond)
        self.outputDocs.append(doc)

    def getOutputDocs(self):
        return self.outputDocs
      
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
        
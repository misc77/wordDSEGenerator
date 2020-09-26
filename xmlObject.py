from datetime import date

class XMLObject:
        
    def __init__ (self):
        self.elementList = {}
        self.wordVersion = ""
        self.xmlVersion = ""
        self.created = date.today()

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
        return self.elementList[elementName][key]

    def getValueByPos(self, position):
        return self.elementList[position]

    def getKeyList(self, elementName, key):
        keyList = ""
        for e in self.elementList[elementName][key]:
            print("key " + key + " in elementName " + elementName + " element " + e )
            keyList += e + ", "
        if keyList.endswith(","):
            keyList = keyList[0:len(keyList)-1]
        return keyList
        
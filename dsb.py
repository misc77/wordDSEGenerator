class DSB:
    def __init__(self):
        self.name = ""
        self.address = ""
        self.phone = ""
        self.fax = ""
        self.email = ""
        self.internet = ""
        self.country =""
        self.state =""
    
    def getName(self):
        return self.name
    
    def getAddress(self):
        return self.address

    def getPhone(self):
        return self.phone
    
    def getFax(self):
        return self.fax
    
    def getEmail(self):
        return self.email

    def getInternet(self):
        return self.internet
    
    def getCountry(self):
        return self.country
    
    def getState(self):
        return self.state

    def setName(self, name):
        self.name = name
    
    def setAddress(self, address):
        self.address = address

    def setPhone(self, phone):
        self.phone = phone
    
    def setFax(self, fax):
        self.fax = fax
    
    def setEmail(self, email):
        self.email = email

    def setInternet(self, internet):
        self.internet = internet
    
    def setCountry(self, country):
        self.country = country
    
    def setState(self, state):
        self.state = state

    def toString(self, separator = "\n"):
        string = ""
        string = self.getName() + separator
        string = string + self.getAddress() + separator
        string = string + self.getState() + separator
        string = string + self.getCountry() + separator
        string = string + self.getPhone() + separator
        string = string + self.getFax() + separator
        string = string + self.getEmail() + separator
        string = string + self.getInternet()
        return string
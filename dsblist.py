import xml.etree.ElementTree as ET
import const
import logger

from const import DSBDOC_ATTRIB_LAND
from dsb import DSB
from resources import Resources

class DSBList:
    def __init__(self):
        self.dsbList = self.readFile()
        
    def readFile(self):
        log = logger.getLogger()
        liste = []
        
        filename = Resources.getDSBList()
        try:
            tree = ET.parse(filename)   
        except(ET.ParseError):
            tree = None
            log.error("Error occured when parsing XML document '" + filename + "'! " + ET.ParseError.text)
        if tree is not None:
            root = tree.getroot()
            for elem in root:
                if elem.tag == const.DSBDOC_TAG_DSB:
                    dsb = DSB()
                    dsb.setState(elem.attrib.get(const.DSBDOC_ATTRIB_BUNDESLAND))
                    dsb.setCountry(elem.attrib.get(const.DSBDOC_ATTRIB_LAND))
                    for sub in elem:
                        if sub.tag == const.DSBDOC_TAG_NAME:
                            dsb.setName(sub.text)
                        if sub.tag == const.DSBDOC_TAG_ANSCHRIFT:
                            dsb.setAddress(sub.text)
                        if sub.tag == const.DSBDOC_TAG_EMAIL:
                            dsb.setEmail(sub.text)
                        if sub.tag == const.DSBDOC_TAG_TELEFON:
                            dsb.setPhone(sub.text)
                        if sub.tag == const.DSBDOC_TAG_FAX:
                            dsb.setFax(sub.text)
                        if sub.tag == const.DSBDOC_TAG_INTERNET:
                            dsb.setInternet(sub.text)
                    liste.append(dsb)
        return liste

    def getDSBbyCountryState(self, country, state):
        result = DSB()
        for dsb in self.dsbList:
            if dsb.getCountry() == country and dsb.getState() == state:
                result = dsb
                break
        return result

    def getDSBList(self):
        return self.dsbList      

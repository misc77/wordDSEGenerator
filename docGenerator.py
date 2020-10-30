"""Generates DSE Document based on dse Template information

Returns:
    [type] -- [description]
"""
import os
import xml.etree.ElementTree as ET
import const
import logger
import datetime

from docx import Document
from docx.shared import Pt
from resources import Resources

class DocGenerator:
    """DocGenerator:
    """
   
    def __init__(self, checklist):
        self.checklistObject = checklist
        self.dseTemplate = {}
        self.dseDocument = None
        self.processed = False

    def applyDocFormatting(self):
        style = self.dseDocument.styles['Normal']
        font = style.font
        font.name = "Arial"
        font.size = Pt(12)

        style = self.dseDocument.styles['Heading 1']
        font = style.font
        font.name = "Arial"
        font.size = Pt(16)

        style = self.dseDocument.styles['Heading 2']
        font = style.font
        font.name = "Arial"
        font.size = Pt(14)
        font.bold = True

        style = self.dseDocument.styles['Heading 3']
        font = style.font
        font.name = "Arial"
        font.size = Pt(12)
        font.bold = True

    def containsElement(self, array, element):
        """[summary]Checks for element in list
        
        Arguments:
            array {[type]} -- [description]
            element {[type]} -- [description]
        
        Returns:
            [type] -- [description]
        """
        print ("element: " + element)
        for item in array:
            print("find " + element + " in " + item)
            if item.find(element) == -1:                
                continue
            else:
                print("element " + element + " found!")
                return True
        return False

    def compareElementValue(self, dictionary, element, value, exact_match = False):
        """Compares value of element in Dictionary structure
        
        Arguments:
            dictionary {[type]} -- [description]
            element {[type]} -- [description]
            value {[type]} -- [description]
        
        Returns:
            [type] -- [description]
        """        
        if exact_match:
            if element in dictionary:
                return dictionary[element] == value
        else:
            for item in dictionary.keys():
                if item.find(element) == -1:
                    continue
                else:
                    return (str(dictionary[item]) == str(value))
        return False 

    def evaluateCondition(self, text):
        """evalutate conditions given in Mapping template for DSE Document
        
        Arguments:
            text {[type]} -- [description]
        """
        log = logger.getLogger()
        condition = False
        if text != "":
            try:
                condition = eval(text)
            except Exception (IndexError, OverflowError, SyntaxError, TypeError, NameError):                    
                log.warning("Error occured! Skipped evaluation! Condition to evaluate '" + text + "' will return False." )
        return condition

    def evaluateFormular(self, text):
        """evalutate formulars given in Mapping template for DSE Document
        
        Arguments:
            text {[type]} -- [description]
        """
        log = logger.getLogger()
        try:
            startpos = text.index("{")
        except(ValueError):
            return text
        if startpos > 0:
            endpos = text.index("}")+1
            if endpos > startpos:
                skript = text[startpos:endpos]
                cleanSkript = skript.replace("{","").replace("}","")
                try:
                    text = text.replace(skript, eval(cleanSkript)) 
                except (IndexError, OverflowError, SyntaxError, TypeError, NameError):                    
                    log.warning("Error occured! Skipped evaluation! String to evaluate '" + text + "' will be replaced by ''.")
                    text = text.replace(skript, "")    

                if text.count("{") > 0:
                    text = self.evaluateFormular(text)
            else:
                log.warning("Skipped processing! End position of symbol of text to evaluate is before start position (start:" + startpos +", end:" + endpos+")")
        return text

    def processText(self, text_elem):
        cond = ""
        text = text_elem.text
        cond = text_elem.attrib.get(const.DSEDOC_ATTRIB_COND)
        if cond != "" and cond != None:
            condition = self.evaluateCondition(cond)
            if condition is True:
                text = self.evaluateFormular(text)
            else:
                text = ""
        else:
            text = self.evaluateFormular(text)
        return text

    def processTable(self, table_elem):  #TODO
        text = table_elem.text
        #for elem in table_elem:
       #     if elem.tag == const.DSEDOC_TAG_ROW:

        return text


    def processParagraph(self, paragraph, chapter_title, is_first_paragraph):
        is_first = True
        title = paragraph.attrib.get(const.DSEDOC_ATTRIB_TITLE)
        text = paragraph.text
        if text != "":
            for elem in paragraph:
                if elem.tag == const.DSEDOC_TAG_TEXT:
                    text = self.processText(elem)
                elif elem.tag == const.DSEDOC_TAG_TABLE:
                    text = self.processTable(elem)            
                if text != "": 
                    # Print header only if there is content to print
                    if is_first_paragraph == True and is_first == True and chapter_title != "":
                        self.dseDocument.add_heading(chapter_title, level=1)
                    if is_first and title != "":    
                        self.dseDocument.add_heading(title, level=2)
                    self.dseDocument.add_paragraph(text)
                    is_first = False


    def processChapter(self, chapter):
        is_first_paragraph = True
        title = chapter.attrib.get(const.DSEDOC_ATTRIB_TITLE)
        for elem in chapter:
            if elem.tag == const.DSEDOC_TAG_PARAGRAPH:
                self.processParagraph(elem, title, is_first_paragraph)
                is_first_paragraph = False


    def parseTemplate(self, version = "1.0"):
        log = logger.getLoggerCtx("DSEGenerator.docGenerator.parseTemplate")
        filename = Resources.getDSETemplate(version)
        try:
            tree = ET.parse(filename)   
        except(ET.ParseError):
            tree = None
            log.error("Error occured when parsing XML document '" + filename + "'! " + ET.ParseError.text)
        if tree is not None:
            root = tree.getroot()
            if Resources.validVersions(self.checklistObject.xmlVersion, root.attrib.get(const.DSEDOC_ATTRIB_VERSION)):
                self.dseDocument = Document()
                core_properties = self.dseDocument.core_properties
                core_properties.comments = "Checklist Version:" + self.checklistObject.wordVersion + ", Checklist Template Version: " + self.checklistObject.xmlVersion + ", DSE Document Template Version: " + root.attrib.get(const.DSEDOC_ATTRIB_VERSION)
                self.applyDocFormatting()
                for elem in root:
                    if elem.tag == const.DSEDOC_TAG_CHAPTER:
                        self.processChapter(elem)
                year = datetime.date.today().strftime("%Y")

                self.dseDocument.add_paragraph("@ " + year + " netvocat GmbH")
                self.processed = True 
            else:
                log.warning("Processing skipped because of invalid versions between Checklist template XML and DSE template XML!! ")


    def saveDocument(self, versionnumber=1, path=None):
        log = logger.getLoggerCtx("DSEGenerator.docGenerator.saveDocument")
        if path is None or len(path)==0:
            filename = Resources.getOutputPath() + "/" + self.checklistObject.created.strftime("%Y%m%d%H%M%S") + "_dseDocument_"+ versionnumber+".docx"  
        else:
            filename = path      
        try:
            self.dseDocument.save(filename)
        except (PermissionError):
            log.warning("File '" + filename + "' could not be written! " + PermissionError.strerror)
            filename = Resources.getOutputPath() + "/" + self.checklistObject.created.strftime("%Y%m%d%H%M%S") + "_dseDocument_"+ (versionnumber+1)+".docx"  
            self.saveDocument(filename)

        if os.path.isfile(filename):
            log.info("File '" + filename + "' has been written successfully!")
            return True
        
        log.warning("File '" + filename + "' has NOT been written! Please check error log!")
        return False


    
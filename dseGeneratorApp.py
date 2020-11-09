import configProvider
import logger
import wx
import toolbox
import os.path
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from dseGenerator import DSEGenerator
from docGenerator import DocGenerator
from checklistParser import parseChecklist
from resources import Resources
from dsblist import DSBList

class DSEGeneratorApp(wx.Frame):
    """DSEGeneratorApp
    Generates Documents based on Input documents in Word format. 
    To Parse input documents a specific template in XML format is necessary.
    Generation of output Document is done based on XML Template for mapping
    input document values to text blocks
    
    Arguments:
        wx {[Frame]} -- [description]
    """
    
    def __init__(self, *args, **kwargs):
        """init function
        """
        super(DSEGeneratorApp, self).__init__(*args, **kwargs)
        # Read Config for UI
        self.display_log_size = configProvider.getConfigEntryOrDefault('UI Setup', 'DISPLAY_LOG_SIZE', -500)
        #Scheduler   
        self.log_scheduler = BackgroundScheduler()
        self.generator = DSEGenerator()
        self.docList = []
        self.log_scheduler.add_job(self.log_update, 'interval', seconds=10, id='log_job')
        self.log_scheduler.start() 
        self.view_show_log_item = None
        self.ui_width = 1100
        self.ui_height_min = 500
        self.ui_height_max = 700  
        self.init_ui()   
        self.SetBackgroundColour("white")
        self.path = Resources.getOutputPath();       
    
    def init_ui(self):
        """[summary]
           Generates the UI of the Application
        """ 
        self.SetSize((self.ui_width, self.ui_height_max))
        self.SetTitle("Document Generator Application")
        self.Centre()
        self.panel = wx.Panel(self)
        self.sizer = wx.GridBagSizer(3,16)
        self.border = 10
        self.line = wx.StaticLine(self.panel, -1, style=wx.LI_VERTICAL)
        self.line.SetSize((100,30))
        
        #Header Graphic
        imageSizer = wx.BoxSizer(wx.HORIZONTAL)
        headerImage = wx.Image(Resources.getHeaderImage(), wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        img = wx.StaticBitmap(self.panel, -1, headerImage, (0, 0), (headerImage.GetWidth(), headerImage.GetHeight()))
        imageSizer.Add(img, flag=wx.LEFT)
        self.sizer.Add(imageSizer, pos=(0,0), span=(1, 3), flag=wx.TOP|wx.LEFT|wx.RIGHT)
        
        #Checklist Label
        checklist_label = wx.StaticText(self.panel, label="Input Document:")
        font = checklist_label.GetFont()
        font.PointSize += 2
        font = font.Bold()
        checklist_label.SetFont(font)
        self.sizer.Add(checklist_label, pos=(2,0), flag=wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, border=self.border)
        
        #FileDialog Button
        file_picker = wx.FilePickerCtrl(self.panel, path=Resources.getInputPath(), message="Please select a Input Document in *.docx Format:", wildcard="*.docx", style = wx.FLP_USE_TEXTCTRL )
        file_picker.SetTextCtrlGrowable(True)
        file_picker.SetTextCtrlProportion(10)
        self.sizer.Add(file_picker, pos=(2,1), span=(1,2), flag=wx.EXPAND|wx.LEFT|wx.RIGHT,border=self.border)

        #Used Template of Document selected
        version_label_xml = wx.StaticText(self.panel, label="Used Input XMLTemplate:")
        version_label_xml.SetFont(font)
        self.sizer.Add(version_label_xml, pos=(4,0), flag=wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, border=self.border)
        self.template_text_xml = wx.StaticText(self.panel)
        self.template_text_xml.SetFont(font)
        self.sizer.Add(self.template_text_xml, pos=(4,1),  flag=wx.EXPAND|wx.LEFT|wx.RIGHT, border=self.border)
        self.sizer.Add(self.line, pos=(6,0), span=(1,3), flag=wx.EXPAND|wx.LEFT|wx.RIGHT, border=self.border)

        #Status
        status_label = wx.StaticText(self.panel, label="Processing Status:")
        status_label.SetFont(font)
        self.sizer.Add(status_label, pos=(7,0), flag=wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, border=self.border)
        self.status_text = wx.StaticText(self.panel, label="Please select Checklist to read!")
        self.status_text.SetFont(font)
        self.sizer.Add(self.status_text, pos=(7,1), flag=wx.EXPAND|wx.LEFT|wx.RIGHT, border=self.border)
            
        #Buttons
        self.generate_button = wx.Button(self.panel, label="Generate output document!", name="generate")
        self.generate_button.Disable()
        self.sizer.Add(self.generate_button, pos=(9,0), flag=wx.LEFT|wx.ALIGN_CENTER_VERTICAL, border=self.border)
        self.Bind(wx.EVT_BUTTON, self.on_generate, self.generate_button)
        
        self.save_button = wx.Button(self.panel, label="Save output Document!", name="save")
        self.save_button.Disable()
        self.sizer.Add(self.save_button, pos=(9,1), flag=wx.LEFT|wx.ALIGN_CENTER_VERTICAL, border=self.border)
        self.Bind(wx.EVT_BUTTON, self.on_save, self.save_button)

        #Log 
        self.log_label = wx.StaticText(self.panel, label="Log:")
        self.sizer.Add(self.log_label, pos=(15,0), flag=wx.EXPAND|wx.LEFT|wx.RIGHT,  border=self.border)
        self.log_view = wx.TextCtrl(self.panel, size=(200,200), style=wx.TE_MULTILINE|wx.HSCROLL|wx.TE_READONLY|wx.TE_BESTWRAP|wx.TE_RICH2, pos=wx.DefaultPosition)
        self.log_view.SetEditable(False)
        self.sizer.Add(self.log_view, pos=(16,0), span=(3,3), flag=wx.EXPAND|wx.LEFT|wx.RIGHT, border=self.border)

        self.sizer.AddGrowableCol(2)
        self.panel.SetSizer(self.sizer)    

        self.init_menu()

        #Events
        self.Bind(wx.EVT_FILEPICKER_CHANGED, self.on_pick_file, file_picker)
        

    def init_menu(self):
        """ Initialize Menu
        """
        #Menubar
        menubar = wx.MenuBar()
        file_menu = wx.Menu()
        view_menu = wx.Menu()
        file_item = file_menu.Append(wx.ID_EXIT, 'Exit', 'Exit application')
        self.view_show_log_item = view_menu.Append(wx.ID_ANY, 'Show Log', 'Show Log View', kind=wx.ITEM_CHECK)
        view_menu.Check(self.view_show_log_item.GetId(), False)
        self.hide_log()
        menubar.Append(file_menu, '&File')
        menubar.Append(view_menu, '&View')
        self.SetMenuBar(menubar)
        #Events
        self.Bind(wx.EVT_MENU, self.on_exit, file_item)
        self.Bind(wx.EVT_MENU, self.on_show_log, self.view_show_log_item)

    #--- EVENT HANDLER FUNCTIONS
    def on_pick_file(self, evt):
        """Takes care of loading Checklist file
        Arguments:
            e {[type]} -- [description]
        """
        log = logger.getLogger()
        self.reset()
        if evt.GetPath() != None:
            self.generator.checklistFile = evt.GetPath()
            if os.path.isfile(self.generator.checklistFile):
                checklist_doc = parseChecklist(self.generator.checklistFile)
                if checklist_doc != None:
                    self.generator.checklistObject = checklist_doc
                    self.template_text_xml.SetLabelText(self.generator.checklistObject.getTemplate())
                    self.status_text.SetLabelText("Input Document successfully processed!")      
                    self.generate_button.Enable()    
                else:
                    self.status_text.SetLabelText("Input document could not be parsed! Please check input file!")
            else:
               self.status_text.SetLabelText("Input document could not be parsed! File '" + self.generator.checklistFile + "' does not exist!")       
        else:
            wx.MessageBox("Warning! No file has been selected! Please select a valid file in order to proceed!")
            log.warning("No file has been selected!")
    
    def on_generate(self, evt):
        """[summary]
        
        Arguments:
            e {[type]} -- [description]
        """
        log = logger.getLogger()
        log.info("Button pushed")
        if self.generator.checklistObject != None:
            self.generate_output()
        else:
            wx.MessageBox("Warning! Output Document can't be generated because of missing or incomplete parsed Input Document!", caption="Warning!")
            log.warning("No checklist has been parsed! Please select a valid checklist document!")

    def on_exit(self, evt):
        """[summary]
        
        Arguments:
            e {[type]} -- [description]
        """
        dlg = wx.MessageDialog  (self, 
                                "Do you really want to close this application?",
                                "Confirm Exit", wx.OK|wx.CANCEL|wx.ICON_QUESTION)
        result = dlg.ShowModal()
        dlg.Destroy()
        if result == wx.ID_OK:
            self.Close()

    def on_show_log(self, evt):
        """Shows/Hides the Log View
        
        Arguments:
            evt {[type]} -- [description]
        """
        if self.view_show_log_item.IsChecked():
            self.show_log()
        else:
            self.hide_log()    

    def on_save(self, evt):
        """Saves DSE Document to File system
        
        Arguments:
            evt {[type]} -- [description]
        """
        if self.docList is not None and len(self.docList) > 0:
            count = 0
            dlg = wx.DirDialog(self, "Please select destination directory to save generated document(s)!", Resources.getOutputPath(), wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
            now = datetime.datetime.now().strftime("%Y%m%d%H%M%S") 
            if dlg.ShowModal() == wx.ID_OK:
                self.path = dlg.GetPath()
                for doc in self.docList:
                    if doc.saveDocument(self.template_text_xml.GetLabelText(), self.path, now):
                        count = count + 1
                        self.status_text.SetLabelText(doc.name + " saved successfully!")   
                self.status_text.SetLabelText("All " + str(count) + " documents saved successfully!")   
                count = 0
            else:
                wx.MessageBox("Warning! Output Document hasn't been saved!", caption="Warning!")
        else:
            wx.MessageBox("Warning! Output Document has not yet generated! Please Generate output document when Input document has been read successfully!", caption="Warning!")  

    #--- End of Event Handler

    def hide_log(self):
        """Hides log view and reduces size of frame
        """
        self.log_view.Hide()
        self.log_label.Hide()
        self.log_scheduler.pause_job("log_job")
        self.SetSize((self.ui_width, self.ui_height_min)) 

    def show_log(self):
        """show Logview
        """
        self.log_view.Show()   
        self.log_label.Show()
        self.log_scheduler.resume_job("log_job")
        self.SetSize((self.ui_width, self.ui_height_max))

    def log_update(self):
        """
            Updates Logview with content of log file
        """
        file_handle = open(Resources.getLogFile(), "r")
        self.log_view.SetInsertionPoint(0)
        self.log_view.SetValue(file_handle.read())
        self.log_view.AppendText("")
        self.log_view.Refresh()
        file_handle.close()

    def generate_output(self):
        """ Generates DSE Document by 
        """
        #TODO: Implement concurrency!!
        count = 0
        self.status_text.SetLabelText("Output Document(s) are being processed...")
        
        if self.generator.checklistObject != None:
            for output in self.generator.checklistObject.getOutputDocs():
                if output.getCond() == "" or eval(output.getCond()):
                    doc = DocGenerator(self.generator.checklistObject, output.getName())
                    doc.parseTemplate(output.getTemplate())
                    self.docList.append(doc)
                    count = count +1
                    self.status_text.SetLabelText(output.getName() +" successfully processed!")

        self.status_text.SetLabelText(str(count) + " documents processed ! Ready to save to disc.")    
        count = 0
        self.save_button.Enable()     

    def reset(self):
        """Reset status of GUI
        """
        self.generate_button.Disable()
        self.save_button.Disable()
        self.generator = DSEGenerator()
        self.docList = []

def main():
    """Main Method
    """
    app = wx.App()
    ex = DSEGeneratorApp(None)
    ex.Show()
    app.MainLoop()     
    

if __name__ == '__main__':
    main()
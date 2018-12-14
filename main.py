#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# generated by wxGlade 0.8.3 on Fri Aug 31 03:44:54 2018
#

import wx
import wx.aui
import os
import random
import SummaryTab, FileTab, ImagesTab, AnalyzedDataTab, NewCaseDialog, mainmenu, search, searchTab, SessionsTab, DNSTab, CredentialsTab        
import connectdb
import subprocess
import sqlite3
from sqlite3 import Error
from pathlib import Path
import datetime, time
import re
from threading import Thread

# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode
# end wxGlade

openTabs = [0]

class mainFrame(wx.Frame):
    def __init__(self, parent):
        # begin wxGlade: mainFrame.__init__
        wx.Frame.__init__(self, parent=parent)
        self.SetSize((1280, 720))
        
        # Menu Bar
        self.frame_menubar = wx.MenuBar()
        wxglade_tmp_menu = wx.Menu()
        item = wxglade_tmp_menu.Append(wx.ID_ANY, "New case", "")
        self.Bind(wx.EVT_MENU, self.onNewCase, id=item.GetId())
        item = wxglade_tmp_menu.Append(wx.ID_ANY, "Open case", "")
        self.Bind(wx.EVT_MENU, self.onOpenCase, id=item.GetId())
        wxglade_tmp_menu.AppendSeparator()
        itemAddEvidenceBtn = wxglade_tmp_menu.Append(wx.ID_ANY, "Add PCAP File", "")                                      
        self.Bind(wx.EVT_MENU, self.onAddEvidence, id=itemAddEvidenceBtn.GetId())     
        wxglade_tmp_menu.AppendSeparator()
        item = wxglade_tmp_menu.Append(wx.ID_ANY, "Quit", "")
        self.Bind(wx.EVT_MENU, self.onQuit, id=item.GetId())
        self.frame_menubar.Append(wxglade_tmp_menu, "File")
        wxglade_tmp_menu = wx.Menu()
        item = wxglade_tmp_menu.Append(wx.ID_ANY, "Clear GUI", "")
        self.Bind(wx.EVT_MENU, self.onClearGUI, id=item.GetId())
        item = wxglade_tmp_menu.Append(wx.ID_ANY, "Delete Data", "")
        self.Bind(wx.EVT_MENU, self.onDeleteData, id=item.GetId())
        
        """item = wxglade_tmp_menu.Append(wx.ID_ANY, "Network pcap files", "")
        self.Bind(wx.EVT_MENU, self.onSelNetworkPcapFiles, id=item.GetId())"""

        self.frame_menubar.Append(wxglade_tmp_menu, "Tools")
        self.SetMenuBar(self.frame_menubar)
        # Menu Bar end

        #splitter window
        self.window_1 = wx.SplitterWindow(self, wx.ID_ANY)

        #left panel
        self.windowLeftPanel = wx.Panel(self.window_1, wx.ID_ANY)
        self.tree_ctrl_1 = wx.TreeCtrl(self.windowLeftPanel, wx.ID_ANY, style=wx.TR_HAS_BUTTONS | wx.TR_MULTIPLE)
        
        #right panel
        self.windowRightPanel = wx.Panel(self.window_1, wx.ID_ANY)
        self.searchBtn = wx.Button(self.windowRightPanel, id=wx.ID_ANY, label="Search", pos=wx.DefaultPosition, size=(100,-1), style=0, validator=wx.DefaultValidator)
       
        self.auiNotebook = wx.aui.AuiNotebook(self.windowRightPanel)
        self.paneltest = wx.Panel(self.auiNotebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        
    
        #bind events
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.onItemSel, self.tree_ctrl_1)
        self.Bind(wx.EVT_BUTTON, self.onSearchBtn, self.searchBtn)
        self.Bind(wx.aui.EVT_AUINOTEBOOK_PAGE_CLOSE, self.onAuiClose, self.auiNotebook)

        #properties
        self.SetTitle("Forensic Pi")
        self.tree_ctrl_1.SetBackgroundColour(wx.Colour(240, 240, 240))
        self.windowLeftPanel.SetMinSize((180, -1))
        self.windowRightPanel.SetMinSize((980, -1))
        self.window_1.SetMinimumPaneSize(20)

        #layout
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        
        #left panel sizer
        panel1Sizer = wx.BoxSizer(wx.HORIZONTAL)
        panel1Sizer.Add(self.tree_ctrl_1, 1, wx.EXPAND, 0)
        self.windowLeftPanel.SetSizer(panel1Sizer)
        
        #right panel sizer
        self.panel2Sizer = wx.BoxSizer(wx.VERTICAL)
        self.panel2Sizer.Add(self.searchBtn, 0, wx.ALIGN_RIGHT , 0)
        self.panel2Sizer.Add(self.auiNotebook, 1, wx.EXPAND, 0)
        self.windowRightPanel.SetSizer(self.panel2Sizer)
        
        #splitter
        self.window_1.SplitVertically(self.windowLeftPanel, self.windowRightPanel)
        mainSizer.Add(self.window_1, 1, wx.EXPAND, 0)
       
        self.SetSizer(mainSizer)
        self.Layout()

    def recreateTree(self, caseDbFile):
        self.tree_ctrl_1.Freeze()
        self.tree_ctrl_1.DeleteAllItems()
        global caseName
        for x in caseDetails:
            caseName = str(x[2]) + "_" + x[3]

        root = self.tree_ctrl_1.AddRoot(caseName)                                   #adds the name of case as root item in treectrl
        self.tree_ctrl_1.AppendItem(root, "Summary")
       
        conn = connectdb.create_connection(caseDbFile)                              #connect to case database
        evidenceInfo = connectdb.select_evidence_details(conn)                      #get evidenceName, EvidenceDbPath EvidenceDatetime and Md5 from case database
                                                                                    #EvidenceDbPath = path to tsk database generated when onAddEvidence is called
        self.tree_ctrl_1.AppendItem(root, "Bookmarks")
        self.tree_ctrl_1.AppendItem(root, "File")
        self.tree_ctrl_1.AppendItem(root, "Images")
        self.tree_ctrl_1.AppendItem(root, "Sessions")
        self.tree_ctrl_1.AppendItem(root, "DNS")
        self.tree_ctrl_1.AppendItem(root, "Credentials")

        self.tree_ctrl_1.ExpandAll()
        self.tree_ctrl_1.Thaw()

    #menu functions
    def onNewCase(self, event):  
        dialog = NewCaseDialog.newCase(None)
        dialog.Center()
        dialog.ShowModal()
        dbPath = dialog.getCaseDb()
        
        global caseDetails
        try:
            conn = connectdb.create_connection(dbPath)                      #connects to new case database
            caseDetails = connectdb.select_case_details(conn)               #get InvestigatorName, CaseNum, CaseName, CaseFolder, CaseDb, CaseDesc, Datatime from case database
            self.recreateTree(dbPath)                                       #creates treectrl
        except:
            pass 
        
        dialog.Destroy()
        

    def onOpenCase(self, event):  
        openFileDialog = wx.FileDialog(self, "Open", "", "","*.db",         #creates a filedialog that only allow user to select .db files
                                       wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) 
 
        openFileDialog.ShowModal()                      
        global caseDbPath
        caseDbPath  = openFileDialog.GetPath()                              #get path selected in filedialog
        
        global caseDetails, evidenceDetails
        try:
            conn = connectdb.create_connection(caseDbPath)                  #try to connect to case database and get case and evidence details
            caseDetails = connectdb.select_case_details(conn)
            evidenceDetails = connectdb.select_evidence_details(conn)       #get EvidenceName, EvidenceDbPath, EvidenceDatatime and Md5 from case database
            self.addAuiTab("Summary", evidenceDetails)                      #opens summary page 
            openTabs.append("Summary")                          
            self.recreateTree(caseDbPath)
        except:
            pass                                                            #ignore if try: fails
        openFileDialog.Destroy()

   
    def onAddEvidence(self, event):
        try:
            caseDetails                                                     
        except NameError:                                                   #if caseDetails not defined
            print("Case not opened")                                        
        else:                                                               #if caseDetails is defined
            openFileDialog = wx.FileDialog(self, "Open", "", "","*.pcap",     #creates a filedialog that only allow user to select .dd files 
                                        wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
    
            openFileDialog.ShowModal()                         
            global caseDir, caseDbPath                                   
            evidencePath = openFileDialog.GetPath()                         #get path of selected dd file
            fileName = os.path.basename(evidencePath)
            
        
            for x in caseDetails:
                caseDir = x[4]                                              #get case directory from caseDetails
                caseDbPath = x[5]                                           #get case database path from caseDetails

            evidenceDbDir = Path(caseDir+"/Evidence_Database")
            if evidenceDbDir.is_dir() == False:                             #check if directory exist
                os.mkdir(str(evidenceDbDir))                                #create directory if it does not exist
            if fileName != "":
                self._dialog = wx.ProgressDialog("Adding evidence", "Creating database for '{s}'".format(s=fileName), 100) 
                LoadingDialog(self._dialog)                                 #starts the loading dialog
                load_db = subprocess.call(["tsk_loaddb", "-d",  "{caseDir}/Evidence_Database/{fileName}.db".format(caseDir=caseDir, fileName=fileName), evidencePath]) #use tsk_loaddb to generate tsk database
                LoadingDialog.endLoadingDialog(self)                        #ends the loading dialog

                if load_db == 0:                                            #if no error
                    conn = connectdb.create_connection(caseDbPath)
                    with conn:
                        evidenceDbPath = str(evidenceDbDir)+"/"+fileName+".db"
                        #hash = "md5sum {evidencePath} | awk '{col}".format(evidencePath=evidenceDbPath, col="{print $1}")
                        #evidenceMd5 = subprocess.Popen([hash], stdout=subprocess.PIPE).communicate()[0]
                        evidenceMd5 = "None"
                        insertEvidence = (1, fileName, evidenceDbPath, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), evidenceMd5)
                        connectdb.insertEvidenceDetails(conn, insertEvidence)   #insert to EvidenceInfo in case database
                    
                    evidenceConn = connectdb.create_connection(caseDir+"/Evidence_Database/"+fileName+".db")    #connect to tsk database
                    evidencePart = connectdb.select_image_partitions(evidenceConn)                              #get image partitions from tsk database
                    
                    if Path(caseDir+"/Evidence_Database/Deleted_Files.db").is_file() == False:                  #check if Deleted_Files.db exist
                        createDeletedFilesDb = connectdb.create_connection(caseDir+"/Evidence_Database/Deleted_Files.db") 
                        deteledFilesTable = "CREATE TABLE 'DeletedFiles' ('fileType' TEXT, 'status' TEXT, 'inode' TEXT, 'filePath' TEXT, 'ctime' TEXT, 'crtime' TEXT, 'atime' TEXT, 'mtime' TEXT, 'size' INTEGER, 'uid' INTEGER, 'gid' INTEGER, 'image' TEXT);"
                        connectdb.createTable(createDeletedFilesDb, deteledFilesTable)                          #creates if it does not exist
                    
                    else:
                        createDeletedFilesDb = connectdb.create_connection(caseDir+"/Evidence_Database/Deleted_Files.db")   #connects to Deleted_Files.db
                        
                    for x in evidencePart:
                        if x[2] != "Unallocated":
                            subprocess.Popen(["tsk_recover", "-e", "-o", str(x[0]), evidencePath, caseDir+"/Extracted/"+fileName]) #recover files from all partitions that re not unallocated
                            
                            listAllDeletedFiles = "fls -rFdl -o {offset} {image}".format(offset=str(x[0]), image=evidencePath)
                            process = subprocess.Popen(listAllDeletedFiles, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) #list all deleted files

                            stdout,stderr = process.communicate()
                            output = stdout.decode()
                            chk = re.sub(r'[ ]\*[ ]', '\t*\t', output)          #change all ' ' in the second and third column of fls output to to '\t'
                            chk = re.sub(r'\n', '\t', chk)                      #change all '\n' to '\t'
                            chk = chk.split('\t')                               #splits all values between \t into a list 
                            itemList = []
                            k=0
                            for i in range(k,len(chk)-1,11):
                                k=i
                                itemList.append(chk[k:k+11])                    #appends every 11 items into a list

                            with createDeletedFilesDb:
                                for list in itemList:
                                    insertDeletedFiles = (list[0], list[1], list[2], list[3], list[4], list[5], list[6], list[7], list[8], list[9], list[10], fileName)
                                    connectdb.insertDeletedFiles(createDeletedFilesDb, insertDeletedFiles)  #inserts all deleted files info into Deleted_Files.db
                    wx.MessageBox("Extracting '{file}' in the background.".format(file=fileName))

                    global evidenceDetails
                    evidenceDetails = connectdb.select_evidence_details(conn)

                    self.auiNotebook.DeletePage(0)
                    self.auiNotebook.RemovePage(0)
                    self.addAuiTab("Summary", evidenceDetails)                  
                    self.recreateTree(caseDbPath)

            openFileDialog.Destroy()

    def onQuit(self, event):  
        self.Close()
        self.Destroy()

    def onClearGUI(self, event):  
        print("Event handler 'onClearGUI' not implemented!")
        event.Skip()

    def onDeleteData(self, event):  
        print("Event handler 'onDeleteData' not implemented!")
        event.Skip()

    #end of menu functions

    #aui tab functions
    def checkOpenedTab(self, tabName):                     #check if tab is opened in aui
        openedTab = set(openTabs)
        if tabName not in openedTab:
            openTabs.append(tabName)
            return True
        else:
            return False

    def addAuiTab(self, tabName, evidenceDetails):
        global caseDir
        for x in caseDetails:
            caseDir = x[4]

        if tabName == "Summary":
            self.auiNotebook.AddPage(SummaryTab.TabPanel(self.auiNotebook, caseDetails, evidenceDetails), tabName, False, wx.NullBitmap)

        if tabName == "File":
            self.auiNotebook.AddPage(FileTab.TabPanel(self.auiNotebook, caseDetails, evidenceDetails), tabName, False, wx.NullBitmap)

        if tabName == "Images":
            self.auiNotebook.AddPage(ImagesTab.TabPanel(self.auiNotebook, caseDetails, evidenceDetails), tabName, False, wx.NullBitmap)

        if tabName == "Sessions":
            self.auiNotebook.AddPage(SessionsTab.TabPanel(self.auiNotebook, caseDetails, evidenceDetails), tabName, False, wx.NullBitmap)

        if tabName == "DNS":
            self.auiNotebook.AddPage(DNSTab.TabPanel(self.auiNotebook, caseDetails, evidenceDetails), tabName, False, wx.NullBitmap)

        if tabName == "Credentials":
            self.auiNotebook.AddPage(CredentialsTab.TabPanel(self.auiNotebook, caseDetails, evidenceDetails), tabName, False, wx.NullBitmap)

        if tabName == "Bookmarks":
            self._dialog = wx.ProgressDialog("Loading", "Loading {tabName}".format(tabName=tabName), 100)
            LoadingDialog(self._dialog)
            self.auiNotebook.AddPage(AnalyzedDataTab.TabPanel(self.auiNotebook, tabName, evidenceDetails, caseDir, caseDbPath), tabName, False, wx.NullBitmap)  #calls and open a aui tab from SummaryTab.py
            LoadingDialog.endLoadingDialog(self)

        for x in evidenceDetails:                     
            evidenceDbConn = connectdb.create_connection(x[2])                      #connects to tsk database
            evidenceDbInfo = connectdb.select_image_info(evidenceDbConn)            #get name, size and md5 from tsk database
            evidencePart  = connectdb.select_image_partitions(evidenceDbConn)       #get partition info from tsk database
            count = 0
            for i in evidencePart:
                count += 1
                if tabName == "Vol{count} {desc}: {start}-{end})".format(count=count, desc=str(i[2]), start=str(i[0]), end=str(i[1])):
                    self._dialog = wx.ProgressDialog("Loading", "Loading {tabName}".format(tabName=tabName), 100)
                    LoadingDialog(self._dialog)
                    self.auiNotebook.AddPage(AnalyzedDataTab.TabPanel(self.auiNotebook, tabName, evidenceDetails, caseDir, caseDbPath), tabName, False, wx.NullBitmap)
                    LoadingDialog.endLoadingDialog(self)
                
    def onItemSel(self, event):  
        temp = event.GetItem()          #gets selected item from treectrl
        tabName = self.tree_ctrl_1.GetItemText(temp)    
        print("{name} selected".format(name=tabName))
        
        try:
            caseDetails                 #checks if caseDetails is defined
        except:                         #if not defined
            print("Case not opened")
        else:                           #if defined
            try:                    
                evidenceDetails
            except:
                print("No evidence found")
            else:
                if self.checkOpenedTab(tabName) == True:        #check if selected item is open 
                    self.addAuiTab(tabName, evidenceDetails)    #open aui tab
                else: 
                    print('Tab already open')


    def onAuiClose(self, event):
        temp = event.GetSelection()
        tabName = self.auiNotebook.GetPageText(temp)
        #self.auiNotebook.RemovePage(temp)          #mac
        print("Closing " + tabName)
        openTabs.remove(tabName)                    #remove closed tab from openTabs
    
    def onSearchBtn(self, event):
        try:
            caseDetails
        except:
            print("Case not open")
        else:
            dlg = search.searchDialog(None)         #calls searchDialog() from search.py
            dlg.Center()
            dlg.ShowModal()
            searchItem = dlg.searchItems()          #calls searchItem() to get search and search option

            searchReturn = []
            if searchItem[1] == "Normal Search":
                for x in evidenceDetails:
                    conn = connectdb.create_connection(x[2])                            #connect to tsk database
                    searchResults = connectdb.search_file_name(conn, searchItem[0])     #search in tsk database
                    if searchResults != []:
                        for i in searchResults:
                            i = i + (x[1],)                                             #adds image location to end of result
                            searchReturn.append(i)                                      #append each result

                self._dialog = wx.ProgressDialog("Search", "Searching for {val}".format(val=searchItem[0]), 100)
                LoadingDialog(self._dialog)
                self.auiNotebook.AddPage(searchTab.searchTabPanel(self.auiNotebook, searchReturn, caseDir), "Search ("+searchItem[0]+")", False, wx.NullBitmap) #call and add searchTab aui page
                LoadingDialog.endLoadingDialog(self)
            else:
                print("Regular Expression")

            dlg.Destroy()
        

class LoadingDialog():
    def __init__(self, _dialog):
        self._dialog = _dialog
        self._dialog.Center()
        self._dialog.Pulse()
        self.run()
     
    def run(self):
        count = 0
        while True:
            self._dialog.Update(count)
            if count == 100:
                break
            count += 2
        
    def endLoadingDialog(self):
        self._dialog.Destroy()

class MyApp(wx.App):
    def OnInit(self):
        self.ForensicPi = mainFrame(None)
        self.SetTopWindow(self.ForensicPi)
        self.ForensicPi.Show()
        self.ForensicPi.Center()
        mainMenuDialog = mainmenu.dialog(None)
        mainMenuDialog.Center()
        mainMenuDialog.ShowModal()
        
        return True
    

# end of class MyApp

if __name__ == "__main__":
    forensicPi = MyApp(0)
    forensicPi.MainLoop()

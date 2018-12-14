import wx
import datetime
from datetime import timedelta
from pathlib import Path
import connectdb
import subprocess
import os
import re

class TabPanel(wx.Panel):
    def __init__(self, parent, caseDetails, evidenceDetails):
        # begin wxGlade: MyDialog.__init__
        wx.Panel.__init__(self, parent=parent)
        self.notebook_3 = wx.Notebook(self, wx.ID_ANY)
        self.notebook_3_Hex = wx.Panel(self.notebook_3, wx.ID_ANY)
        #text_ctrl_2 = hex
        self.text_ctrl_2 = wx.TextCtrl(self.notebook_3_Hex, wx.ID_ANY, "", style=wx.TE_MULTILINE | wx.TE_READONLY)

        self.notebook_3_Image = wx.Panel(self.notebook_3, wx.ID_ANY)
        self.bitmap = wx.StaticBitmap(self.notebook_3_Image, wx.ID_ANY)

        self.notebook_3_pane_1 = wx.Panel(self.notebook_3, wx.ID_ANY)
        #text_ctrl_4 & list_ctrl_1 = file metadata
        self.text_ctrl_4 = wx.TextCtrl(self.notebook_3_pane_1, wx.ID_ANY, "", style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.list_ctrl_1 = wx.ListCtrl(self, wx.ID_ANY, style=wx.LC_HRULES | wx.LC_REPORT | wx.LC_VRULES)

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: MyDialog.__set_properties
        self.text_ctrl_2.SetMinSize((920, 284))
        self.list_ctrl_1.AppendColumn("FIlename", format=wx.LIST_FORMAT_LEFT, width=200)
        self.list_ctrl_1.AppendColumn("MD5", format=wx.LIST_FORMAT_LEFT, width=100)
        self.list_ctrl_1.AppendColumn("Size", format=wx.LIST_FORMAT_LEFT, width=100)
        self.list_ctrl_1.AppendColumn("Parent Path", format=wx.LIST_FORMAT_LEFT, width=200)
        self.list_ctrl_1.AppendColumn("Extension", format=wx.LIST_FORMAT_LEFT, width=200)
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyDialog.__do_layout
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_6 = wx.BoxSizer(wx.VERTICAL)
        sizer_3 = wx.BoxSizer(wx.VERTICAL)
        sizer_4 = wx.BoxSizer(wx.VERTICAL)
        sizer_4.Add(self.text_ctrl_2, 0, wx.ALL | wx.EXPAND, 0)
        self.notebook_3_Hex.SetSizer(sizer_4)
        sizer_3.Add(self.bitmap, 0, 0, 0)
        self.notebook_3_Image.SetSizer(sizer_3)
        sizer_6.Add(self.text_ctrl_4, 1, wx.ALL | wx.EXPAND, 0)
        self.notebook_3_pane_1.SetSizer(sizer_6)
        self.notebook_3.AddPage(self.notebook_3_Hex, "Hex")
        self.notebook_3.AddPage(self.notebook_3_Image, "Image")
        self.notebook_3.AddPage(self.notebook_3_pane_1, "File Metadata")
        sizer_2.Add(self.notebook_3, 1, wx.EXPAND, 0)
        sizer_2.Add(self.list_ctrl_1, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_2)
        sizer_2.Fit(self)
        self.Layout()
        # end wxGlade

# end of class MyDialog
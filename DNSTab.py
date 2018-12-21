#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# generated by wxGlade 0.8.3 on Thu Sep  6 00:17:50 2018
#

import wx
import connectdb
import os
import sqlite3
from sqlite3 import Error
from subprocess import Popen, PIPE

# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode
style=wx.BORDER_NONE
# end wxGlade


class TabPanel(wx.Panel):
    def __init__(self, parent, caseDetails, evidenceDetails):
        # begin wxGlade: MyFrame.__init__
        wx.Panel.__init__(self, parent=parent)
        self.dnslist = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_MULTILINE | wx.TE_READONLY)
        

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: MyDialog.__set_properties
        self.dnslist.SetBackgroundColour(wx.Colour(211, 211, 211))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyDialog.__do_layout
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_2.Add(self.dnslist, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_2)
        self.Layout()
        # end wxGlade


# end of class TabPanel

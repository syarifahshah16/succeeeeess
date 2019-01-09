import wx
from wx.lib.wordwrap import wordwrap
import wx.lib.agw.ultimatelistctrl as ULC   

class Frame(wx.Frame):
    def __init__(self, *args, **kw):
        wx.Frame.__init__(self, *args, **kw)

        self.list = ULC.UltimateListCtrl(self, agwStyle=ULC.ULC_REPORT|ULC.ULC_HAS_VARIABLE_ROW_HEIGHT)
        items = ['A', 'b', 'a really really long line that if would be nice if it could word-wrap']
        colWidth = 100
        self.list.InsertColumn(0, "AA", width=colWidth)
        for item in items:
            item = wordwrap(item, colWidth, wx.ClientDC(self))
            self.list.InsertStringItem(0, item)

app = wx.App(False)
frm = Frame(None, title="ULC wordwrap test")
frm.Show()
app.MainLoop()
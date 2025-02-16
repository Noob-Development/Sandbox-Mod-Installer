import wx
import wx.xrc

import gettext
_ = gettext.gettext


ID_DISCORD = 6000
ID_GITHUB = 6001
ID_BY_NOOB_DEVELOPMENT = 6002
ID_CHECKBOX_ITEM = 6003

class UnitSelector (wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__ (self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size(380,620), style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetBackgroundColour(wx.Colour(34, 39, 46))

        self.createMenuBar()

        self.mainVerticalSizer = wx.BoxSizer(wx.VERTICAL)
        self.HorizontalSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.mainVerticalSizer.Add(self.HorizontalSizer, 0, wx.EXPAND, 5)

        self.createLeftToHideText(self.HorizontalSizer)
        self.createLeftToHideNumber(self.HorizontalSizer)

        self.createInstructionText(self.mainVerticalSizer)

        self.createDLCNationsTitle(self.mainVerticalSizer)
        self.createDLCNationsWindow(self.mainVerticalSizer)

        self.createRepeatUnitsTitle(self.mainVerticalSizer)
        self.createRepeatUnitsWindow(self.mainVerticalSizer)

        self.SetSizer(self.mainVerticalSizer)
        self.Layout()
        self.Centre(wx.BOTH)


    def createMenuBar(self):
        self.menuBar = wx.MenuBar(0)
        self.creditMenu = wx.Menu()

        self.addMenuItem(self.creditMenu, ID_DISCORD, _(u"Discord"))
        self.addMenuItem(self.creditMenu, ID_GITHUB, _(u"GitHub"))
        self.creditMenu.AppendSeparator()
        self.addMenuItem(self.creditMenu, ID_BY_NOOB_DEVELOPMENT, _(u"By Noob Development"))

        self.menuBar.Append(self.creditMenu, _(u"Credit"))
        self.SetMenuBar(self.menuBar)

    def addMenuItem(self, menu, id, label):
        menuItem = wx.MenuItem(menu, id, label, wx.EmptyString, wx.ITEM_NORMAL)
        menu.Append(menuItem)

    def createLeftToHideText(self, sizer):
        self.leftToHideText = wx.StaticText(self, wx.ID_ANY, _(u"Units Left to Hide:"), wx.DefaultPosition, wx.DefaultSize, 0)
        self.leftToHideText.Wrap(-1)
        self.leftToHideText.SetFont(wx.Font(18, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial"))
        self.leftToHideText.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_ACTIVEBORDER))
        sizer.Add(self.leftToHideText, 0, wx.ALL, 5)

    def createLeftToHideNumber(self, sizer):
        self.leftToHideNumber = wx.StaticText(self, wx.ID_ANY, _(u"39"), wx.DefaultPosition, wx.DefaultSize, 0)
        self.leftToHideNumber.Wrap(-1)
        self.leftToHideNumber.SetFont(wx.Font(18, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Arial"))
        self.leftToHideNumber.SetForegroundColour(wx.Colour(255, 0, 0))
        sizer.Add(self.leftToHideNumber, 0, wx.ALL, 5)

    def createInstructionText(self, sizer):
        self.instructionText = wx.StaticText(self, wx.ID_ANY, _(u"Wargame only allows 2047 units to be in one faction at a time.\nSince the \"All Units to NATO\" option was selected, some DLC\nnations and/or units must be hidden using this menu."), wx.DefaultPosition, wx.DefaultSize, 0)
        self.instructionText.Wrap(-1)
        self.instructionText.SetForegroundColour(wx.SystemSettings.GetColour( wx.SYS_COLOUR_ACTIVEBORDER))
        sizer.Add(self.instructionText, 0, wx.ALL, 5)

    def createDLCNationsTitle(self, sizer):
        self.DLCNationsTitle = wx.StaticText(self, wx.ID_ANY, _(u"DLC Nations"), wx.DefaultPosition, wx.DefaultSize, 0)
        self.DLCNationsTitle.Wrap(-1)
        self.DLCNationsTitle.SetFont(wx.Font(16, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Arial"))
        self.DLCNationsTitle.SetForegroundColour(wx.SystemSettings.GetColour( wx.SYS_COLOUR_ACTIVEBORDER))
        sizer.Add(self.DLCNationsTitle, 0, wx.ALL, 5)

    def createDLCNationsWindow(self, sizer):
        self.DLCNationsWindow = wx.ScrolledWindow(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL)
        self.DLCNationsWindow.SetScrollRate(5, 5)
        self.DLCNationsWindow.SetBackgroundColour(wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWFRAME))
        self.DLCNationsWindow.SetMinSize(wx.Size(-1,100))
        self.DLCNationsWindow.SetMaxSize(wx.Size(-1,100))
        sizer.Add(self.DLCNationsWindow, 0, wx.ALL|wx.EXPAND, 5)

    def createRepeatUnitsTitle(self, sizer):
        self.repeatUnitsTitle = wx.StaticText(self, wx.ID_ANY, _(u"Repeat Units"), wx.DefaultPosition, wx.DefaultSize, 0)
        self.repeatUnitsTitle.Wrap(-1)
        self.repeatUnitsTitle.SetFont(wx.Font(16, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Arial"))
        self.repeatUnitsTitle.SetForegroundColour(wx.SystemSettings.GetColour( wx.SYS_COLOUR_ACTIVEBORDER))
        sizer.Add(self.repeatUnitsTitle, 0, wx.ALL, 5)

    def createRepeatUnitsWindow(self, sizer):
        self.repeatUnitsWindow = wx.ScrolledWindow(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL)
        self.repeatUnitsWindow.SetScrollRate(5, 5)
        self.repeatUnitsWindow.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOWFRAME))
        self.repeatUnitsWindow.SetMinSize(wx.Size(-1,250))
        self.repeatUnitsWindow.SetMaxSize(wx.Size(-1,250 ))

        y_pos = 5
        for i in range(20):
            option = f"Option {i+1}"
            name = f"repeat_unit_{i+1}"
            checkbox = wx.CheckBox(self.repeatUnitsWindow, label=option, pos=(10, y_pos), name=name)
            checkbox.SetToolTip(wx.ToolTip(f"Description for {option}"))
            y_pos += 20

        scroll_unit = 10
        self.repeatUnitsWindow.SetScrollbars(scroll_unit, scroll_unit, 0, (y_pos) // scroll_unit)

        sizer.Add(self.repeatUnitsWindow, 0, wx.EXPAND |wx.ALL, 5)


if __name__ == '__main__':
    app = wx.App(False)
    frame = UnitSelector(None)
    frame.Show()
    app.MainLoop()

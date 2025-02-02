import wx
import wx.xrc
import gettext
_ = gettext.gettext

import utils

# Can't remember what this is for, so we keep it as I don't wanna try to figure that out ATM
ID_DISCORD = 6000
ID_GITHUB = 6001
ID_BY_NOOB_DEVELOPMENT = 6002
ID_CHECKBOX_ITEM = 6003


class InstallDonePopup(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__ (self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size(505,280), style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetBackgroundColour(wx.Colour(34, 39, 46))

        self.createMenuBar()

        self.mainVerticalSizer = wx.BoxSizer(wx.VERTICAL)
        self.HorizontalSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.createMainTitle(self.mainVerticalSizer)
        self.createInstructionText(self.mainVerticalSizer)
        self.addSpacer(self.mainVerticalSizer, 10)
        self.showInviteCode(self.HorizontalSizer)
        self.mainVerticalSizer.Add(self.HorizontalSizer, 0, wx.ALIGN_CENTER, 5)
        self.addSpacer(self.mainVerticalSizer, 10)
        self.createButton(self.mainVerticalSizer)

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

    def createMainTitle(self, sizer):
        self.mainTitle = wx.StaticText(self, wx.ID_ANY, _(u"Install complete!"), wx.DefaultPosition, wx.DefaultSize, 0)
        self.mainTitle.Wrap(-1)
        self.mainTitle.SetFont( wx.Font(36, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Arial"))
        self.mainTitle.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_ACTIVEBORDER))
        sizer.Add(self.mainTitle, 0, wx.ALIGN_CENTER|wx.ALL, 5)

        self.staticLine = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
        self.staticLine.SetFont( wx.Font(8, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial"))
        sizer.Add(self.staticLine, 0, wx.EXPAND |wx.ALL, 5)

    def createInstructionText(self, sizer):
        self.friendInstructionText = wx.StaticText(self, wx.ID_ANY, _(u"Playing with friends? Remember to have the same config else the game WILL desync!\nYou can get the same config by giving your frinds your \"invite code\", they just need to imput it into the installer and walla!\n"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.friendInstructionText.Wrap(-1)
        self.friendInstructionText.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_ACTIVEBORDER))
        sizer.Add(self.friendInstructionText, 0, wx.ALIGN_CENTER|wx.ALL, 5)

    def showInviteCode(self, sizer):
        self.inviteCode = wx.StaticText(self, wx.ID_ANY, _(u"Your invite code is:"), wx.DefaultPosition, wx.DefaultSize, 0)
        self.inviteCode.Wrap(-1)
        self.inviteCode.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_ACTIVEBORDER))
        sizer.Add(self.inviteCode, 0, wx.ALL, 5)

        self.inviteCodeNumber = wx.StaticText(self, wx.ID_ANY, _(u"10"), wx.DefaultPosition, wx.DefaultSize, 0)
        self.inviteCodeNumber.Wrap(-1)
        self.inviteCodeNumber.SetFont(wx.Font(9, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Arial"))
        sizer.Add(self.inviteCodeNumber, 0, wx.ALL, 5)

    def createButton(self, sizer):
        self.closeButton = wx.Button(self, wx.ID_ANY, _(u"Close"), wx.DefaultPosition, wx.DefaultSize, 0)
        sizer.Add(self.closeButton, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        self.closeButton.Bind(wx.EVT_BUTTON, self.onClose)

    def addSpacer(self, sizer, size):
        sizer.Add((0, size), 0, 0, 5)



    def onClose(self, event):
        self.Close()

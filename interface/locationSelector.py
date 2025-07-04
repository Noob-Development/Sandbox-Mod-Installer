import os.path
import wx
import wx.xrc
import gettext

import utils.modDownloader

_ = gettext.gettext

from interface.mainInterface import MainInterface
from interface.handlers.menuHandler import *


class DirSelector(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition, size=wx.Size(393, 150), style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetBackgroundColour(wx.Colour(34, 39, 46))

        mainVerticalSizer = wx.BoxSizer(wx.VERTICAL)

        self.createMenuBar()
        self.createInstructionText(mainVerticalSizer)
        self.createDirPicker(mainVerticalSizer)
        self.createButton(mainVerticalSizer)

        self.SetSizer(mainVerticalSizer)
        self.Layout()
        self.Centre(wx.BOTH)

    def createMenuBar(self):
        self.menuBar = wx.MenuBar(0)
        self.creditMenu = wx.Menu()

        self.addMenuItem(self.creditMenu, ID_DISCORD, _(u"Discord"))
        self.addMenuItem(self.creditMenu, ID_GITHUB, _(u"GitHub"))
        self.addMenuItem(self.creditMenu, ID_DONATE, _(u"Donate"))
        self.creditMenu.AppendSeparator()
        self.addMenuItem(self.creditMenu, ID_BY_NOOB_DEVELOPMENT, _(u"By Noob Development"))

        self.menuBar.Append(self.creditMenu, _(u"Support us"))
        self.SetMenuBar(self.menuBar)

        self.Bind(wx.EVT_MENU, onMenuItemClick)

    def addMenuItem(self, menu, id, label):
        menuItem = wx.MenuItem(menu, id, label, wx.EmptyString, wx.ITEM_NORMAL)
        menu.Append(menuItem)

    def createInstructionText(self, sizer):
        instructionText = wx.StaticText(self, wx.ID_ANY, _(u"Please select your Wargame Installation folder"), wx.DefaultPosition, wx.DefaultSize, 0)
        instructionText.Wrap(-1)
        instructionText.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_ACTIVEBORDER))
        sizer.Add(instructionText, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

    def createDirPicker(self, sizer):
        self.dirPicker = wx.DirPickerCtrl(self, wx.ID_ANY, wx.EmptyString, _(u"Select your Wargame folder"), wx.DefaultPosition, wx.DefaultSize, wx.DIRP_DEFAULT_STYLE | wx.DIRP_DIR_MUST_EXIST | wx.DIRP_SMALL)
        sizer.Add(self.dirPicker, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

    def createButton(self, sizer):
        self.next = wx.Button(self, wx.ID_ANY, _(u"Next"), wx.DefaultPosition, wx.DefaultSize, 0)
        sizer.Add(self.next, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.next.Bind(wx.EVT_BUTTON, self.openInstaller)

    def openInstaller(self, event):
        import utils.variables  # Ensure you are updating the correct module variable
        utils.variables.installLocation = self.dirPicker.GetPath()
        if utils.variables.installLocation and os.path.isfile(os.path.join(utils.variables.installLocation, "WarGame3.exe")):
            self.Destroy()
            utils.modDownloader.getVersionAndDownload()
            frame = MainInterface(None)
            frame.Show()
        else:
            wx.MessageBox("The selected location does not appear to be your Wargame Directory", "Wrong location", wx.ICON_ERROR)
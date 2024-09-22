from os.path import join
import wx
import wx.xrc
import json
import gettext
_ = gettext.gettext

import utils

ID_DISCORD = 6000
ID_GITHUB = 6001
ID_BY_NOOB_DEVELOPMENT = 6002
ID_CHECKBOX_ITEM = 6003

def loadPatcherJson():
    with open(join(utils.installLocation + '\\SandboxMod', 'patcher_paths.json'), encoding='utf-8') as patcherJson:
        return json.load(patcherJson)


class MainInterface ( wx.Frame ):
    def __init__( self, parent ):
        patcherJson = loadPatcherJson()

        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition, size=wx.Size(900, 415), style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetBackgroundColour(wx.Colour(34, 39, 46))

        self.createMenuBar()
        mainVerticalSizer = wx.BoxSizer(wx.VERTICAL)

        self.createInstructionText(mainVerticalSizer)
        self.createSettingsGrid(patcherJson, mainVerticalSizer)
        self.createInstallButton(mainVerticalSizer)

        self.SetSizer(mainVerticalSizer)
        self.Layout()
        self.Centre(wx.BOTH)

    def createMenuBar(self):
        self.menuBar = wx.MenuBar(0)
        self.settingsMenu = wx.Menu()
        self.creditMenu = wx.Menu()

        self.addMenuItem(self.creditMenu, ID_DISCORD, _(u"Discord"))
        self.addMenuItem(self.creditMenu, ID_GITHUB, _(u"GitHub"))
        self.creditMenu.AppendSeparator()
        self.addMenuItem(self.creditMenu, ID_BY_NOOB_DEVELOPMENT, _(u"By Noob Development"))

        self.addClickableMenuItem(self.settingsMenu, ID_CHECKBOX_ITEM, _(u"Modify whats currently loaded?"))

        self.menuBar.Append(self.settingsMenu, _(u"Settings"))
        self.menuBar.Append(self.creditMenu, _(u"Credit"))
        self.SetMenuBar(self.menuBar)

    def addMenuItem(self, menu, id, label):
        menuItem = wx.MenuItem(menu, id, label, wx.EmptyString, wx.ITEM_NORMAL)
        menu.Append(menuItem)

    def addClickableMenuItem(self, menu, id, label):
        menuItem = wx.MenuItem(menu, id, label, kind=wx.ITEM_CHECK)
        menu.Append(menuItem)

    def createInstructionText(self, sizer):
        instructionText = wx.StaticText(self, wx.ID_ANY, _(u"Select the mods you want applied to the game and then press \"install\"."), wx.DefaultPosition, wx.DefaultSize, 0)
        instructionText.Wrap(-1)
        instructionText.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_ACTIVEBORDER))
        sizer.Add(instructionText, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

    def createSettingsGrid(self, patcher_json, sizer):
        settingsGridSizer = wx.FlexGridSizer(0, 3, 0, 0)
        settingsGridSizer.SetFlexibleDirection(wx.BOTH)
        settingsGridSizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)
        settingsGridSizer.SetMinSize(wx.Size(-1, 300))

        categories = ['Lobby', 'Deck', 'Gameplay']
        for category in categories:
            category_sizer = wx.BoxSizer(wx.VERTICAL)
            self.addCategorytTitle(category_sizer, category)
            self.addCategorySettings(category_sizer, patcher_json, category)
            settingsGridSizer.Add(category_sizer, 0, wx.EXPAND | wx.ALL, 5)

        sizer.Add(settingsGridSizer, 0, wx.ALIGN_CENTER, 5)

    def addCategorytTitle(self, sizer, category):
        title = wx.StaticText(self, wx.ID_ANY, _(category), wx.DefaultPosition, wx.DefaultSize, 0)
        title.Wrap(-1)
        title.SetFont(wx.Font(14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Arial"))
        title.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_ACTIVEBORDER))
        sizer.Add(title, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

    def addCategorySettings(self, sizer, patcher_json, category):
        settingsWindow = wx.ScrolledWindow(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL | wx.VSCROLL)
        settingsWindow.SetScrollRate(5, 5)
        settingsWindow.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOWFRAME))
        settingsWindow.SetMinSize(wx.Size(280, -1))
        settingsWindow.SetMaxSize(wx.Size(-1, 250))

        y_pos = 5
        for option in patcher_json.get(category, {}).keys():
            name = ';'.join([join(category, file) for file in patcher_json[category][option]['paths']])
            checkbox = wx.CheckBox(settingsWindow, label=option, pos=(10, y_pos), name=name)
            checkbox.SetToolTip(wx.ToolTip(patcher_json[category][option]['desc']))
            self.Bind(wx.EVT_CHECKBOX, self.optionCheck, checkbox)
            y_pos += 20

        scroll_unit = 10
        settingsWindow.SetScrollbars(scroll_unit, scroll_unit, 0, (y_pos) // scroll_unit)

        sizer.Add(settingsWindow, 1, wx.ALL | wx.EXPAND, 2)

    def createInstallButton(self, sizer):
        installButtonSizer = wx.BoxSizer(wx.VERTICAL)
        installButton = wx.Button(self, wx.ID_ANY, _(u"Install!"), wx.DefaultPosition, wx.DefaultSize, 0)
        installButtonSizer.Add(installButton, 0, wx.ALL, 5)
        sizer.Add(installButtonSizer, 1, wx.ALIGN_CENTER_HORIZONTAL, 5)
        installButton.Bind(wx.EVT_BUTTON, self.startInstall)


    def startInstall( self, event ):
        if self.GetMenuBar().FindItemById(6003).IsChecked():
            utils.mod_from_backup = False
        self.Destroy()


    def optionCheck(self, event):
        event = event.GetEventObject()

        print(f'{event.GetValue()}')
        print(event.GetName().split(';'))

        names = event.GetName().split(';')
        if event.GetValue():
            utils.patches_to_apply += names
        else:
            for name in names:
                utils.patches_to_apply.remove(name)

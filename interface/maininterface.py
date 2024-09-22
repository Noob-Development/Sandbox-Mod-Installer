import wx
import wx.xrc

from os.path import join, dirname
import json

import utils

import gettext
_ = gettext.gettext

ID_DISCORD = 6000
ID_GITHUB = 6001
ID_BY_NOOB_DEVELOPMENT = 6002

###########################################################################
## Class MainInstaller
###########################################################################

def load_patcher_json():
    with open(join(utils.installLocation + '\\SandboxMod', 'patcher_paths.json'), encoding='utf-8') as patcher_json:
        return json.load(patcher_json)


class MainInterface ( wx.Frame ):

    def __init__( self, parent ):
        patcher_json = load_patcher_json()

        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 900,415 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
        self.SetBackgroundColour( wx.Colour( 34, 39, 46 ) )

        # Menu bar
        self.menuBar = wx.MenuBar(0)
        self.settingsMenu = wx.Menu()
        self.creditMenu = wx.Menu()

        # Credit menu items
        self.creditDiscordItem = wx.MenuItem(self.creditMenu, ID_DISCORD, _(u"Discord"), wx.EmptyString, wx.ITEM_NORMAL)
        self.creditMenu.Append(self.creditDiscordItem)

        self.creditGithubItem = wx.MenuItem(self.creditMenu, ID_GITHUB, _(u"GitHub"), wx.EmptyString, wx.ITEM_NORMAL)
        self.creditMenu.Append(self.creditGithubItem)

        self.creditMenu.AppendSeparator()

        self.addClickableMenuItem(self.settingsMenu, ID_CHECKBOX_ITEM, _(u"Modify whats currently loaded?"))

        self.menuBar.Append(self.settingsMenu, _(u"Settings"))
        self.menuBar.Append(self.creditMenu, _(u"Credit"))

        self.SetMenuBar(self.menuBar)

        mainVerticalSizer = wx.BoxSizer(wx.VERTICAL)

    def addClickableMenuItem(self, menu, id, label):
        menuItem = wx.MenuItem(menu, id, label, kind=wx.ITEM_CHECK)
        menu.Append(menuItem)

        self.m_staticText2.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_ACTIVEBORDER ) )

        mainVerticalSizer.Add(self.m_staticText2, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        settingsGridSizer = wx.FlexGridSizer(0, 3, 0, 0)
        settingsGridSizer.SetFlexibleDirection(wx.BOTH)
        settingsGridSizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        settingsGridSizer.SetMinSize(wx.Size(-1, 300))
        self.lobbyTitle = wx.StaticText(self, wx.ID_ANY, _(u"Lobby"), wx.DefaultPosition, wx.DefaultSize, 0)
        self.lobbyTitle.Wrap(-1)

        self.lobbyTitle.SetFont(wx.Font(14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Arial"))
        self.lobbyTitle.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_ACTIVEBORDER))

        settingsGridSizer.Add(self.lobbyTitle, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.deckTitle = wx.StaticText(self, wx.ID_ANY, _(u"Deck"), wx.DefaultPosition, wx.DefaultSize, 0)
        self.deckTitle.Wrap(-1)

        self.deckTitle.SetFont(wx.Font(14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Arial"))
        self.deckTitle.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_ACTIVEBORDER))

        settingsGridSizer.Add(self.deckTitle, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.gameplayTitle = wx.StaticText(self, wx.ID_ANY, _(u"Gameplay"), wx.DefaultPosition, wx.DefaultSize, 0)
        self.gameplayTitle.Wrap(-1)

        self.gameplayTitle.SetFont(wx.Font(14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Arial"))
        self.gameplayTitle.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_ACTIVEBORDER))

        settingsGridSizer.Add(self.gameplayTitle, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.lobbySettings = wx.ScrolledWindow(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL | wx.VSCROLL)
        self.lobbySettings.SetScrollRate(5, 5)
        self.lobbySettings.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOWFRAME))
        self.lobbySettings.SetMinSize(wx.Size(280, -1))
        self.lobbySettings.SetMaxSize(wx.Size(-1, 250))

        settingsGridSizer.Add(self.lobbySettings, 1, wx.ALL | wx.EXPAND, 5)

        self.deckSettings = wx.ScrolledWindow(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL | wx.VSCROLL)
        self.deckSettings.SetScrollRate(5, 5)
        self.deckSettings.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOWFRAME))
        self.deckSettings.SetMinSize(wx.Size(280, -1))
        self.deckSettings.SetMaxSize(wx.Size(-1, 250))

        settingsGridSizer.Add(self.deckSettings, 1, wx.ALL | wx.EXPAND, 5)

        self.gameplaySettings = wx.ScrolledWindow(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL | wx.NO_FULL_REPAINT_ON_RESIZE | wx.VSCROLL)
        self.gameplaySettings.SetScrollRate(10, 10)
        self.gameplaySettings.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOWFRAME))
        self.gameplaySettings.SetMinSize(wx.Size(280, -1))
        self.gameplaySettings.SetMaxSize(wx.Size(-1, 250))

        settingsGridSizer.Add(self.gameplaySettings, 1, wx.ALL | wx.EXPAND, 5)

        self.Bind(wx.EVT_CHECKBOX, self.optionCheck)
        for category in patcher_json.keys():
            if category == 'Lobby':
                window = self.lobbySettings
            if category == 'Deck':
                window = self.deckSettings
            if category == 'Gameplay':
                window = self.gameplaySettings

            y_pos = 5
            for option in patcher_json[category].keys():
                name = ';'.join([join(category, file) for file in patcher_json[category][option]['paths']])
                wx.CheckBox(window, label=option, pos=(10, y_pos), name=name).SetToolTip(
                    wx.ToolTip(patcher_json[category][option]['desc']))
                y_pos += 20
        scroll_unit = 10
        window.SetScrollbars(scroll_unit, scroll_unit, 0, (y_pos) // scroll_unit)


        mainVerticalSizer.Add(settingsGridSizer, 0, wx.ALIGN_CENTER, 5)

        installButtonSizer = wx.BoxSizer(wx.VERTICAL)

        self.install = wx.Button( self, wx.ID_ANY, _(u"Install!"), wx.DefaultPosition, wx.DefaultSize, 0 )
        installButtonSizer.Add(self.install, 0, wx.ALL, 5)


        mainVerticalSizer.Add(installButtonSizer, 1, wx.ALIGN_CENTER_HORIZONTAL, 5)


        self.SetSizer(mainVerticalSizer)
        self.Layout()

        self.Centre( wx.BOTH )

        # Connect Events
        self.install.Bind( wx.EVT_BUTTON, self.startInstall )

    def __del__( self ):
        pass


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


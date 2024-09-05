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

        self.m_menubar2 = wx.MenuBar( 0 )
        self.credit = wx.Menu()
        self.discord = wx.MenuItem( self.credit, ID_DISCORD, _(u"Discord"), wx.EmptyString, wx.ITEM_NORMAL )
        self.credit.Append( self.discord )

        self.github = wx.MenuItem( self.credit, ID_GITHUB, _(u"GitHub"), wx.EmptyString, wx.ITEM_NORMAL )
        self.credit.Append( self.github )

        self.credit.AppendSeparator()

        self.byNoobDevelopment = wx.MenuItem( self.credit, ID_BY_NOOB_DEVELOPMENT, _(u"By Noob Development"), wx.EmptyString, wx.ITEM_NORMAL )
        self.credit.Append( self.byNoobDevelopment )

        self.m_menubar2.Append( self.credit, _(u"Credit") )

        self.SetMenuBar( self.m_menubar2 )

        bSizer2 = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, _(u"Select the mods you want applyed to the game and then press \"install\"."), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText2.Wrap( -1 )

        self.m_staticText2.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_ACTIVEBORDER ) )

        bSizer2.Add( self.m_staticText2, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

        fgSizer1 = wx.FlexGridSizer( 0, 3, 0, 0 )
        fgSizer1.SetFlexibleDirection( wx.BOTH )
        fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        fgSizer1.SetMinSize( wx.Size( -1,300 ) )
        self.m_staticText41 = wx.StaticText( self, wx.ID_ANY, _(u"Lobby"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText41.Wrap( -1 )

        self.m_staticText41.SetFont( wx.Font( 14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Arial" ) )
        self.m_staticText41.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_ACTIVEBORDER ) )

        fgSizer1.Add( self.m_staticText41, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

        self.m_staticText42 = wx.StaticText( self, wx.ID_ANY, _(u"Deck"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText42.Wrap( -1 )

        self.m_staticText42.SetFont( wx.Font( 14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Arial" ) )
        self.m_staticText42.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_ACTIVEBORDER ) )

        fgSizer1.Add( self.m_staticText42, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

        self.m_staticText43 = wx.StaticText( self, wx.ID_ANY, _(u"Gameplay"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText43.Wrap( -1 )

        self.m_staticText43.SetFont( wx.Font( 14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Arial" ) )
        self.m_staticText43.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_ACTIVEBORDER ) )

        fgSizer1.Add( self.m_staticText43, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

        self.lobbySel = wx.ScrolledWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL )
        self.lobbySel.SetScrollRate( 5, 5 )
        self.lobbySel.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWFRAME ) )
        self.lobbySel.SetMinSize( wx.Size( 280,-1 ) )
        self.lobbySel.SetMaxSize( wx.Size( -1,250 ) )

        fgSizer1.Add( self.lobbySel, 1, wx.ALL|wx.EXPAND, 5 )

        self.deckSel = wx.ScrolledWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL )
        self.deckSel.SetScrollRate( 5, 5 )
        self.deckSel.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWFRAME ) )
        self.deckSel.SetMinSize( wx.Size( 280,-1 ) )
        self.deckSel.SetMaxSize( wx.Size( -1,250 ) )

        fgSizer1.Add( self.deckSel, 1, wx.ALL|wx.EXPAND, 5 )

        self.gameplaySel = wx.ScrolledWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.NO_FULL_REPAINT_ON_RESIZE|wx.VSCROLL )
        self.gameplaySel.SetScrollRate( 10, 10 )
        self.gameplaySel.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWFRAME ) )
        self.gameplaySel.SetMinSize( wx.Size( 280,-1 ) )
        self.gameplaySel.SetMaxSize( wx.Size( -1,250 ) )


        self.Bind(wx.EVT_CHECKBOX, self.optionCheck)
        for category in patcher_json.keys():
            if category == 'Lobby':
                window = self.lobbySel
            if category == 'Deck':
                window = self.deckSel
            if category == 'Gameplay':
                window = self.gameplaySel

            y_pos = 5
            for option in patcher_json[category].keys():
                name = ';'.join([join(category, file) for file in patcher_json[category][option]['paths']])
                wx.CheckBox(window, label=option, pos=(10, y_pos), name=name).SetToolTip(
                    wx.ToolTip(patcher_json[category][option]['desc']))
                y_pos += 20
        scroll_unit = 10
        window.SetScrollbars(scroll_unit, scroll_unit, 0, (y_pos) // scroll_unit)


        fgSizer1.Add( self.gameplaySel, 1, wx.ALL|wx.EXPAND, 5 )


        bSizer2.Add( fgSizer1, 0, wx.ALIGN_CENTER, 5 )

        bSizer6 = wx.BoxSizer( wx.VERTICAL )

        self.install = wx.Button( self, wx.ID_ANY, _(u"Install!"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer6.Add( self.install, 0, wx.ALL, 5 )


        bSizer2.Add( bSizer6, 1, wx.ALIGN_CENTER_HORIZONTAL, 5 )


        self.SetSizer( bSizer2 )
        self.Layout()

        self.Centre( wx.BOTH )

        # Connect Events
        self.install.Bind( wx.EVT_BUTTON, self.startInstall )

    def __del__( self ):
        pass


    def startInstall( self, event ):
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


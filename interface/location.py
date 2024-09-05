import os.path

import wx
import wx.xrc

from interface.maininterface import MainInterface

import utils

import gettext
_ = gettext.gettext

ID_DISCORD = 6000
ID_GITHUB = 6001
ID_BY_NOOB_DEVELOPMENT = 6002

###########################################################################
## Class DirSelector
###########################################################################

class DirSelector ( wx.Frame ):

    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 393,150 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
        self.SetBackgroundColour( wx.Colour( 34, 39, 46 ) )

        bSizer2 = wx.BoxSizer( wx.VERTICAL )

        self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, _(u"Please select your Wargame Installation folder"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText1.Wrap( -1 )

        self.m_staticText1.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_ACTIVEBORDER ) )

        bSizer2.Add( self.m_staticText1, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

        self.m_dirPicker1 = wx.DirPickerCtrl( self, wx.ID_ANY, wx.EmptyString, _(u"Select you wargame folder"), wx.DefaultPosition, wx.DefaultSize, wx.DIRP_DEFAULT_STYLE|wx.DIRP_DIR_MUST_EXIST|wx.DIRP_SMALL )
        bSizer2.Add( self.m_dirPicker1, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

        self.next = wx.Button( self, wx.ID_ANY, _(u"Next"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer2.Add( self.next, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )


        self.SetSizer( bSizer2 )
        self.Layout()
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


        self.Centre( wx.BOTH )

        # Connect Events
        self.next.Bind( wx.EVT_BUTTON, self.openInstaller )

    def __del__( self ):
        pass

    def openInstaller( self, event):
        utils.installLocation = self.m_dirPicker1.GetPath()
        print(utils.installLocation)
        if utils.installLocation:
            file_path = os.path.join(utils.installLocation, "WarGame3.exe")
            if os.path.isfile(file_path):
                self.Destroy()
                frame = MainInterface(None)
                print(f"Valid location: {utils.installLocation}")
                utils.get_version_and_download()
                frame.Show()
            else:
                wx.MessageBox(f"The selected location does not appear to be you Wargame Directory", "Wrong location", wx.ICON_ERROR)



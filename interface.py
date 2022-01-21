###########################################################################
## Python code generated with wxFormBuilder (version 3.10.1-0-g8feb16b3)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.adv

###########################################################################
## Class MyFrame1
###########################################################################

class MyFrame1 ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Sandbox Mod Components", pos = wx.DefaultPosition, size = wx.Size( 465,564 ), style = wx.CAPTION|wx.CLOSE_BOX|wx.ICONIZE|wx.MINIMIZE|wx.MINIMIZE_BOX|wx.SYSTEM_MENU|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		self.SetBackgroundColour( wx.Colour( 34, 39, 46 ) )

		bSizer1 = wx.BoxSizer( wx.VERTICAL )

		self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"Select \"Modify what is currently loaded\" if applying Sandbox on top of another mod", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )

		self.m_staticText1.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNSHADOW ) )

		bSizer1.Add( self.m_staticText1, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

		fgSizer1 = wx.FlexGridSizer( 0, 2, 0, 20 )
		fgSizer1.SetFlexibleDirection( wx.BOTH )
		fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		fgSizer1.SetMinSize( wx.Size( 1,1 ) )
		self.m_radioBtn2 = wx.RadioButton( self, wx.ID_ANY, u"Modify from backup", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_radioBtn2.SetValue( True )
		self.m_radioBtn2.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNSHADOW ) )

		fgSizer1.Add( self.m_radioBtn2, 0, wx.ALL, 5 )

		self.m_radioBtn1 = wx.RadioButton( self, wx.ID_ANY, u"Modify what is currently loaded", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_radioBtn1.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNSHADOW ) )

		fgSizer1.Add( self.m_radioBtn1, 0, wx.ALL, 5 )


		bSizer1.Add( fgSizer1, 1, wx.ALIGN_CENTER, 5 )

		bSizer4 = wx.BoxSizer( wx.VERTICAL )

		self.install = wx.Button( self, wx.ID_ANY, u"Install!", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer4.Add( self.install, 0, wx.ALIGN_CENTER_HORIZONTAL, 5 )


		bSizer1.Add( bSizer4, 1, wx.EXPAND, 5 )

		self.m_scrolledWindow1 = wx.ScrolledWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL )
		self.m_scrolledWindow1.SetScrollRate( 5, 5 )
		self.m_scrolledWindow1.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWFRAME ) )
		self.m_scrolledWindow1.SetMinSize( wx.Size( -1,420 ) )
		self.m_scrolledWindow1.SetMaxSize( wx.Size( -1,420 ) )

		bSizer1.Add( self.m_scrolledWindow1, 1, wx.EXPAND, 2 )

		self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, u"Created and maintained by Noob Development", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )

		self.m_staticText2.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNSHADOW ) )

		bSizer1.Add( self.m_staticText2, 0, wx.ALIGN_CENTER|wx.ALL, 2 )

		fgSizer2 = wx.FlexGridSizer( 0, 2, 0, 15 )
		fgSizer2.SetFlexibleDirection( wx.BOTH )
		fgSizer2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_hyperlink1 = wx.adv.HyperlinkCtrl( self, wx.ID_ANY, u"Discord", u"https://discord.gg/kqvneca5Dr", wx.DefaultPosition, wx.DefaultSize, wx.adv.HL_DEFAULT_STYLE )
		fgSizer2.Add( self.m_hyperlink1, 0, wx.ALIGN_CENTER|wx.ALL, 0 )

		self.m_hyperlink2 = wx.adv.HyperlinkCtrl( self, wx.ID_ANY, u"GitHub", u"https://github.com/Noob-Development", wx.DefaultPosition, wx.DefaultSize, wx.adv.HL_DEFAULT_STYLE )
		fgSizer2.Add( self.m_hyperlink2, 0, wx.ALIGN_CENTER|wx.ALL, 0 )


		bSizer1.Add( fgSizer2, 1, wx.ALIGN_CENTER, 0 )


		self.SetSizer( bSizer1 )
		self.Layout()

		self.Centre( wx.BOTH )

	def __del__( self ):
		pass

if __name__ == '__main__':
	pass
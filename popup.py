import wx
import wx.xrc
import wx.adv

###########################################################################
## Class Popup
###########################################################################

class Popup ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Mod Version Selector", pos = wx.DefaultPosition, size = wx.Size( 561,137 ), style = wx.CAPTION|wx.CLOSE_BOX|wx.MINIMIZE|wx.MINIMIZE_BOX|wx.SYSTEM_MENU|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		self.SetBackgroundColour( wx.Colour( 34, 36, 49 ) )

		bSizer10 = wx.BoxSizer( wx.VERTICAL )

		fgSizer13 = wx.FlexGridSizer( 0, 3, 0, 10 )
		fgSizer13.SetFlexibleDirection( wx.BOTH )
		fgSizer13.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		fgSizer13.SetMinSize( wx.Size( 1,1 ) )
		self.m_radioBtn5 = wx.RadioButton( self, wx.ID_ANY, u"Vanilla Sandbox Mod", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_radioBtn5.SetValue( True )
		self.m_radioBtn5.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNSHADOW ) )

		fgSizer13.Add( self.m_radioBtn5, 0, wx.ALL, 5 )

		self.m_radioBtn6 = wx.RadioButton( self, wx.ID_ANY, u"Ontop of Annihilation Mod", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_radioBtn6.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNSHADOW ) )

		fgSizer13.Add( self.m_radioBtn6, 0, wx.ALL, 5 )

		self.m_radioBtn7 = wx.RadioButton( self, wx.ID_ANY, u"Ontop of Ash and Shadows", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_radioBtn7.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNSHADOW ) )

		fgSizer13.Add( self.m_radioBtn7, 0, wx.ALL, 5 )


		bSizer10.Add( fgSizer13, 0, wx.ALIGN_CENTER, 5 )

		self.m_button7 = wx.Button( self, wx.ID_ANY, u"Continue", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer10.Add( self.m_button7, 0, wx.ALIGN_CENTER|wx.ALL, 10 )

		self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, u"Created and maintained by Noob Development", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )

		self.m_staticText2.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNSHADOW ) )

		bSizer10.Add( self.m_staticText2, 0, wx.ALIGN_CENTER, 5 )

		fgSizer2 = wx.FlexGridSizer( 0, 2, 0, 20 )
		fgSizer2.SetFlexibleDirection( wx.BOTH )
		fgSizer2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_hyperlink1 = wx.adv.HyperlinkCtrl( self, wx.ID_ANY, u"Discord", u"https://discord.gg/kqvneca5Dr", wx.DefaultPosition, wx.DefaultSize, wx.adv.HL_DEFAULT_STYLE )
		fgSizer2.Add( self.m_hyperlink1, 0, wx.ALL, 0 )

		self.m_hyperlink2 = wx.adv.HyperlinkCtrl( self, wx.ID_ANY, u"GitHub", u"https://github.com/Noob-Development/", wx.DefaultPosition, wx.DefaultSize, wx.adv.HL_DEFAULT_STYLE )
		fgSizer2.Add( self.m_hyperlink2, 0, wx.ALL, 0 )


		bSizer10.Add( fgSizer2, 1, wx.ALIGN_CENTER, 5 )


		self.SetSizer( bSizer10 )
		self.Layout()

		self.Centre( wx.BOTH )

	def __del__( self ):
		pass
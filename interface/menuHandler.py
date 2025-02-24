import webbrowser

ID_DISCORD = 6000
ID_GITHUB = 6001
ID_BY_NOOB_DEVELOPMENT = 6002
ID_DONATE = 6003

def onMenuItemClick(event):
    menu_id = event.GetId()
    if menu_id == ID_DISCORD:
        webbrowser.open("https://discord.gg/kqvneca5Dr")
    elif menu_id == ID_GITHUB:
        webbrowser.open("https://github.com/Noob-Development")
    elif menu_id == ID_DONATE:
        webbrowser.open("https://ko-fi.com/griffeng")
    elif menu_id == ID_BY_NOOB_DEVELOPMENT:
        # Website at some point? :O
        pass

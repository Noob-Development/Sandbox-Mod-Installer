# Sandbox Mod Installer

A Python 3 program to automatically update, configure, patch, and install the Sandbox Mod for the game Wargame: Red Dragon. It uses WxPython for the interface.

## Usage
### **[DOWNLOAD INSTALLER](https://github.com/Noob-Development/Sandbox-Mod-Installer/releases/latest/download/SandboxModInstall.exe "DOWNLOAD INSTALLER")**

Place the executable file from the latest release in your Wargame Red Dragon folder and double-click it to begin.  

**Default Game Locations:**

Steam: `C:\Program Files\Steam\steamapps\common\Wargame Red Dragon`

Epic Games: `C:\Program Files\Epic Games\WargameRedDragon`

#### Using with other mods:
1. Install mod of your choice
2. On the install screen go to the settings menu and select the 'Modify what is currently loaded' and then install the mod as normal.
3. To uninstall both mods, uninstall the Sandbox Mod first (instructions below), then uninstall the other mod following their provided instructions

#### Issues:
90% of the time, if there is any error that pops up, running the installer again will make it work perfectly. If that does not work and it is a matter of permissions, try Running as Administrator. If all fails, join the [Sandbox Mod Discord](https://discord.gg/kqvneca5Dr "Sandbox Mod Discord") and post the contents of `SandboxInstallOutput.txt` in the #help channel.

#### Uninstalling:
To uninstall the mod you go into steam or epic games and use there verify process.

## Development (For Modders)
The information below is for people wanting to edit the installer for their own use.

#### Prerequisites:
```powershell
pip install -r requirements.txt
```

#### Build:
```powershell
pyinstaller main.py -F --uac-admin -i SandboxLogo.ico
```

#### How it works:
+ Checks game variant
    + Steam base folder = "Wargame Red Dragon"
    + Epic base folder = "WargameRedDragon"
+ Checks if the current mod version is different than online version
+ Displays interface for component selection
+ Creates/moves backup NDF_Win.dat if neccesary 
+ Calls the XML Patcher made by PowerCrystals
    + The XML Patcher edits the NDF_Win.dat file, which holds all game statistics
    + If no components are selected, then the program cancels here
+ Creates an installerConfig for the Wargame Mod Installer
    + The Wargame Mod Installer by Vasto is used to install assets, which the XML Patcher cannot do

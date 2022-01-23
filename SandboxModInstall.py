# === IMPORTS ===
import os
from os.path import join, dirname
import requests
import json
import re
from shutil import copyfile, move, rmtree
import subprocess
from sys import exit

import urllib.request
import zipfile
import wx
import ctypes, sys

from interface import Installer


INSTALLER_VERSION = '1.0.6'
RELEASE_URL = 'https://api.github.com/repos/Noob-Development/Sandbox-Mod-Files/releases/latest'
MOD_FOLDER = 'SandboxMod'
PATCHES_LOG = 'patch_list.txt'
PATCHER_JSON = 'patcher_paths.json'
INSTALL_JSON = 'install_locations.json'
PRESANDBOX_SUFFIX = '_pre-sandbox'
ZIP_NAME = 'master.zip'
DEVMODE = True

patches_to_apply = []
game_variant = 'Steam'
output_file = open('SandboxInstallOutput.txt', 'w+', encoding='utf-8')
mod_from_backup = True #Whether to use the patcher on the backup or on the currently installed NDF_Win.dat
install_cancelled = True #Should we stop after component selection


# === HELPERS ===
def log_output(text):
    """
    Prints to console and to log file
    """
    print(text)
    output_file.write(str(text)+'\n')

def write_config(config_file, new_file):
    contents = config_file.read()
    splits = contents.split('%')
    for i in range(len(splits)):
        if i % 2:
            try:
                splits[i] = config_replacements[splits[i]]
            except KeyError:
                log_output(f'Key error with {splits[i]}')
    new_file.write(''.join(splits))

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# === GETTERS ===
def get_zip_from_github():
    """
    Downloads zip from latest release, extracts to temporary download folder, renames it, moves it, deletes temps
    """
    log_output('Downloading from GitHub, do not close...')
    dir_path = dirname(os.path.realpath(__file__))
    download_url = json.loads(requests.get(RELEASE_URL, allow_redirects=True).content)['zipball_url']
    urllib.request.urlretrieve(download_url, ZIP_NAME)
    log_output('Extracting Zip')
    with zipfile.ZipFile(ZIP_NAME, 'r') as zip_ref:
        zip_ref.extractall('download')
    log_output('Moving folders')
    download_name = list(os.listdir('download'))[0]
    if os.path.isdir(MOD_FOLDER):
        rmtree(join(dir_path, MOD_FOLDER))
    os.rename(join(dir_path, 'download', download_name), MOD_FOLDER)
    rmtree(join(dir_path, 'download'))
    os.remove(ZIP_NAME)

def get_online_version():
    return json.loads(requests.get(RELEASE_URL, allow_redirects=True).content)['tag_name']

def get_current_version():
    with open(join(MOD_FOLDER, 'version.txt'), encoding='utf-8') as version_file:
        return version_file.read().strip()

def load_patcher_json():
    with open(join(MOD_FOLDER, PATCHER_JSON), encoding='utf-8') as patcher_json:
        return json.load(patcher_json)

def load_configuration():
    with open(join(MOD_FOLDER, INSTALL_JSON), encoding='utf-8') as install_json:
        return json.load(install_json)


# === UI ===
def wx_radio(e):
    """
    WxPython radio button handler, changes game_variant
    """
    event = e.GetEventObject()
    global mod_from_backup
    mod_from_backup = bool(int(event.GetName()))
    log_output(mod_from_backup)

def wx_button(e):
    """
    WxPython radio button handler, changes game_variant
    """
    global install_cancelled
    install_cancelled = False
    e.GetEventObject().GetParent().Close()

def wx_check(e):
    """
    WxPython checkbox handler, adds/removes to patches_to_apply list
    """
    event = e.GetEventObject()
    global patches_to_apply
    names = event.GetName().split(';')
    if event.GetValue():
        patches_to_apply += names
    else:
        for name in names:
            patches_to_apply.remove(name)

def show_interface():
    if is_admin():
        """
        Loads entire interface
        """
        app = wx.App(False)  # Create a new app, don't redirect stdout/stderr to a window.
        #frame = wx.Frame(None, wx.ID_ANY, "Sandbox Mod Components")  # A Frame is a top-level window.
        frame = Installer(None)
        frame.Bind(wx.EVT_RADIOBUTTON, wx_radio)
        frame.Bind(wx.EVT_BUTTON, wx_button)
        patcher_json = load_patcher_json()
        frame.Bind(wx.EVT_CHECKBOX, wx_check)
        #window = wx.ScrolledWindow(frame, pos=(0, 90))
        window = frame.m_scrolledWindow1
        y_pos = 0 #var for keeping track of current y pos
        for category in patcher_json.keys():
            wx.StaticText(window, label=category, pos=(5, y_pos))
            wx.StaticLine(window, 2, pos=(0, y_pos+20), size=(1, 250), style=wx.HORIZONTAL)
            for option in patcher_json[category].keys():
                y_pos+=20
                name = ';'.join([join(category, file) for file in patcher_json[category][option]['paths']])
                wx.CheckBox(window, label=option, pos=(10, y_pos), name=name).SetToolTip(wx.ToolTip(patcher_json[category][option]['desc']))
            y_pos+=30
        scroll_unit = 10
        window.SetScrollbars(scroll_unit, scroll_unit, 0, (y_pos)//scroll_unit)
        frame.Show(True)  # Show the frame.
        app.MainLoop()
    else:
        # Re-run the program with admin rights
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)



# === MAIN ===
if __name__ == '__main__':
    try:
        log_output('Welcome to the Sandbox Mod Installer')
        log_output('Please wait until this console says "Finished!"')
        log_output('======================================================\n\n\n')

        #Get game variant
        dir_path = dirname(os.path.realpath(__file__))
        base_folder = os.path.basename(os.path.normpath(dir_path))
        if base_folder == 'Wargame Red Dragon':
            game_variant = 'Steam'
        elif base_folder == 'WargameRedDragon':
            game_variant = 'Epic'
        elif DEVMODE:
            game_variant = 'Steam'
        else:
            log_output('Please place this in your Wargame Red Dragon folder')
            exit()
        log_output(f'Game variant: {game_variant}')

        #Get most current version
        if not os.path.isdir(join(dir_path, MOD_FOLDER)):
            log_output('Mod not downloaded yet')
            get_zip_from_github()
        else:
            if get_online_version() != get_current_version():
                log_output('Local mod outdated, getting new version')
                log_output(f'Online version: {get_online_version()}, Local version: {get_current_version()}')
                get_zip_from_github()
            else:
                log_output('Local mod is most updated version')

        #Load installation paths
        log_output('Getting install config')
        install_config = load_configuration()

        #Check to see if installing from patch log
        hide_interface = False
        if os.path.isfile(PATCHES_LOG):
            log_output('Patch log detected, installing from log instead of showing interface')
            hide_interface = True
            with open(PATCHES_LOG, 'r', encoding='utf-8') as patches_log:
                patches_to_apply = patches_log.read().splitlines()

        #Show interface
        if not hide_interface:
            log_output('Showing interface')
            show_interface()
            if install_cancelled:
                log_output('Install cancelled')
                exit()

        #Logging patches applied
        if patches_to_apply == []:
            log_output('No patches applied')
            input("Press enter to continue...")
            exit()
        if mod_from_backup:
            patches_log = open(join(MOD_FOLDER, PATCHES_LOG), 'w+', encoding='utf-8')
        else:
            patches_log = open(join(MOD_FOLDER, PATCHES_LOG), 'a+', encoding='utf-8')
        for patch in patches_to_apply:
            patches_log.write(patch)
            patches_log.write('\n')
        patches_log.close()

        #Make original NDF_Win.dat file if needed
        log_output(f'{mod_from_backup=}')
        pc_path = join('Data', 'WARGAME', 'PC')
        ndf_path = join(pc_path, install_config[game_variant]["NDF_Win.dat"], "NDF_Win.dat")
        full_ndf_path = join(dir_path, ndf_path)
        if not os.path.isfile(ndf_path+PRESANDBOX_SUFFIX):
            log_output('Backup does not exist')
            copyfile(full_ndf_path, full_ndf_path+PRESANDBOX_SUFFIX)
        else:
            if mod_from_backup:
                os.remove(full_ndf_path)
                copyfile(full_ndf_path + PRESANDBOX_SUFFIX, full_ndf_path)

        #Call patcher
        log_output('\n')
        log_output('This normaly takes around 5 minutes to complete! The install will say when its done!')
        log_output('\n')

        patcher_call_list = []
        for patch_path in patches_to_apply:
            patcher_call_list += [f'{MOD_FOLDER}\\Script Library\\{patch_path}']
        patcher_call = [f'{MOD_FOLDER}\\Patcher\\WGPatcher.exe', 'apply', full_ndf_path] + patcher_call_list
        log_output(f'Patcher Call: {" ".join(patcher_call)}')
        patcher = subprocess.run([f'{MOD_FOLDER}\\Patcher\\WGPatcher.exe', 'apply', full_ndf_path] + patcher_call_list, cwd=dir_path)
        move(join(dirname(full_ndf_path), 'ndf_win_patched.dat'), ndf_path)

        #Make installerConfig
        log_output('Making asset installerConfig')
        config_replacements = {
            'mod_version': get_current_version(),
            'game_version': install_config[game_variant]["NDF_Win.dat"],
            'NDF_Win.dat-path': install_config[game_variant]["NDF_Win.dat"],
            'ZZ_Win.dat|interface_outgame-path': install_config[game_variant]["ZZ_Win.dat-interface_outgame"],
            'Data.dat-path': install_config[game_variant]["Data.dat"],
            'ZZ_4.dat-path': install_config[game_variant]["ZZ_4.dat"],}
        with open(join(MOD_FOLDER, 'Installer', 'installerConfigTemplate.wmi'), encoding='utf-8') as config_file, open(join(MOD_FOLDER, 'Installer', 'installerConfig.wmi'), 'w+', encoding='utf-8') as new_file:
            write_config(config_file, new_file)
        with open(join(MOD_FOLDER, 'Uninstaller', 'uninstallerConfigTemplate.wmi'), encoding='utf-8') as config_file, open(join(MOD_FOLDER, 'Uninstaller', 'uninstallerConfig.wmi'), 'w+', encoding='utf-8') as new_file:
            write_config(config_file, new_file)

        #Run asset installer
        log_output('Running asset installer')
        asset_installer = subprocess.run('WargameModInstaller.exe', cwd=join(dir_path, MOD_FOLDER, 'Installer'), shell=True)



        log_output('\nFinished!')
        input("Press enter to exit...")

    except Exception as e:
        log_output(f'\nERROR: {e}')
        input("Press enter to exit...")
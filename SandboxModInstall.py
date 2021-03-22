"""

"""


# === IMPORTS ===
import os
from os.path import join, dirname
import requests
import json
from shutil import copyfile, move, rmtree
import subprocess
from sys import exit

import urllib.request
import zipfile
import wx

RELEASE_URL = 'https://api.github.com/repos/TheWRDNoob/Sandbox-Mod-Files/releases/latest'
MOD_FOLDER = 'SandboxMod'
PATCHER_JSON = 'patcher_paths.json'
INSTALL_JSON = 'install_locations.json'
PRESANDBOX_SUFFIX = '_pre-sandbox'
WINDOW_X = 500
WINDOW_Y = 600
ZIP_NAME = 'master.zip'

patches_to_apply = []
game_variant = 'Steam'
output_file = open('SandboxInstallOutput.txt', 'w+')
mod_from_backup = True #Whether to use the patcher on the backup or on the currently installed NDF_Win.dat
install_canceled = True #Should we stop after component selection


# === HELPERS ===
def log_output(text):
    """
    Prints to console and to log file
    """
    print(text)
    output_file.write(str(text))
    output_file.write('\n')


# === GETTERS ===
def get_zip_from_github():
    """
    Downloads zip from latest release, extracts to temporary download folder, renames it, moves it, deletes temps
    """
    log_output('Downloading from GitHub')
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
    with open(join(MOD_FOLDER, 'version.txt')) as version_file:
        return version_file.read().strip()

def load_patcher_json():
    with open(join(MOD_FOLDER, PATCHER_JSON)) as patcher_json:
        return json.load(patcher_json)

def load_configuration():
    with open(join(MOD_FOLDER, INSTALL_JSON)) as install_json:
        return json.load(install_json)


# === UI ===
def wx_radio(e):
    """
    WxPython radio button handler, changes game_variant
    """
    event = e.GetEventObject()
    global mod_from_backup
    mod_from_backup = bool(int(event.GetName()))

def wx_button(e):
    """
    WxPython radio button handler, changes game_variant
    """
    global install_canceled
    install_canceled = False
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
    """
    Loads entire interface
    """
    app = wx.App(False)  # Create a new app, don't redirect stdout/stderr to a window.
    frame = wx.Frame(None, wx.ID_ANY, "Sandbox Mod Components")  # A Frame is a top-level window.
    wx.StaticText(frame, label='Select "Modify what is currently loaded" if applying Sandbox on top of another mod', pos=(5, 5))
    frame.Bind(wx.EVT_RADIOBUTTON, wx_radio)
    wx.RadioButton(frame, label='Modify from backup', name='1', pos=(5, 30))
    wx.RadioButton(frame, label='Modify what is currently loaded', name='0', pos=(170, 30))
    frame.Bind(wx.EVT_BUTTON, wx_button)
    wx.Button(frame, label='Install!', pos=((WINDOW_X-100)//2, 60))

    patcher_json = load_patcher_json()
    frame.Bind(wx.EVT_CHECKBOX, wx_check)
    window = wx.ScrolledWindow(frame, pos=(0, 90))
    y_pos = 0 #var for keeping track of current y pos
    for category in patcher_json.keys():
        wx.StaticText(window, label=category, pos=(5, y_pos))
        wx.StaticLine(window, 2, pos=(0, y_pos+20), size=(1, 250), style=wx.HORIZONTAL)
        for option in patcher_json[category].keys():
            y_pos+=20
            name = ';'.join([join(category, file) for file in patcher_json[category][option]['paths']])
            wx.CheckBox(window, label=option, pos=(10, y_pos), name=name).SetToolTip(wx.ToolTip(patcher_json[category][option]['desc']))
        y_pos+=30
    window.SetSize(wx.Size(WINDOW_X-20, WINDOW_Y-130))
    scroll_unit = 10
    window.SetScrollbars(scroll_unit, scroll_unit, 0, (y_pos)//scroll_unit)
    frame.SetSize(wx.Size(WINDOW_X, WINDOW_Y))
    frame.Show(True)  # Show the frame.
    app.MainLoop()


# === MAIN ===
if __name__ == '__main__':
    dir_path = dirname(os.path.realpath(__file__))
    base_folder = os.path.basename(os.path.normpath(dir_path))
    if base_folder == 'Wargame Red Dragon':
        game_variant = 'Steam'
    elif base_folder == 'WargameRedDragon':
        game_variant = 'Epic'
    else:
        log_output('Please place this in your Wargame Red Dragon directory')
        exit()
    log_output(f'Game variant: {game_variant}')

    #Get most current version
    if not os.path.isdir(join(dir_path, MOD_FOLDER)):
        log_output('Mod folder does not exist')
        get_zip_from_github()
    else:
        if get_online_version() != get_current_version():
            log_output('Local mod outdated')
            log_output(f'{get_online_version()=}, {get_current_version()=}')
            get_zip_from_github()
        else:
            log_output('Local mod is most updated version')

    log_output('Getting install config')
    install_config = load_configuration()

    #Show interface
    log_output('Showing interface')
    show_interface()
    if install_canceled:
        log_output('Install canceled')
        exit()

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
    if patches_to_apply == []:
        log_output('No patches applied')
        input("Press enter to continue...")
        exit()
    log_output('Patching')
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
    with open(join(MOD_FOLDER, 'Installer', 'installerConfigTemplate.wmi')) as config_file:
        contents = config_file.read()
        splits = contents.split('%')
        for i in range(len(splits)):
            if i % 2:
                try:
                    splits[i] = config_replacements[splits[i]]
                except KeyError:
                    log_output(f'Key error with {splits[i]}')
        with open(join(MOD_FOLDER, 'Installer', 'installerConfig.wmi'), 'w+') as final_config:
            final_config.write(''.join(splits))

    #Run asset installer
    log_output('Running asset installer')
    asset_installer = subprocess.run('WargameModInstaller.exe', cwd=join(dir_path, MOD_FOLDER, 'Installer'), shell=True)



    log_output('Done!')
    input("Press enter to exit...")

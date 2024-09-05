import os
import requests
from os.path import join, dirname
import wx
import json

import logging


from shutil import copyfile, move, rmtree
import subprocess

from interface.maininterface import *
from interface.location import *
import utils

MOD_FOLDER = 'SandboxMod'


INSTALLER_VERSION = '1.1.1'
RELEASE_URL = 'https://api.github.com/repos/Noob-Development/Sandbox-Mod-Files/releases/latest'
MOD_FOLDER = 'SandboxMod'
PATCHES_LOG = 'patch_list.txt'
PATCHER_JSON = 'patcher_paths.json'
INSTALL_JSON = 'install_locations.json'
PRESANDBOX_SUFFIX = '_pre-sandbox'
ZIP_NAME = 'master.zip'
DEVMODE = False
DEBUGMODE = False


logger = logging.getLogger('logs')
logger.setLevel(logging.DEBUG)

cli_handler = logging.StreamHandler()
file_handler = logging.FileHandler('SandboxInstallOutput.txt')
cli_handler.setLevel(logging.DEBUG)
file_handler.setLevel(logging.DEBUG)

cli_formatter = logging.Formatter('[%(levelname)s] %(message)s', '%H:%M:%S')
file_formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', '%H:%M:%S')

cli_handler.setFormatter(cli_formatter)
file_handler.setFormatter(file_formatter)
logger.addHandler(cli_handler)
logger.addHandler(file_handler)

def log_output(text, level):
    if level == 'info':
        logger.info(text)
    elif level == 'warning':
        logger.warning(text)
    elif level == 'error':
        logger.error(text)
    elif level == 'debug':
        logger.debug(text)

def main():
    app = wx.App()
    frame = DirSelector(None)
    frame.Show(True)
    app.MainLoop()


if __name__ == '__main__':
    try:
        #Set logging mode
        log_output('Welcome to the Sandbox Mod Installer', 'info')
        log_output('Please wait until this console says "Finished!"', 'info')
        log_output('======================================================', 'info')

        #Show interface
        main()

        #Get game variant
        dir_path = utils.installLocation
        base_folder = os.path.basename(os.path.normpath(utils.installLocation))
        if base_folder == 'Wargame Red Dragon':
            game_variant = 'Steam'
        elif base_folder == 'WargameRedDragon':
            game_variant = 'Epic'
        else:
            log_output('Please place this in your Wargame Red Dragon folder', 'error')
            exit()
        log_output(f'Game variant: {game_variant}', 'info')

        #Load installation paths
        log_output('Getting install config', 'info')
        install_config = utils.load_configuration()

        #Logging patches applied
        if utils.patches_to_apply == []:
            log_output('No patches applied', 'info')
            input("Press enter to continue...")
            exit()
        #if mod_from_backup:
        #    patches_log = open(join(MOD_FOLDER, PATCHES_LOG), 'w+', encoding='utf-8')
        #else:
        patches_log = open(join(f'{dir_path}\\{MOD_FOLDER}', PATCHES_LOG), 'w+', encoding='utf-8')
        for patch in utils.patches_to_apply:
            patches_log.write(patch)
            patches_log.write('\n')
            patches_log.close()

        #Make original NDF_Win.dat file if needed
        #log_output(f'{mod_from_backup=}', 'debug')
        pc_path = join('Data', 'WARGAME', 'PC')
        ndf_path = join(pc_path, install_config[game_variant]["NDF_Win.dat"], "NDF_Win.dat")
        full_ndf_path = join(dir_path, ndf_path)
        if not os.path.isfile(full_ndf_path+PRESANDBOX_SUFFIX):
            log_output('Backup does not exist','warning')
            copyfile(full_ndf_path, full_ndf_path+PRESANDBOX_SUFFIX)
        #else:
        #    if mod_from_backup:
        #        os.remove(full_ndf_path)
        #        copyfile(full_ndf_path + PRESANDBOX_SUFFIX, full_ndf_path)

        #Call patcher
        log_output('', 'info')
        log_output('This normaly takes around 5 minutes to complete! The installer will say when its done!', 'info')
        log_output('', 'info')

        patcher_call_list = []
        for patch_path in utils.patches_to_apply:
            patcher_call_list += [f'{dir_path}\\{MOD_FOLDER}\\Script Library\\{patch_path}']
        patcher_call = [f'{dir_path}\\{MOD_FOLDER}\\Patcher\\WGPatcher.exe', 'apply', full_ndf_path] + patcher_call_list
        log_output(f'Patcher Call: {" ".join(patcher_call)}', 'info')
        patcher = subprocess.run([f'{dir_path}\\{MOD_FOLDER}\\Patcher\\WGPatcher.exe', 'apply', full_ndf_path] + patcher_call_list, cwd=dir_path)
        move(join(dirname(full_ndf_path), 'ndf_win_patched.dat'), full_ndf_path)

        #Make installerConfig

    #    if compatability_mode == False:
    #        log_output('Making asset installerConfig', 'debug')
    #        config_replacements = {
    #            'mod_version': utils.get_current_version(),
    #            'game_version': install_config[game_variant]["NDF_Win.dat"],
    #            'NDF_Win.dat-path': install_config[game_variant]["NDF_Win.dat"],
    #            'ZZ_Win.dat|interface_outgame-path': install_config[game_variant]["ZZ_Win.dat-interface_outgame"],
    #            'Data.dat-path': install_config[game_variant]["Data.dat"],
    #            'ZZ_4.dat-path': install_config[game_variant]["ZZ_4.dat"],}
    #        with open(join(MOD_FOLDER, 'Installer', 'installerConfigTemplate.wmi'), encoding='utf-8') as config_file, open(join(MOD_FOLDER, 'Installer', 'installerConfig.wmi'), 'w+', encoding='utf-8') as new_file:
    #            write_config(config_file, new_file)
    #            log_output('Writing to installerconfig', 'debug')
    #
    #        #Run asset installer
    #        log_output('Running asset installer', 'debug')
    #        asset_installer = subprocess.run('WargameModInstaller.exe', cwd=join(dir_path, MOD_FOLDER, 'Installer'), shell=True)


        log_output('\nFinished!', 'info')
        input("Press enter to exit...")

    except Exception as e:
        log_output(f'\nERROR: {e}', 'error')
        input("Press enter to exit...")

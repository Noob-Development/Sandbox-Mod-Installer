import os
import zipfile
from os.path import join
from shutil import copyfile, move, rmtree
import requests
import urllib.request
import json

from loggingConfig import setupLogging

logger = setupLogging()

MOD_FOLDER = 'SandboxMod'

#Global veriables nice right?
installLocation = None
patches_to_apply = []
mod_from_backup = True

#Get version and download if needed
def get_version_and_download():
    #Get most current version
    if not os.path.isdir(join(installLocation, MOD_FOLDER)):
        logger.warning('Mod not downloaded yet')
        get_zip_from_github()
    else:
        if get_online_version() != get_current_version():
            logger.warning('Local mod outdated, getting new version')
            logger.warning(f'Online version: {get_online_version()}, Local version: {get_current_version()}')
            get_zip_from_github()
        else:
            logger.info('Local mod is most updated version')

#Download zip from github
def get_zip_from_github():
    """
    Downloads zip from latest release, extracts to temporary download folder, renames it, moves it, deletes temps
    """
    logger.info('Downloading from GitHub, do not close...')
    download_url = json.loads(requests.get('https://api.github.com/repos/Noob-Development/Sandbox-Mod-Files/releases/latest', allow_redirects=True).content)['zipball_url']
    urllib.request.urlretrieve(download_url, os.path.join(installLocation, 'master.zip'))
    logger.info('Extracting Zip')
    with zipfile.ZipFile(join(installLocation, 'master.zip'), 'r') as zip_ref:
        zip_ref.extractall(os.path.join(installLocation, 'download'))
    logger.info('Moving folders')
    download_name = list(os.listdir(installLocation + '\\' + 'download'))[0]
    if os.path.isdir(join(installLocation, MOD_FOLDER)):
        rmtree(join(installLocation, MOD_FOLDER))
    os.rename(os.path.join(installLocation, 'download', download_name), os.path.join(installLocation, MOD_FOLDER))
    rmtree(join(installLocation, 'download'))
    os.remove(os.path.join(installLocation, 'master.zip'))

#Get version from github
def get_online_version():
    return json.loads(requests.get('https://api.github.com/repos/Noob-Development/Sandbox-Mod-Files/releases/latest', allow_redirects=True).content)['name']

#Get version from local
def get_current_version():
    with open(join(installLocation + '\\' + MOD_FOLDER, 'version.txt'), encoding='utf-8') as version_file:
        return version_file.read().strip()

#Load patcher locations
def load_patcher_json():
    with open(join(installLocation + '\\' + MOD_FOLDER, 'patcher_paths.json'), encoding='utf-8') as patcher_json:
        return json.load(patcher_json)

#Load install locations
def load_configuration():
    with open(join(installLocation + '\\' + MOD_FOLDER, 'install_locations.json'), encoding='utf-8') as install_json:
        return json.load(install_json)

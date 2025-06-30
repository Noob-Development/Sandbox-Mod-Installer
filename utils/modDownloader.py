import json
import os
import urllib.request
import zipfile
from os.path import join
from shutil import rmtree


from loggingConfig import setupLogging
logger = setupLogging()

import requests

from utils.apiCalls import callAnalyticsAPI
import utils.variables as var

#Get version and download if needed
def getVersionAndDownload():
    #Get most current version
    if not os.path.isdir(join(var.installLocation, var.MOD_FOLDER)):
        logger.warning('Mod not downloaded yet')
        getZipFromGithub()
    else:
        if getOnlineVersion() != getCurrentVersion():
            logger.warning('Local mod outdated, getting new version')
            logger.warning(f'Online version: {getOnlineVersion()}, Local version: {getCurrentVersion()}')
            getZipFromGithub()
        else:
            logger.info('Local mod is most updated version')

#Download zip from github
def getZipFromGithub():
    """
    Downloads zip from latest release, extracts to temporary download folder, renames it, moves it, deletes temps
    """
    #TODO: Rework this to use our own download server for more stable downloads
    logger.info('Downloading from GitHub, do not close...')
    download_url = json.loads(requests.get('https://api.github.com/repos/Noob-Development/Sandbox-Mod-Files/releases/latest', allow_redirects=True).content)['zipball_url']
    urllib.request.urlretrieve(download_url, os.path.join(var.installLocation, 'master.zip'))
    logger.info('Extracting Zip')
    with zipfile.ZipFile(join(var.installLocation, 'master.zip'), 'r') as zip_ref:
        zip_ref.extractall(os.path.join(var.installLocation, 'download'))
    logger.info('Moving folders')
    download_name = list(os.listdir(var.installLocation + '\\' + 'download'))[0]
    if os.path.isdir(join(var.installLocation, var.MOD_FOLDER)):
        rmtree(join(var.installLocation, var.MOD_FOLDER))
    os.rename(os.path.join(var.installLocation, 'download', download_name), os.path.join(var.installLocation, var.MOD_FOLDER))
    rmtree(join(var.installLocation, 'download'))
    os.remove(os.path.join(var.installLocation, 'master.zip'))
    callAnalyticsAPI('download', 'sandbox')
    logger.debug('Called analytics API for download')

#Get version from github
def getOnlineVersion():
    return json.loads(requests.get('https://api.github.com/repos/Noob-Development/Sandbox-Mod-Files/releases/latest', allow_redirects=True).content)['name']

#Get version from local
def getCurrentVersion():
    with open(join(var.installLocation + '\\' + var.MOD_FOLDER, 'version.txt'), encoding='utf-8') as version_file:
        return version_file.read().strip()

#Load patcher locations
def loadPatcherJson():
    with open(join(var.installLocation + '\\' + var.MOD_FOLDER, 'patcher_paths.json'), encoding='utf-8') as patcher_json:
        return json.load(patcher_json)

#Load install locations
def loadConfiguration():
    with open(join(var.installLocation + '\\' + var.MOD_FOLDER, 'install_locations.json'), encoding='utf-8') as install_json:
        return json.load(install_json)

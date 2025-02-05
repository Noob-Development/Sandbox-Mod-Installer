import os
import zipfile
from os.path import join
from shutil import copyfile, move, rmtree
import requests
import urllib.request
import json
import base64

from loggingConfig import setupLogging

logger = setupLogging()

MOD_FOLDER = 'SandboxMod'

API_URL = 'http://127.0.0.1:8000/'

#Global veriables nice right?
installLocation = None
patches_to_apply = []
mod_from_backup = True
invite_id = "No ID"

#Get version and download if needed
def getVersionAndDownload():
    #Get most current version
    if not os.path.isdir(join(installLocation, MOD_FOLDER)):
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
    callAnalyticsAPI('download', 'sandbox')
    logger.debug('Called analytics API for download')

#Get version from github
def getOnlineVersion():
    return json.loads(requests.get('https://api.github.com/repos/Noob-Development/Sandbox-Mod-Files/releases/latest', allow_redirects=True).content)['name']

#Get version from local
def getCurrentVersion():
    with open(join(installLocation + '\\' + MOD_FOLDER, 'version.txt'), encoding='utf-8') as version_file:
        return version_file.read().strip()

#Load patcher locations
def loadPatcherJson():
    with open(join(installLocation + '\\' + MOD_FOLDER, 'patcher_paths.json'), encoding='utf-8') as patcher_json:
        return json.load(patcher_json)

#Load install locations
def loadConfiguration():
    with open(join(installLocation + '\\' + MOD_FOLDER, 'install_locations.json'), encoding='utf-8') as install_json:
        return json.load(install_json)

#Send call to analytics API
def callAnalyticsAPI(action, mod):
    #TODO: Setup API call to analytics

    pass

#Encode patch list to base64 and send to API
def encodeAndSendPatchList():
    base64PatchList =  base64.b64encode(json.dumps(patches_to_apply).encode('utf-8')).decode('utf-8')
    print("test")
    try:
        response = requests.post(API_URL + 'api/invite/', json={'base64PatchList': base64PatchList})
        if response.status_code == 201:
            global invite_id
            logger.info('Sent patch list to API')
            invite_id = str(response.json().get('id'))
            print(invite_id)
        else:
            logger.error('Failed to send patch list to API')
    except Exception as e:
        logger.error('API call timed out')

#Get and decode patch list from API
def getAndDecodePatchList(invite_code):
    try:
        response = requests.get(API_URL + 'api/invite/' + invite_code)
        if response.status_code == 200:
            global patches_to_apply
            global invite_id
            patches_to_apply = json.loads(base64.b64decode(response.json().get('base64PatchList')).decode('utf-8'))
            invite_id = invite_code
            logger.info('Loaded options from invite code!')
            return True
        else:
            logger.error('Failed to get patch list from API')
            return False
    except Exception as e:
        logger.error('API call timed out')
        return False



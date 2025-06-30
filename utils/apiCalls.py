import base64
import json

import requests


from loggingConfig import setupLogging
logger = setupLogging()

import utils.variables as var


#Send call to analytics API
def callAnalyticsAPI(action, mod):
    #TODO: Setup API call to analytics

    pass

#Encode patch list to base64 and send to API
def encodeAndSendPatchList():
    base64PatchList =  base64.b64encode(json.dumps(var.patches_to_apply).encode('utf-8')).decode('utf-8')
    try:
        response = requests.post(var.API_URL + 'api/invite/', json={'base64PatchList': base64PatchList})
        if response.status_code == 201:
            logger.info('Sent patch list to API')
            var.invite_id = str(response.json().get('id'))
        else:
            logger.error('Failed to send patch list to API')
    except Exception as e:
        logger.error('API call timed out')

#Get and decode patch list from API
def getAndDecodePatchList(invite_code):
    try:
        response = requests.get(var.API_URL + 'api/invite/' + invite_code)
        if response.status_code == 200:
            var.patches_to_apply = json.loads(base64.b64decode(response.json().get('base64PatchList')).decode('utf-8'))
            var.invite_id = invite_code
            logger.info('Loaded options from invite code!')
            return True
        else:
            logger.error('Failed to get patch list from API')
            return False
    except Exception as e:
        logger.error('API call timed out')
        return False

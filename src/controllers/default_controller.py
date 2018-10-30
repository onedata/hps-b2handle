import logging as log
import urllib.parse
import requests
from requests.auth import HTTPBasicAuth


def resolve_handle(hndl, serviceProperties):
    return 'Not implemented', 501


def register_handle(hndl, handleProperties):

    try:
        serviceProperties = handleProperties['serviceProperties']
        username = serviceProperties['username']
        username = username.replace(':', '%3A')
        password = serviceProperties['password']
        endpoint = serviceProperties['endpoint']
        if not endpoint.endswith('/'):
            endpoint = endpoint + '/'
        prefix = serviceProperties['prefix']

        shareUrl = handleProperties['url']

        # Create handle endpoint URL
        handleEndpoint = urllib.parse.urljoin(endpoint, "{}/{}".format(prefix, hndl))

        handleData = {}
        handleData['values'] = []
        handleData['values'].append({
            "index": 1,
            "type": "url",
            "data": shareUrl})

        log.info("Trying to register a handle {}/{} using {}".format(
            prefix, hndl, handleEndpoint))

        r = requests.put(handleEndpoint, json=handleData,
                auth=HTTPBasicAuth(username, password))

        handle = r.json()['handle']

        log.info("Registered PID under location: {}".format(handle))

        return {"handle": handle}, r.status_code
    except KeyError as error:
        log.error("Invalid request: " + str(error))
        return 'Invalid request', 400
    except requests.RequestException as error:
        log.error("B2HANDLE connection error: " + str(error))
        return 'Internal server error', 500
    except Exception as error:
        log.error("Internal server error: " + str(error))
        return 'Internal server error', 500


def unregister_handle(hndl, serviceProperties):
    return 'Not implemented', 501


def update_handle(hndl, handleProperties):
    return 'Not implemented', 501

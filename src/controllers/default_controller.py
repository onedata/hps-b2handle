import logging as log
import urllib.parse
import os
import requests
from requests.auth import HTTPBasicAuth

HNDL_RESOLVE_PREFIX = 'http://hdl.handle.net/'
HNDL_CERT_FILE = '/hps-b2handle/certs/cert.pem'
HNDL_KEY_FILE = '/hps-b2handle/certs/privkey.pem'

def resolve_handle(hndl, serviceProperties):
    return 'Not implemented', 501


def register_handle(hndl, handleProperties):

    try:
        serviceProperties = handleProperties['serviceProperties']
        handleType = serviceProperties['type']
        if handleType != 'PID':
            raise "Invalid handle type " + str(handleType)
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
        handleData['values'].append({
            "index": 100,
            "type": "HS_ADMIN",
            "data": {
                 "format": "admin",
                 "value": {"handle": "0.NA/'{}'".format(prefix),
                          "index": 200,
                          "permissions": "011111110011"}}})

        log.info("Trying to register a handle {}/{} using {}".format(
            prefix, hndl, handleEndpoint))

        log.info("Handle data: {}".format(handleData))

        if username and password:
            # Use username and password authentication
            log.info("Using basic authentication")
            r = requests.put(handleEndpoint, json=handleData,
                    auth=HTTPBasicAuth(username, password))
        elif os.path.getsize(HNDL_CERT_FILE) and os.path.getsize(HNDL_KEY_FILE):
            # Use certificate for authentication
            log.info("Using cert based authentication")
            headers =  {}
            headers['content-type'] = 'application/json'
            headers['authorization'] = 'Handle clientCert="true"'
            r = requests.put(handleEndpoint, json=handleData, headers=headers,
                    cert=(HNDL_CERT_FILE, HNDL_KEY_FILE), verify=False)
        else:
            raise "Invalid or no authentication method provided"

        handle = HNDL_RESOLVE_PREFIX + r.json()['handle']

        if r.ok:
            log.info("Registered PID under location: {}".format(handle))
        else:
            log.error("Handle registration failed: {}".format(r.status_code))

        return {"handle": handle}, r.status_code
    except KeyError as error:
        log.error("Invalid request: " + str(error))
        return 'Invalid request', 400
    except requests.RequestException as error:
        log.error("HANDLE service connection error: " + str(error))
        return 'Internal server error', 500
    except Exception as error:
        log.error("Internal server error: " + str(error))
        return 'Internal server error', 500


def unregister_handle(hndl, serviceProperties):
    try:
        handleType = serviceProperties['type']
        if handleType != 'PID':
            raise "Invalid handle type " + str(handleType)
        username = serviceProperties['username']
        username = username.replace(':', '%3A')
        password = serviceProperties['password']
        endpoint = serviceProperties['endpoint']
        if not endpoint.endswith('/'):
            endpoint = endpoint + '/'
        prefix = serviceProperties['prefix']

        # Construct the handle URL
        handleEndpoint = urllib.parse.urljoin(endpoint, "{}/{}".format(prefix, hndl))


        log.info("Trying to unregister the handle {}/{} using {}".format(
            prefix, hndl, handleEndpoint))

        if username and password:
            # Use basic authentication
            log.info("Using basic authentication for unregister")
            headers =  {}
            headers['content-type'] = 'application/json'
            headers['accept'] = 'application/json'
            r = requests.delete(handleEndpoint, json={}, headers=headers, auth=HTTPBasicAuth(username, password))
        elif os.path.getsize(HNDL_CERT_FILE) and os.path.getsize(HNDL_KEY_FILE):
            # Use certificate-based authentication
            log.info("Using cert-based authentication for unregister")
            headers = {}
            headers['content-type'] = 'application/json'
            headers['authorization'] = 'Handle clientCert="true"'
            r = requests.delete(handleEndpoint, headers=headers,
                                cert=(HNDL_CERT_FILE, HNDL_KEY_FILE), verify=False)
        else:
            raise "Invalid or no authentication method provided"

        if r.ok:
            log.info("Successfully unregistered handle: {}".format(hndl))
            return {"message": "Handle unregistered successfully"}, r.status_code
        else:
            log.error("Handle unregistration failed: {}".format(r.status_code))
            return 'Failed to unregister handle', r.status_code
    except KeyError as error:
        log.error("Invalid request: " + str(error))
        return 'Invalid request', 400
    except requests.RequestException as error:
        log.error("HANDLE service connection error: " + str(error))
        return 'Internal server error', 500
    except Exception as error:
        log.error("Internal server error: " + str(error))
        return 'Internal server error', 500


def update_handle(hndl, handleProperties):
    return '', 204

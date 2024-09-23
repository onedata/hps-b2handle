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

def check_handle_type(serviceProperties):
    handleType = serviceProperties.get('type')
    if handleType != 'PID':
        raise Exception("Invalid handle type " + str(handleType))

def construct_handle_endpoint(serviceProperties, hndl):
    endpoint = serviceProperties['endpoint']
    if not endpoint.endswith('/'):
        endpoint += '/'
    prefix = serviceProperties['prefix']
    handleEndpoint = urllib.parse.urljoin(endpoint, f"{prefix}/{hndl}")
    return handleEndpoint

def get_auth_headers(serviceProperties, action):
    username = serviceProperties.get('username', '')
    password = serviceProperties.get('password', '')
    headers = {'Content-Type': 'application/json'}

    if action == 'unregister' and username and password:
        headers['Accept'] = 'application/json'

    if username and password:
        # Use basic authentication
        auth = HTTPBasicAuth(username.replace(':', '%3A'), password)
        cert = None
        log.info("Using basic authentication for {}".format(action))
    elif os.path.exists(HNDL_CERT_FILE) and os.path.exists(HNDL_KEY_FILE):
        # Use certificate-based authentication
        auth = None
        headers['Authorization'] = 'Handle clientCert="true"'
        cert = (HNDL_CERT_FILE, HNDL_KEY_FILE)
        log.info("Using cert-based authentication for {}".format(action))
    else:
        raise Exception("Invalid or no authentication method provided")
    return auth, headers, cert

def handle_exceptions(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError as error:
            log.error("Invalid request: " + str(error))
            return 'Invalid request', 400
        except requests.RequestException as error:
            log.error("HANDLE service connection error: " + str(error))
            return 'Internal server error', 500
        except Exception as error:
            log.error("Internal server error: " + str(error))
            return 'Internal server error', 500
    return wrapper

@handle_exceptions
def register_handle(hndl, handleProperties):
    serviceProperties = handleProperties['serviceProperties']
    check_handle_type(serviceProperties)
    handleEndpoint = construct_handle_endpoint(serviceProperties, hndl)
    shareUrl = handleProperties['url']

    # Prepare handle data
    handleData = {
        'values': [
            {
                "index": 1,
                "type": "url",
                "data": shareUrl
            },
            {
                "index": 100,
                "type": "HS_ADMIN",
                "data": {
                    "format": "admin",
                    "value": {
                        "handle": "0.NA/{}".format(serviceProperties['prefix']),
                        "index": 200,
                        "permissions": "011111110011"
                    }
                }
            }
        ]
    }

    log.info("Trying to register a handle {}/{} using {}".format(
        serviceProperties['prefix'], hndl, handleEndpoint))

    log.info("Handle data: {}".format(handleData))

    auth, headers, cert = get_auth_headers(serviceProperties, 'register')

    r = requests.put(handleEndpoint, json=handleData, headers=headers, auth=auth, cert=cert, verify=False)

    if r.ok:
        handle = HNDL_RESOLVE_PREFIX + r.json()['handle']
        log.info("Registered PID under location: {}".format(handle))
        return {"handle": handle}, r.status_code
    else:
        log.error("Handle registration failed: {}".format(r.status_code))
        return 'Failed to register handle', r.status_code

@handle_exceptions
def unregister_handle(hndl, serviceProperties):
    check_handle_type(serviceProperties)
    handleEndpoint = construct_handle_endpoint(serviceProperties, hndl)

    log.info("Trying to unregister the handle {}/{} using {}".format(
        serviceProperties['prefix'], hndl, handleEndpoint))

    auth, headers, cert = get_auth_headers(serviceProperties, 'unregister')

    r = requests.delete(handleEndpoint, headers=headers, auth=auth, cert=cert, verify=False)

    if r.ok:
        log.info("Successfully unregistered handle: {}".format(hndl))
        return {"message": "Handle unregistered successfully"}, r.status_code
    else:
        log.error("Handle unregistration failed: {}".format(r.status_code))
        return 'Failed to unregister handle', r.status_code

def update_handle(hndl, handleProperties):
    return '', 204

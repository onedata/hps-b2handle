# Handle Proxy Service for B2Handle

This is an example of implementation of a Handle Proxy Service, a [Onedata](https://onedata.org) proxy between Onezone component and [Handle](http://handle.net) global identifier registration services.

This implementation is specific for [B2HANDLE](https://www.eudat.eu/services/userdoc/b2handle) service.


## Building and running

### Dependencies

```bash
pip3 install -r requirements.txt
```

### Initialize submodules
To build this service first initialize and build the submodules:
```bash
./init-submodules.sh
```

### Start the proxy service
```bash
cd src
./app.py
# Optionally pass host and port for the server
# Defaults are '0.0.0.0' and '8080'
./app.py --host 127.0.0.1 --port 9999
```

The service has a user interface which allows manual generation of REST requests:
```bash
open http://localhost:8080/api/v1/ui
```

### Running from Docker
```bash
docker run -p 8080:8080 -t docker.onedata.org/hps-b2handle:1.0.0

open http://localhost:8080/api/v1/ui
```
For PID registration services, which require cert based authorization, the key and cert should be mounted
as Docker volumes, e.g.:
```bash
docker run -v $PWD/privkey.pem:/hps-b2handle/certs/privkey.pem -v $PWD/cert.pem:/hps-b2handle/certs/cert.pem onedata/hps-b2handle:1.0.0
```

## Testing from command line

First export username and password to B2HANDLE:
```bash
export B2HANDLE_USERNAME=...
export B2HANDLE_PASSWORD=...
```

### Resolve existing handle in B2HANDLE
```bash
echo '{"type": "PID", "endpoint": "https://hdl.grnet.gr:8001/api/handles", "username": "${B2HANDLE_USERNAME}", "password": ${B2HANDLE_PASSWORD}" }' | \
curl -X POST --header 'Content-Type: application/json' --header 'Accept: text/plain' \
-d @- 'http://localhost:8080/api/v1/handle?hndl=10.5072/TEST.1'
```


### Register a handle in B2HANDLE
An example JSON document that should be passed to this service to register a DOI is below:
```json
{
  "url": "http://onedata.org/share/LHASDJHASLKDJHpyp98hpiUABSDihPASUD",
  "serviceProperties": {
    "host": "https://hdl.grnet.gr:8001/api/handles"",
    "prefix": "PREFIX",
    "username": "USERNAME",
    "password": "PASSWORD",
    "type": "PID",
  },
  "metadata": {}
}
```

Paste this JSON into a `handle.json` file and run:
```bash
cat handle.json | \
curl -X PUT -H 'Content-Type: application/json' -H 'Accept: application/json' -d @- 'http://localhost:8080/api/v1/handle?hndl=share1'
```



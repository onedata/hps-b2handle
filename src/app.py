#!/usr/bin/env python3

import connexion
import logging
import argparse
import os

app = connexion.App(__name__, specification_dir='./swagger/')
app.add_api('swagger.yaml', strict_validation=True)

logging.basicConfig(level=logging.INFO)

def parse_args():
    parser = argparse.ArgumentParser(description='Onedata handle proxy implementation for PID handles.')

    # Fetch host and port from environment variables if available
    default_host = os.getenv('HANDLE_PROXY_HOST', '0.0.0.0')
    default_port = int(os.getenv('HANDLE_PROXY_PORT', '8080'))

    # Command-line options for host and port
    parser.add_argument('--host', type=str, default=default_host,
                        help=f'The host to bind to. Default is {default_host} (or from HANDLE_PROXY_HOST environment variable)')
    parser.add_argument('--port', type=int, default=default_port,
                        help=f'The port to bind to. Default is {default_port} (or from HANDLE_PROXY_PORT environment variable)')

    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    app.run(host=args.host, port=args.port)

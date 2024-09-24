#!/usr/bin/env python3

import connexion
import logging
import argparse

app = connexion.App(__name__, specification_dir='./swagger/')
app.add_api('swagger.yaml', strict_validation=True)

logging.basicConfig(level=logging.INFO)

def parse_args():
    parser = argparse.ArgumentParser(
            description='Onedata Handle Proxy service implementation for PID handles.')
    parser.add_argument('--host', type=str, default='0.0.0.0', help='Hostname to bind to. Default is 0.0.0.0')
    parser.add_argument('--port', type=int, default=8080, help='Port to bind to. Default is 8080')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    app.run(host=args.host, port=args.port)

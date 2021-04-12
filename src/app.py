#!/usr/bin/env python3

import connexion
import logging

import sys
import os

app = connexion.App(__name__, specification_dir='./swagger/')
app.add_api('swagger.yaml', strict_validation=True)

logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    app.run(port=8080, debug=True)

#!/bin/bash

git submodule init
git submodule update

cd handle-proxy-service && ./build.sh && cd ..


#!/usr/bin/env bash

cd $(dirname $BASH_SOURCE)

certoraRun.py LinearSearch.sol:LinearSearch \
              --path $PWD \
              --verify LinearSearch:LinearSearch.cvl \
              "$@"

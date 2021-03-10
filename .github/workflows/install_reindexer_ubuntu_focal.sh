#!/usr/bin/env bash

filelist=$(wget -q -O - http://repo.reindexer.org/ubuntu-focal/amd64/ | grep "reindexer-dev" | sed "/.*>\(reindexer-dev.*\)<.*/s//\1/")

filename=$(./choose_latest_version.sh "$filelist")

wget -O $filename http://repo.reindexer.org/ubuntu-focal/amd64/$filename
apt install $filename

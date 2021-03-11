#!/usr/bin/env bash

pwd
ls -a
cd $RX_DIR/build
for f in reindexer*.deb; do
	sudo dpkg -i $f
	sudo apt-get install -f
done;

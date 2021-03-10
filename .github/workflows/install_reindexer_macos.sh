#!/usr/bin/env bash

filelist=$(wget -q -O - http://repo.reindexer.org/brew-bottles/ | grep "reindexer-" | sed "/.*>\(reindexer-.*\)<.*/s//\1/")

filename=$(./.github/workflows/choose_latest_version.sh "$filelist")

wget -O $filename http://repo.reindexer.org/brew-bottles/$filename
brew tap restream/reindexer
brew install $filename

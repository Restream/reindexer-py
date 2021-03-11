#!/usr/bin/env bash

pwd
ls
python3 example/main.py
cd tests
python3 -m unittest test_builtin.py
reindexer_server --db /tmp/reindex_test -l0 --serverlog="" --corelog="" --httplog="" --rpclog="" &
server_pid=$!
sleep 1
python3 -m unittest test_cproto.py

kill $server_pid
wait $server_pid

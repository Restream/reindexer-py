export PYTHONPATH=$(pwd)
python3 example/main.py || exit 1
python3 -m pytest tests/tests || exit 1
reindexer_server --db /tmp/reindex_test -l0 --serverlog="" --corelog="" --httplog="" --rpclog="" &
server_pid=$!
sleep 1
python3 -m pytest tests/tests --mode=cproto || exit 1
kill $server_pid
wait $server_pid

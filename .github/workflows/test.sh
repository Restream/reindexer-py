python3 example/main.py || exit 1
python3 -m unittest tests/test_builtin.py || exit 1
python3 -m pytest ../qa_test/tests || exit 1
reindexer_server --db /tmp/reindex_test -l0 --serverlog="" --corelog="" --httplog="" --rpclog="" &
server_pid=$!
sleep 1
python3 -m pytest -m unittest tests/test_cproto.py || exit 1
pytest ../qa_test/tests --mode=cproto || exit 1
kill $server_pid
wait $server_pid

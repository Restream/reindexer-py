export PYTHONPATH=$(pwd)
python3 example/main.py || exit 1
python3 -m pytest tests/tests --mode=builtin || exit 1
python3 -m pytest tests/tests --mode=cproto || exit 1

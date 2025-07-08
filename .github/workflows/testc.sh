export PYTHONPATH=$(pwd)

echo "Start cproto tests"
python3 -m pytest tests/tests --mode=cproto || exit 1

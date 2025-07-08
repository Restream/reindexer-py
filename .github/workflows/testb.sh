export PYTHONPATH=$(pwd)

echo "Start example"
python3 example/main.py || exit 1

echo "Start builtin tests"
python3 -m pytest tests/tests --mode=builtin || exit 1

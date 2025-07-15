export PYTHONPATH=$(pwd)

if [[ -z "$1" || "$1" == *"builtin"* ]]; then
  echo "Start example"
  python3 example/main.py || exit 1

  echo "Start builtin tests"
  python3 -m pytest tests/tests --mode=builtin || exit 1
fi

if [[ -z "$1" || "$1" == *"cproto"* ]]; then
  echo "Start cproto tests"
  python3 -m pytest tests/tests --mode=cproto || exit 1
fi

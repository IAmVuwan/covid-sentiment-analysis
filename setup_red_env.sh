#!/bin/bash

set -e

eval "$(ssh-agent)" && ssh-add ~/.ssh/gitops
git pull

export TMPDIR=$HOME/tmp/
rm -rf "$TMPDIR" && mkdir -p "$TMPDIR"
pip install -r requirements.txt && pip install --editable .

Action=$1

echo "Action: $1"

if [ -z "$Action" ]; then
  echo "Please set the 1st argument: action"
  echo "Retry: ./setup_red_env.sh <action>"
  exit 1
fi

if [ "$Action" == "notebook" ]; then
  python -m pip install jupyter
  jupyter notebook
fi

nohup csa "--action=$Action" \
  >"$Action.log" </dev/null 2>&1 &

tail -f "$Action.log"

#!/bin/bash

set -e

eval "$(ssh-agent)" && ssh-add ~/.ssh/gitops
git pull

export TMPDIR=$HOME/tmp/
rm -rf "$TMPDIR" && mkdir -p "$TMPDIR"
pip install -r requirements.txt && pip install --editable .
python -m pip install jupyter

nohup jupyter notebook \
  >"notebook.log" </dev/null 2>&1 &

tail -f "notebook.log"

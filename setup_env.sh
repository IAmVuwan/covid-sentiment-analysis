#!/bin/bash

set -e

python -m pip install jupyter
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt && pip install --editable .
jupyter notebook

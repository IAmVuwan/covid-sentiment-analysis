#!/bin/bash

set -e

CORENLP_HOME="$HOME/.csa/corenlp"
CORENLP_APP_HOME="$CORENLP_HOME/stanford-corenlp-4.5.1"

if [ ! -d "$CORENLP_APP_HOME" ]; then
  mkdir -p "$CORENLP_HOME"
  zip_file="$CORENLP_HOME/corenlp.zip"
  echo "$zip_file does not exist on your filesystem."
  wget https://nlp.stanford.edu/software/stanford-corenlp-4.5.1.zip -O "$zip_file"
  unzip "$zip_file" -d "$CORENLP_HOME"
fi

nohup java -mx4g \
  -cp "$CORENLP_APP_HOME/*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer \
  -port 9000 -timeout 9999999999 \
  >coreNLP.log </dev/null 2>&1 &

tail -f coreNLP.log

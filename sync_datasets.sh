#!/bin/bash

set -e

mkdir -p ~/.csa/data/raw/

scp -o IdentitiesOnly=yes <your_username>@<your_dns_server>:~/.csa/data/raw/ids.csv ~/.csa/data/raw/ids.csv
scp -o IdentitiesOnly=yes <your_username>@<your_dns_server>:~/.csa/data/raw/clean_tweets.csv ~/.csa/data/raw/clean_tweets.csv
scp -o IdentitiesOnly=yes <your_username>@<your_dns_server>:~/.csa/data/raw/us-tweets.pkl ~/.csa/data/raw/us-tweets.pkl

mkdir -p ~/.csa/data/preprocess/
scp -o IdentitiesOnly=yes <your_username>@<your_dns_server>:~/.csa/data/preprocess/us-tweets.pkl ~/.csa/data/preprocess/us-tweets.pkl
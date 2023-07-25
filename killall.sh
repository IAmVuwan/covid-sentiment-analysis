#!/bin/bash

set -e

echo  "Killing 'csa --action=preprocess'"
ps -ef | grep "csa --action=preprocess" | grep -v grep | awk '{print $2}' | xargs -r kill -9
echo  "Killed 'csa --action=preprocess'"
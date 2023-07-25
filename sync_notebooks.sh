#!/bin/bash

set -e

scp -o IdentitiesOnly=yes <your_username>@<your_dns_server>:~/covid-sentiment-analysis/notebooks/notebook-biweekly.ipynb ./notebooks/notebook-biweekly.ipynb
scp -o IdentitiesOnly=yes <your_username>@<your_dns_server>:~/covid-sentiment-analysis/notebooks/notebook-monthly.ipynb ./notebooks/notebook-monthly.ipynb
scp -o IdentitiesOnly=yes <your_username>@<your_dns_server>:~/covid-sentiment-analysis/notebooks/notebook-monthly-final.ipynb ./notebooks/notebook-monthly-final.ipynb
scp -o IdentitiesOnly=yes <your_username>@<your_dns_server>:~/covid-sentiment-analysis/notebooks/notebook.ipynb ./notebooks/notebook.ipynb
scp -o IdentitiesOnly=yes <your_username>@<your_dns_server>:~/covid-sentiment-analysis/notebooks/tests.ipynb ./notebooks/tests.ipynb
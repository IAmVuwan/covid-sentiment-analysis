# Lamar RED Setup

Remote server in Lamar RED

## To Login into Lamar RED

```bash
ssh -o IdentitiesOnly=yes <your_username>@<your_dns_server>
password: <your_password>
```

## Install Prerequisite

* Install virtualenv

```bash
python -m pip install --user virtualenv
```

* Install git without sudo user

```bash
mkdir -p "$HOME/git/"
cd "$HOME/git/"
wget https://mirrors.edge.kernel.org/pub/software/scm/git/git-2.9.4.tar.gz --no-check-certificate
tar -xvf git-2.9.4.tar.gz
cd "$HOME/git/git-2.29.2/"
./configure --prefix=$HOME/git/git-2.9.4/
make
make install
./git --version
```

* Update the PATH variable 

`export PATH=$PATH:$HOME/git/git-2.9.4/`

```bash
vi ~/.bashrc
exec "$SHELL"
git version
```

* Install `cmake`

```bash
mkdir -p "$HOME/cmake/"
cd "$HOME/cmake/"
wget https://github.com/Kitware/CMake/releases/download/v3.25.1/cmake-3.25.1.tar.gz --no-check-certificate
tar -xvf cmake-3.25.1.tar.gz
cd "$HOME/cmake/cmake-3.25.1/"
./bootstrap && make && make install
```

* Update the PATH variable

`export PATH=$PATH:$HOME/cmake/cmake-3.25.1/bin/`


```bash
vi ~/.bashrc
exec "$SHELL"
cmake
```

* Install `conda`

```bash
wget https://repo.anaconda.com/miniconda/Miniconda3-py39_4.12.0-Linux-x86_64.sh
chmod +x Miniconda3-py39_4.12.0-Linux-x86_64.sh
./Miniconda3-latest-Linux-x86_64.sh
```

```bash
conda install pip
```

## Copy source codes

```bash
ssh-keygen -q -N "" -f ~/.ssh/gitops
cat ~/.ssh/gitops.pub
```

> Note: Add this public key to your [repository](https://github.com:bhuwanupadhyay/covid-sentiment-analysis) Settings >
> Deploy Key

Change permissions:

```bash
chmod 600 ~/.ssh/gitops
```

* Load ssh key in ssh-agent: (Note: required when Launchpad restarted as well)

```bash
eval "$(ssh-agent)" && ssh-add ~/.ssh/gitops
```

```bash
git config --global pull.ff true
```

* Setup Repository

```bash
git clone git@github.com:bhuwanupadhyay/covid-sentiment-analysis.git
```

* Install Dependencies

```bash
./setup_red_env.sh
```

* Start CoreNLP

```bash
./setup_corenlp.sh
```

* Run Action `notebook|download|extract|preprocess`

```bash
./setup_red_env.sh <action>
```

## Useful commands

* Test CoreNLP Server
```bash
wget --post-data 'The quick brown fox jumped over the lazy dog.' 'localhost:9000/?properties={"annotators":"tokenize,pos","outputFormat":"json"}' -O -
```

* Copy from local to remove using scp

```bash
scp -o IdentitiesOnly=yes -r <local_dir> <your_username>@<your_dns_server>:<remote_dir>
```

* Copy from remote to local using scp

```bash
scp -o IdentitiesOnly=yes <your_username>@<your_dns_server>:<remote_filepath> <local_filepath>
```
For example:

```bash
mkdir -p  ~/.csa/data/raw
scp -o IdentitiesOnly=yes <your_username>@<your_dns_server>:~/.csa/data/raw/us-tweets.pkl ~/.csa/data/raw/us-tweets.pkl
scp -o IdentitiesOnly=yes <your_username>@<your_dns_server>:~/.csa/data/preprocess/us-tweets.pkl ~/.csa/data/preprocess/us-tweets.pkl
scp -o IdentitiesOnly=yes <your_username>@<your_dns_server>:~/covid-sentiment-analysis/notebooks/notebook.ipynb ./notebooks/notebook.ipynb
```

* Access remote server from local over SSH by setting up SSH tunnel

```bash
ssh -o IdentitiesOnly=yes -L <local_port>:localhost:<remote_port> <your_username>@<your_dns_server>
```

for example jupyter notebook

```bash
ssh -o IdentitiesOnly=yes -L 8888:localhost:8888 <your_username>@<your_dns_server>
```
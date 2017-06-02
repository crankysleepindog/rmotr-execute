#!/bin/bash
# Basic Setup
sudo apt-get update -y
sudo apt-get install -y git vim curl software-properties-common

# Docker Setup

sudo apt-get install -y linux-image-extra-4.4.0-1013-gke # AWS Hack
sudo apt-get install -y linux-image-extra-virtual
sudo apt-get install -y apt-transport-https ca-certificates

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

sudo apt-get update -y

sudo groupadd docker
sudo usermod -aG docker $USER

# Python
sudo add-apt-repository -y ppa:fkrull/deadsnakes
sudo apt-get install -y python3.6

# Python - Pip
wget https://bootstrap.pypa.io/get-pip.py
python3 get-pip.py --user
pip install virtualenv --user
pip install virtualenvwrapper --user

WORKON_HOME=$HOME/.virtualenvs
mkdir -p $WORKON_HOME
echo -e "\n# Virtualenvwrapper" >> ~/.bashrc
echo "export WORKON_HOME=$WORKON_HOME" >> ~/.bashrc
echo "export VIRTUALENVWRAPPER_PYTHON=\$(which python3)" >> ~/.bashrc
echo "VIRTUALENVWRAPPER_PYTHON=\$(which python3) source $HOME/.local/bin/virtualenvwrapper.sh" >> ~/.bashrc
echo -e "# Virtualenvwrapper\n" >> ~/.bashrc
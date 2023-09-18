#!/bin/bash

# Instala o pip
apt-get update
apt-get install python3-pip

# Instala as dependências do Python
pip install -r requirements.txt
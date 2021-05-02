#!/bin/bash

conda env create --name bumblebee-ai --file bumblebee_env_mac.yml --force
conda activate bumblebee-ai
python main.py

#!/bin/bash

conda env create --name bumblebee-ai --file bumblebee_env.yml
conda activate bumblebee-ai
python main.py

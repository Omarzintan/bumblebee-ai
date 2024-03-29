#!/bin/bash

conda env create --name bumblebee-ai --file environment_setup/environment_mac.yml --force
conda activate bumblebee-ai
pip install -r requirements.txt

BUMBLEBEE_APP_FILE=/usr/local/bin/bumblebee
if [ ! -f "$BUMBLEBEE_APP_FILE" ]; then
    python create_bumblebee_app.py
    chmod +x bumblebee_app
    echo "copying executable to /usr/local/bin/bumblebee"
    cp ./bumblebee_app $BUMBLEBEE_APP_FILE
fi
echo "run 'bumblebee' from anywhere in terminal to activate bumblebee."
python main.py
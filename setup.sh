#!/bin/bash

conda env create --name bumblebee-ai --file environment_mac.yml --force
conda activate bumblebee-ai
pip install -r requirements.txt
pip install -e git+https://github.com/Omarzintan/ChatterBot.git@master#egg=chatterbot

# In case issues come with downloading chatterbot-corpus, go to this link for a possible solution:
# https://github.com/man-group/pytest-plugins/issues/87#issuecomment-1123830409 
pip install -e git+https://github.com/Omarzintan/chatterbot-corpus.git@master#egg=chatterbot-corpus
python -m spacy download en_core_web_sm

BUMBLEBEE_APP_FILE=/usr/local/bin/bumblebee
if [ ! -f "$BUMBLEBEE_APP_FILE" ]; then
    python create_bumblebee_app.py
    chmod +x bumblebee_app
    echo "copying executable to /usr/local/bin/bumblebee"
    cp ./bumblebee_app $BUMBLEBEE_APP_FILE
fi
echo "run 'bumblebee' from anywhere in terminal to activate bumblebee."
python main.py
from utils.helpers import bumblebee_root, python3_path

with open("bumblebee_app", "w") as file:
    file.write("#!/bin/sh\n")
    file.write("export BUMBLEBEE_PATH="+bumblebee_root+"\n")
    file.write("export PYTHON3_PATH="+python3_path+"\n")
    file.write("export SERVER_URL=http://127.0.0.1:5000\n")
    file.write("\n")
    file.write("$PYTHON3_PATH $BUMBLEBEE_PATH/main.py")

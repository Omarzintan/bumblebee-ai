'''
This file is just for building a default config file on first install.
Any updates to the config.yaml file should be made directly into
config/config.yaml
'''
import yaml
from helpers import bumblebee_root
from helpers import python3_path


def build_config():
    config = {}

    config["Common"] = {}
    config["Common"]["bumblebee_dir"] = bumblebee_root
    config["Common"]["python3_path"] = python3_path

    config["Database"] = {}
    config["Database"]["path"] = bumblebee_root+"database/"
    config["Database"]["zoom"] = bumblebee_root+"database/zoom_db.json"
    config["Database"]["research"] = bumblebee_root+"database/research_db.json"
    config["Database"]["employers"] = bumblebee_root+"database/employers_db" \
                                                     ".json"
    config["Database"]["contacts"] = bumblebee_root+"database/contacts_db.json"

    config["Api_keys"] = {}
    config["Api_keys"]["wolframalpha"] = "YOUR_API_KEY_HERE"
    config["Api_keys"]["gmail"] = "YOUR_PATH_TO_GMAIL_CREDENTIALS_FILE"

    config["Folders"] = {}
    config["Folders"]["work_study"] = bumblebee_root+"work_study"
    config["Folders"]["research_files"] = bumblebee_root+"research_files/"
    config["Folders"]["models"] = bumblebee_root+"models/"

    config["Utilities"] = {}
    config["Utilities"]["research_server_url"] = "http://127.0.0.1:5000"

    return config


def write_yaml(data):
    with open(bumblebee_root+"utils/config.yaml", "w") as config_file:
        yaml.dump(data, config_file)


def build_yaml():
    try:
        config = build_config()
        write_yaml(config)
        return 0
    except Exception:
        return -1

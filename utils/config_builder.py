'''
This file is just for building a default config file on first install.
Any updates to the config.yaml file should be made directly into
config/config.yaml
'''
from typing import Any, List
import yaml
from helpers import bumblebee_root
from helpers import python3_path
import copy


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
    config["Database"]["chatbot"] = bumblebee_root+"database/chatbot.sqlite3"
    config["Database"]["routines"] = bumblebee_root+"database/routines_db.json"

    config["Api_keys"] = {}
    config["Api_keys"]["wolframalpha"] = "YOUR_API_KEY_HERE"
    config["Api_keys"]["gmail"] = "YOUR_PATH_TO_GMAIL_CREDENTIALS_FILE"
    config["Api_keys"]["bumblebee_online"] = "YOUR_BUMBLEBEE_ONLINE_API_KEY"

    config["Folders"] = {}
    config["Folders"]["work_study"] = bumblebee_root+"work_study"
    config["Folders"]["research_files"] = bumblebee_root+"research_files/"
    config["Folders"]["models"] = bumblebee_root+"models/"
    config["Folders"]["routines"] = bumblebee_root+"routines/"
    config["Folders"]["intents"] = bumblebee_root+"utils/intents/"

    config["Utilities"] = {}
    config["Utilities"]["research_server_url"] = "http://127.0.0.1:5000"
    config["Utilities"]["default_speech_mode"] = 'voice'

    config["Preferences"] = {}
    # Other possible wake_phrases are: 'porcupine', 'grasshopper', 'jarvis',
    # 'terminator', 'americano', 'alexa', 'blueberry', 'hey siri',
    # 'hey google', 'computer', 'grapefruit', 'pico clock', 'bumblebee',
    # 'picovoice', 'ok google'
    config["Preferences"]["wake_phrase"] = "bumblebee"
    # Other possible feature_lists are: test, geo, cybersecurity
    config["Preferences"]["feature_list"] = "all"
    # The name of the config file to use.
    config["Preferences"]["config_file"] = "config"
    # How decisions will be made by the Bee. Options are: rule-based or
    # neural-network
    config["Preferences"]["decision_strategy"] = "rule-based"

    return config


def write_yaml(data, config_path):
    with open(config_path, "w") as config_file:
        yaml.dump(data, config_file)


def build_yaml(filename):
    try:
        config = build_config()
        write_yaml(config, filename)
        return 0
    except Exception:
        return -1


def _update_dict(d: dict, keypath: List[str], value: Any):
    '''Updates a dictionary by inserting value at specified keypath'''
    updated_dict = copy.deepcopy(d)

    current = updated_dict

    nested_key_path = keypath[:-1]
    final_key = keypath[len(keypath) - 1]

    for key in nested_key_path:
        current = current.get(key, {})

    current[final_key] = value

    return updated_dict


def update_yaml(filename: str, keypath: List[str], value: Any):
    with open(filename, "r") as yamlfile:
        data: dict = yaml.safe_load(yamlfile)
        updated_data = _update_dict(data, keypath, value)
        write_yaml(updated_data, filename)


def create_fake_config():
    return build_config()

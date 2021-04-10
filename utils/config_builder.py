import yaml
import subprocess
from helpers import bumblebee_root

config = {}

config["Common"] = {}
config["Common"]["bumblebee_dir"] = bumblebee_root
config["Common"]["python3_env"] = subprocess.check_output(["which", "python3.7"]).decode('utf-8').strip()

config["Databases"] = {}
config["Databases"]["zoom"] = bumblebee_root+"databases/zoom_db.json"
config["Databases"]["research"] = bumblebee_root+"databases/research_db.json"
config["Databases"]["employers"] = bumblebee_root+"databases/employers_db.json"
config["Databases"]["contacts"] = bumblebee_root+"databases/contacts_db.json"

config["Folders"] = {}
config["Folders"]["work_study"] = bumblebee_root+"work_study"
config["Folders"]["research_files"] = bumblebee_root+"research_files/"

config["Utilities"] = {}
config["Utilities"]["research_server_url"] = "http://127.0.0.1:5000"

def write_yaml(data):
    with open("utils/config2.yaml", "w") as config_file:
        yaml.dump(data, config_file)

def build_yaml():
    try:
        write_yaml(config)
        return 0
    except:
        return -1

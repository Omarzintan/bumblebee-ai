import os

def get_root_directory():
    '''Gets the root directory of the project. Source: https://www.kite.com/python/answers/how-to-get-the-path-of-the-root-project-structure-in-python'''
    bumblebee_root_dir = os.getenv('BUMBLEBEE_PATH')
    if not bumblebee_root_dir:
        top_level_filename = "bumblebee.py"
        bumblebee_root_dir = os.path.dirname(os.path.abspath(top_level_filename))
        
    return bumblebee_root_dir + "/"
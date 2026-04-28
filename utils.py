"""
Folder walking and name cleaning
"""

import re
from pathlib import Path
from config import IGNORED_FOLDERS

def get_folders(root_folder):
    """
    Walk through all subfolders recursively, skip anything in the
    IGNORED_FOLDERS list, and return a list of folder paths to process.
    """
    folders = []
    for folder in Path(root_folder).rglob('*'):
        if folder.is_dir() and folder.name.lower() not in [f.lower() for f in IGNORED_FOLDERS]:
            folders.append(folder)

    return folders

def clean_folder_name(folder_name):
    """ Clean up a messy folder name and return a dictionary with title and year """
    pattern = r'^\d{1,3}\s*[-\s]\s*' # Matches 1 or 3 digits at the start, optionally followed by space, hyphen, space

    return re.sub(pattern, '', folder_name)
"""
Folder walking and name cleaning
"""

from pathlib import Path
from config import IGNORED_FOLDERS

def get_folders(root_folder):
    """
    Walk through all subfolders recursively, skip anything in the
    IGNORED_FOLDERS list, and return a list of folder paths to process.
    """
    folders = []
    for folder in Path(root_folder).rglob('*'):
        if folder.is_dir() and folder.name not in IGNORED_FOLDERS:
            folders.append(folder)

    return folders
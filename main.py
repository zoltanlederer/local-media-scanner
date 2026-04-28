"""
Main entry point for the Local Media Scanner.
"""

import argparse
from tmdb import test_connection, search_tmdb
from utils import get_folders

parser = argparse.ArgumentParser(description='Scan local media files')
parser.add_argument('-f', '--folder', help='Select a folder for the scan')
args = parser.parse_args()
root_folder = args.folder

# test_connection()

data = search_tmdb(title="The Dark Knight", media_type='movie', year='2008')
# print(data)

folders = get_folders(root_folder)
print(folders)
"""
Main entry point for the Local Media Scanner.
"""

import argparse
import time
import unicodedata
from tmdb import test_connection, search_tmdb
from utils import get_folders, clean_folder_name

def process_folders(folders, media_type):
    """ Loops through folders, cleans each name, calls search_tmdb(), and returns two lists: matched and unmatched """
    matched = []
    unmatched = []

    for folder in folders:
        clean_folder = clean_folder_name(folder.name)
        time.sleep(0.25) # wait 250ms between calls
        title = unicodedata.normalize('NFC', clean_folder['title']) # normalize unicode characters to avoid encoding mismatches when searching TMDB        
        results = search_tmdb(title=title, year=clean_folder['year'], media_type=media_type)

        if results is None: # a connection failure adds the folder to unmatched rather than crashing the whole program
            unmatched.append(clean_folder)
        elif results['results']:
            matched.append(results['results'][0])
        else:
            unmatched.append(clean_folder)

    return matched, unmatched


# --- CLI setup ---
parser = argparse.ArgumentParser(description='Scan local media files')
parser.add_argument('-f', '--folder', help='Select a folder for the scan')
parser.add_argument('-m', '--media-type', choices=['movie', 'tv'], help='Select the type of media: "movie" or "tv" for tv show.')
args = parser.parse_args()
root_folder = args.folder
media_type = args.media_type

# --- Main execution ---
folders = get_folders(root_folder)
media_info = process_folders(folders, media_type)

print('MATCHED', media_info[0])
print('NOT MATCHED', media_info[1])
"""
Main entry point for the Local Media Scanner.
"""

import argparse
import time
import unicodedata
import csv
from tmdb import test_connection, search_tmdb
from utils import get_folders, clean_folder_name, get_genre

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


def prepare_data(matched, media_type):    
    """ Clean and reformat raw TMDB results — remove unwanted fields, rename keys, convert genre IDs to names, and add media type """
    remove = {'adult', 'backdrop_path', 'original_language', 'popularity', 'poster_path', 'softcore', 'video', 'vote_average', 'vote_count'}
    rename = {'id': 'tmdb_id', 'overview': 'description', 'genre_ids': 'genres'}

    for data in matched:
        data['genre_ids'] = get_genre(data['genre_ids'], media_type)
        # remove unwanted keys
        for item in remove:
            data.pop(item)
        # rename keys
        for old_key, new_key in rename.items():
            data[new_key] = data.pop(old_key)        
        # add media type as a new field
        data['type'] = media_type    
    return matched
        


# --- CLI setup ---
parser = argparse.ArgumentParser(description='Scan local media files')
parser.add_argument('-f', '--folder', help='Select a folder for the scan')
parser.add_argument('-m', '--media-type', choices=['movie', 'tv'], help='Select the type of media: "movie" or "tv" for tv show.')
args = parser.parse_args()
root_folder = args.folder
media_type = args.media_type

# --- Main execution ---
folders = get_folders(root_folder)
matched, unmatched = process_folders(folders, media_type)
clean_data = prepare_data(matched, media_type)

# print('===>', clean_data)

# print('MATCHED', media_info[0])
# print('NOT MATCHED', media_info[1])

# with open('matched.csv', 'w', newline='') as csvfile:
#     fieldnames = media_info[0][0].keys()
#     writer = csv.DictWriter(csvfile, fieldnames=fieldnames) 
#     writer.writeheader()
#     writer.writerows(media_info[0])


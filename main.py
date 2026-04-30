"""
Main entry point for the Local Media Scanner.
"""

import argparse
import time
import unicodedata
import os
from tmdb import test_connection, search_tmdb
from utils import get_folders, clean_folder_name, get_genre, save_to_csv

def process_folders(folders, media_type):
    """ Loops through folders, cleans each name, calls search_tmdb(), and returns two lists: matched and unmatched """
    matched = []
    unmatched = []

    # for folder in folders:
    total = len(folders)
    for i, folder in enumerate(folders, start=1): # enumerate() gives both the index and the item at the same time
        print(f"Scanning {i}/{total}: {folder.name}") # printing the current folder being scanned
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
        

def confirm_save(cleaned_matched, unmatched):
    """ Ask the user to confirm before saving matched and unmatched results to CSV files. Checks if files already exist to avoid accidental overwriting. """
    confirm = input(f'Do you want to save the results? \nIt will be saved as "matched.csv" and "unmatched.csv". \nTo confirm press "Enter", to quit "q": ')
    saved = False
    
    if confirm == '':
        if os.path.exists('matched.csv'):
            overwrite = input(f'The "matched.csv" already exists. Press "Enter" to overwrite or "q" to quit: ')
            if overwrite != 'q':
                save_to_csv(cleaned_matched, 'matched.csv')  # save on overwrite confirmation
                saved = True
        else:
            save_to_csv(cleaned_matched, 'matched.csv')  # save when file doesn't exist
            saved = True

        if os.path.exists('unmatched.csv'):
            overwrite = input(f'The "unmatched.csv" already exists. Press "Enter" to overwrite or "q" to quit: ')
            if overwrite != 'q':
                save_to_csv(unmatched, 'unmatched.csv')
                saved = True
        else:
            save_to_csv(unmatched, 'unmatched.csv')
            saved = True
    else:
        print('Save cancelled.')
        return

    if saved:
        print('💾 The results were saved.')
    else:
        print('Nothing was saved.')


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
cleaned_matched = prepare_data(matched, media_type)

print("-" * 50)
print(f"Scan complete.")
print(f"  Matched:   {len(matched)}")
print(f"  Unmatched: {len(unmatched)}")
print(f"  Total:     {len(matched) + len(unmatched)}")
print("-" * 50)

confirm_save(cleaned_matched, unmatched)

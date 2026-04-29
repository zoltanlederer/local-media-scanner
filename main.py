"""
Main entry point for the Local Media Scanner.
"""

import argparse
import time
from tmdb import test_connection, search_tmdb
from utils import get_folders, clean_folder_name

parser = argparse.ArgumentParser(description='Scan local media files')
parser.add_argument('-f', '--folder', help='Select a folder for the scan')
parser.add_argument('-m', '--media-type', choices=['movie', 'tv'], help='Select the type of media: "movie" or "tv" for tv show.')
args = parser.parse_args()
root_folder = args.folder
media_type = args.media_type

# test_connection()

def process_folders(folders, media_type):
    """ Loops through folders, cleans each name, calls search_tmdb(), and returns two lists: matched and unmatched """
    matched = []
    unmatched = []

    for folder in folders:
        clean_folder = clean_folder_name(folder.name)
        time.sleep(0.25) # wait 250ms between calls
        results = search_tmdb(title=clean_folder['title'], year=clean_folder['year'], media_type=media_type)
        if results['results']:
            # print(results['results'][0], '\n')
            matched.append(results['results'][0])
        else:
            # print(clean_folder, '\n')
            unmatched.append(clean_folder)
    # return {'matched': matched, 'unmatched': unmatched}
    return matched, unmatched

# data = search_tmdb(title="The Dark Knight", media_type='movie', year='2008')
# print(data)

folders = get_folders(root_folder)
# print(folders)

# for folder in folders:
#     result = clean_folder_name(folder.name)
#     print(result)


media_info = process_folders(folders, media_type)

print(media_info)
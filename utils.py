"""
Folder walking and name cleaning
"""

import re
import csv
from pathlib import Path
from config import IGNORED_FOLDERS, MOVIE_GENRES, TV_GENRES

def get_folders(root_folder):
    """
    Walk through all subfolders recursively, skip anything in the
    IGNORED_FOLDERS list and season folders detected via regex,
    and return a list of folder paths to process.
    """
    folders = []
    for folder in Path(root_folder).rglob('*'):
        # Season folders (e.g. "Season 01", "Season 01 (2010–11)", "S01") are filtered here via regex, not in IGNORED_FOLDERS
        if (folder.is_dir() 
            and folder.name.lower() not in [f.lower() for f in IGNORED_FOLDERS]
            and not re.match(r'^Season\s*\d*', folder.name, re.IGNORECASE)
            and not re.match(r'^S\d{2}$', folder.name, re.IGNORECASE)):
                folders.append(folder)

    return folders


def clean_folder_name(folder_name):
    """ Clean up a messy folder name and return a dictionary with title and year """

    folder = re.sub(r'^\d{1,3}\s*[-\s]\s*', '', folder_name) # strip number prefixes like 01, 09 - from the start. Matches 1 to 3 digits at the start, optionally followed by space, hyphen, space
    year = re.search(r'\b\d{4}\b', folder) # find any 4-digit number
  
    if year and (1910 <= int(year.group()) <= 2090): # Check if it is a year
        if year.start() == 0: # If the year is at the start, extract the title from after it
            title = folder[year.end():] # (everything after the year) keep only the string from the end index of the year until the end of the string
            second_year = re.search(r'\b\d{4}\b', title) # checking if there is a year in the string again
            if second_year: # cut title at the second year to remove remaining junk
                title = title[:second_year.start()] # then keep the string from the beginning until the first index of the year
        else:
            title = folder[:year.start()] # keep the string from the beginning until the first index of the year
        year = year.group() # extract the matched year string from the match object
    else:
        title = folder
        year = None

    quality_markers = re.search(r'1080p|720p|480p|2160p|4K|3D', title) # find quality markers like 1080p — everything from this point onwards is junk
    if quality_markers:
        title = title[:quality_markers.start()] # keep the string from the beginning until the first index of the quality marker

    title = title.replace('.', ' ') # replace dots with spaces
    title = title.strip('- ()') # strip leading/trailing junk characters
    title = title.strip() # strip any remaining whitespace

    return {'title': title, 'year': year}


def get_genre(genres, media_type):
    """ Loop through the list of IDs, look each one up in the genre dictionary, and join the results into a string """
    
    if media_type == 'movie':
        genre_list = MOVIE_GENRES
    elif media_type == 'tv':
        genre_list = TV_GENRES
    else:
        return ''

    genre_names = []

    for genre in genres:
        genre_names.append(genre_list.get(genre, 'Unknown')) # if TMDB returns an ID that we don't have in genre_list, it will return "Unknown"

    return ', ' .join(genre_names)


def save_to_csv(data, filename):
    """ Save a list of dictionaries to a CSV file. Handles permission and OS errors gracefully. """
    try:
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = data[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames) 
            writer.writeheader()
            writer.writerows(data)
    except PermissionError:
        print(f'Permission denied. Could not write to "{filename}".')
    except OSError as error:
        print(f'Could not create file: {error}')
    except Exception:
        print('Something went wrong while writing the file.')
"""
Handling TMDB API calls
"""

import requests
from config import TMDB_API_KEY

def test_connection():
    """ Test the TMDB API connection and print the result. """
    url = "https://api.themoviedb.org/3/configuration"

    try:
        response = requests.get(url, params={"api_key": TMDB_API_KEY})
        if response.status_code == 200:
            print('The connection was successful.')
        else:
            print('Connection was not successful.')    
    except requests.exceptions.RequestException as error: 
        print(f"Something went wrong: {error}")


def search_tmdb(title, media_type, year=''):
    """ Search TMDB for a movie or TV show by title and optional year. Returns a dictionary or None. """
    base_url = 'https://api.themoviedb.org/3/search/'   
    try:
        response = requests.get(base_url + media_type, params={"api_key": TMDB_API_KEY, "query": title, "year": year})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as error: 
        print(f"Something went wrong: {error}")
        return None

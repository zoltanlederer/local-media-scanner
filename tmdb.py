"""
Handling TMDB API calls
"""

import requests
from config import TMDB_API_KEY

def test_connection():
    """ Test API Connection """
    url = "https://api.themoviedb.org/3/configuration"

    try:
        response = requests.get(url, params={"api_key": TMDB_API_KEY})
        if response.status_code == 200:
            print('The connection was successful.')
        else:
            print('Connection was not successful.')    
    except requests.exceptions.RequestException as error: 
        print(f"Something went wrong: {error}")

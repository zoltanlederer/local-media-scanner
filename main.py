"""
Main entry point for the Local Media Scanner.
"""

from tmdb import test_connection, search_tmdb

# test_connection()

data = search_tmdb(title="The Dark Knight", media_type='movie', year='2008')
print(data)

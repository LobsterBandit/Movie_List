import os
import json
import requests
import requests_cache

from config import BASEDIR, JSONFILE, APIURL, APIKEY, HEADERS, CACHELOC


def enable_cache(cache_loc=CACHELOC, backend='sqlite', expire=432000):
    """
    Enables caching of get requests.
        - Cache file defaults to CACHELOC from config.py
        - Backend defaults to sqlite.
        - Expiration default of 432,000 seconds (5 days).
    """
    requests_cache.install_cache(cache_loc, backend=backend, expire_after=expire)


def input_movies(base_dir=BASEDIR, file=JSONFILE):
    """
    Reads in JSON file containing movie data structured as a list of dictionaries
        - dir defaults to base directory of config.py
        - file defaults to JSONFILE from config.py
    :return: movies (list of dicts each containing movie data)
    """
    json_file = os.path.join(base_dir, file)
    with open(json_file, 'r') as f:
        movies = json.load(f)

    return movies


if __name__ == '__main__':
    enable_cache()
    movies = input_movies()
    print(movies)

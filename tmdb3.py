import os
import time
import json
import pprint

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


def search_movie_with_year(request_list, api_key, headers, api_url):
    """
    Request movie data based on title AND year returned in JSON format

    TMDb allows a max of 40 requests per 10 seconds.
    Build in some sort of caching mechanism...
    Temp fix: sleep after 40 requests for 10 seconds then continue looping.

    Initial search only returns some parameters.
    Have to get movie page a second time by TMDb id to retrieve append_to_response parameters.
    ie: reviews, trailers, imdb_id, etc.

    base_url = 'https://www.themoviedb.org/movie/'
    """
    for movie in request_list:
        title = movie['title']
        year = movie['year']
        payload = {
            'query': {title},
            'year': {year},
        }
        search_url = '{url}search/movie?api_key={key}'.format(url=api_url, key=api_key)
        try:
            search_req = requests.get(search_url, headers=headers, params=payload)

            if not search_req.from_cache:
                remain = search_req.headers['X-RateLimit-Remaining']
                print(search_req.headers)
                print(remain)
            else:
                remain = None

            search_result = search_req.json()

            if search_result['results']:
                if search_result['results'][0]['id']:
                    movie.update(tmdb_id=search_result['results'][0]['id'])
                else:
                    movie.update(tmdb_id=None)
                if search_result['results'][0]['overview']:
                    movie.update(Overview=search_result['results'][0]['overview'])
                else:
                    movie.update(Overview=None)
            else:
                movie.update(tmdb_id=None, Overview=None)

        except KeyError as k:
            print(k)
            if remain is not None:
                if remain == '0':
                    print('0 requests left.  Sleeping for 10 seconds.')
                    time.sleep(10)
        finally:
            if remain is not None:
                if remain == '0':
                    print('0 requests left.  Sleeping for 10 seconds.')
                    time.sleep(10)

    return request_list


def append_response(request_list, api_key, headers, api_url):
    """
    Retrieve additional movie data based on TMDb ID

    ie: external_ids, similar, reviews, videos, credits
    """
    req_resp = {}
    search_type = 'movie'
    payload = {
        'append_to_response': 'videos'
    }
    for movie in request_list:
        try:
            tmdb_id = movie['tmdb_id']
            search_pattern = '{0}{1}/{2}?api_key={3}'.format(api_url, search_type, tmdb_id, api_key)
            search_req = requests.get(search_pattern, headers=headers, params=payload)
            if not search_req.from_cache:
                remain = search_req.headers['X-RateLimit-Remaining']
                print(remain)
            else:
                remain = None

            search_result = search_req.json()

            movie_keys = ['imdb_id', 'vote_average', 'runtime', 'poster_path',
                          'backdrop_path', 'release_date', 'tagline']

            for key in movie_keys:
                if key in search_result.keys():
                    result = search_result[key]
                else:
                    result = None
                movie[key] = result

        except KeyError as k:
            print(k)
            print('The offending movie is: {}'.format(movie[0]))
            if remain is not None:
                if remain == '0':
                    print('0 requests left.  Sleeping for 10 seconds.')
                    time.sleep(10)
        finally:
            title = movie['title']
            req_resp[title] = search_result
            if remain is not None:
                if remain == '0':
                    print('0 requests left.  Sleeping for 10 seconds.')
                    time.sleep(10)

    return request_list, req_resp


if __name__ == '__main__':
    enable_cache()
    pp = pprint.PrettyPrinter(indent=4)
    movies = input_movies()
    mlist = search_movie_with_year(movies[:3], APIKEY, HEADERS, APIURL)
    # pp.pprint(mlist)
    final_list, responses = append_response(mlist, APIKEY, HEADERS, APIURL)
    pp.pprint(final_list)
    # pp.pprint(responses)



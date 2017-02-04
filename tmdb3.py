import time

import requests
import requests_cache

from movies import file_details
from update_db import upsert_db
from config import SEARCHDIRS, EXTENSIONS, APIURL, APIKEY, HEADERS, CACHELOC, DATABASE


def enable_cache(cache_loc=CACHELOC, backend='sqlite', expire=432000):
    """
    Enables caching of get requests.
        - Cache file defaults to CACHELOC from config.py
        - Backend defaults to sqlite.
        - Expiration default of 432,000 seconds (5 days).
    """
    requests_cache.install_cache(cache_loc, backend=backend, expire_after=expire)


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
        stime = 0
        try:
            search_req = requests.get(search_url, headers=headers, params=payload)

            if not search_req.from_cache:
                remain = search_req.headers['X-RateLimit-Remaining']
                print(remain)
            else:
                remain = None

            if remain == '39':
                stime = time.time()
                print(stime)

            search_result = search_req.json()

            if search_result['results']:
                if search_result['results'][0]['id']:
                    movie.update(tmdb_id=search_result['results'][0]['id'])
                else:
                    movie.update(tmdb_id=None)
                if search_result['results'][0]['overview']:
                    movie.update(overview=search_result['results'][0]['overview'])
                else:
                    movie.update(overview=None)
            else:
                movie.update(tmdb_id=None, overview=None)

        except KeyError as k:
            print(k)
            if remain is not None and remain == '0':
                etime = time.time()
                delta = etime - stime
                if delta < 10:
                    sleep = 11 - delta
                    print('0 requests left.  Sleeping for {} seconds.'.format(sleep))
                    time.sleep(sleep)
        finally:
            if remain is not None and remain == '0':
                etime = time.time()
                if stime is not None:
                    delta = etime - stime
                else:
                    delta = 0
                if delta < 10:
                    sleep = 11 - delta
                    print('0 requests left.  Sleeping for {} seconds.'.format(sleep))
                    time.sleep(sleep)

    return request_list, stime


def append_response(request_list, api_key, headers, api_url, startingtime, response=False):
    """
    Retrieve additional movie data based on TMDb ID

    ie: external_ids, similar, reviews, videos, credits
    """
    req_resp = {}
    search_type = 'movie'
    payload = {
        'append_to_response': 'videos'
    }
    starttime = startingtime
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

            if remain == '39':
                starttime = time.time()
                print(starttime)

            search_result = search_req.json()

            movie_keys = ['imdb_id', 'vote_average', 'runtime', 'poster_path',
                          'backdrop_path', 'release_date', 'tagline', 'genres']

            for key in movie_keys:
                if key in search_result.keys():
                    if key == 'genres':
                        genres = ','.join(i['name'] for i in search_result[key])
                        result = genres
                        # print(genres)
                    else:
                        result = search_result[key]
                else:
                    result = None
                movie[key] = result
            print(movie['genres'])
        except KeyError as k:
            print(k)
            print('The offending movie is: {}'.format(movie['filename']))
            if remain is not None and remain == '0':
                endtime = time.time()
                delta = endtime - starttime
                if delta < 10:
                    sleep = 11 - delta
                    print('0 requests left.  Sleeping for {} seconds.'.format(sleep))
                    time.sleep(sleep)
        finally:
            title = movie['title']
            req_resp[title] = search_result
            if remain is not None and remain == '0':
                endtime = time.time()
                if starttime is not None:
                    delta = endtime - starttime
                else:
                    delta = 0
                if delta < 10:
                    sleep = 11 - delta
                    print('0 requests left.  Sleeping for {} seconds.'.format(sleep))
                    time.sleep(sleep)

    return request_list

if __name__ == '__main__':
    enable_cache(expire=1296000)
    movies = file_details(SEARCHDIRS, EXTENSIONS)
    mlist, stime = search_movie_with_year(movies, APIKEY, HEADERS, APIURL)
    final_list = append_response(mlist, APIKEY, HEADERS, APIURL, stime)
    upsert_db(final_list, DATABASE)

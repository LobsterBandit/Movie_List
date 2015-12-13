import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))

SEARCHDIRS = ['E:\\1080p',
              'E:\\720p',
              'E:\\3D',
              'E:\\DvD.BRRip.R5',
              'I:\\3D',
              'T:\\720p',
              'T:\\1080p Movies',
              'X:\\1080p',
              'X:\\720p',
              'X:\\3D',
              'V:\\High Def\\Movies\\1080p2']
EXTENSIONS = ('.mkv', '.avi', '.mp4', '.iso', '.wmv')
JSONFILE = 'Movies.txt'

# database information
DBNAME = 'Movie_DB.db'
DATABASE = os.path.join(BASEDIR, DBNAME)

# TMDb api information
APIURL = 'https://api.themoviedb.org/3/'
APIKEY = os.environ['TMDBAPIKEY']
HEADERS = {
    'Accept': 'application/json'
}

# requests cache
CACHENAME = 'tmdb_cache'
CACHELOC = os.path.join(BASEDIR, CACHENAME)

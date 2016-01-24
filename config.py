import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))

SEARCHDIRS = ['E:\\1080p',
              'E:\\720p',
              'E:\\3D',
              'E:\\DvD.BRRip.R5',
              # 'F:\\',
              'I:\\3D',
              'T:\\720p',
              'T:\\1080p Movies',
              'W:\\',
              'X:\\1080p',
              'X:\\720p',
              'X:\\3D',
              'V:\\High Def\\Movies\\1080p2']

DRIVES = ['C:',
          'D:',
          'E:',
          'F:',
          'I:',
          'T:',
          'W:',
          'X:',
          'V:']


EXTENSIONS = ('.mkv', '.avi', '.mp4', '.iso', '.wmv')
JSONFILE = os.path.join(BASEDIR, 'Movies.txt')
SPACEFILE = os.path.join(BASEDIR, 'Drive_Usage.txt')

# database information
DBNAME = 'Movie_DB.db'
DATABASE = os.path.join(BASEDIR, DBNAME)
# database migration
FRESH_PATH = r'C:\Users\Darin\PythonProjects\Movie_List'
FRESHDB = os.path.join(FRESH_PATH, DBNAME)
APP_PATH = r'C:\Users\Darin\Movie_App\Movie_DB_App'
APPDB = os.path.join(APP_PATH, DBNAME)

# TMDb api information
CONFIG_PATTERN = 'https://api.themoviedb.org/3/configuration?api_key={key}'
IMG_PATTERN = 'https://api.themoviedb.org/3/movie/{tmdbid}/images?api_key={key}'
APIURL = 'https://api.themoviedb.org/3/'
APIKEY = os.environ['TMDBAPIKEY']
HEADERS = {
    'Accept': 'application/json'
}

# requests cache
CACHENAME = 'tmdb_cache'
CACHELOC = os.path.join(BASEDIR, CACHENAME)

# movie app static image location
APPIMG = r'C:\Users\Darin\Movie_App\Movie_DB_App\app\static\images'

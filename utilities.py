import shutil
from config import FRESHDB, APPDB


def copy_db(src=FRESHDB, dst=APPDB):
    """ Copy most updated DB from Movie_List directory to the flask app directory
        :param src: accepts string value of fully qualified file path
        :param dst: accepts string value of either fully qualified destination path and filename
                    or just directory path.  filename will be maintained if only path supplied.
    """
    try:
        shutil.copy2(src, dst)
    except shutil.SameFileError as e:
        print('Both source and destination files are identical.')
        print('No copy necessary.')


if __name__ == '__main__':
    copy_db()
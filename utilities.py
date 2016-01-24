import shutil
from config import FRESHDB, APPDB


def copy_db(src=FRESHDB, dst=APPDB):
    """ Copy most updated DB from Movie_List directory to the flask app directory
        :param src: accepts string value of fully qualified file path
        :param dst: accepts string value of either fully qualified destination path and filename
                    or just directory path.  filename will be maintained if only path supplied.
    """
    try:
        x = shutil.copy2(src, dst)
        print('File copied to {}.'.format(x))
    except shutil.SameFileError as e:
        print('Both source and destination are identical.')


if __name__ == '__main__':
    copy_db()

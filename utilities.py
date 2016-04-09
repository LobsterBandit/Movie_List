import shutil
import os
from datetime import datetime
from config import FRESHDB, APPDB, BACKUPDB


def copy_db(src=FRESHDB, dst=[APPDB]):
    """
    Copy most updated DB from Movie_List directory to the flask app directory
    :param src: accepts string value of fully qualified file path
    :param dst: accepts list of strings of either fully qualified destination path and filename
                or just directory path.  filename will be maintained if only path supplied.
    """
    for dest in dst:
        try:
            x = shutil.copy2(src, dest)
            print('File copied to {}'.format(x))
        except shutil.SameFileError:
            print('Both source and destination are identical.')


def backup_db(src=APPDB, dst=BACKUPDB, append_date=False):
    """
    :param append_date:
    :param src: accepts string value of fully qualified file path.  Defaults to flask app's Movie_DB.db
    :param dst: accepts string value of either fully qualified destination path and filename
                or just directory path.  Filename maintained if only path supplied.  Defaults to DB Backups/
                directory in flask app.
    """
    try:
        if append_date is True:
            filename, ext = os.path.splitext(dst)
            head, tail = os.path.split(filename)
            newfile = '{file}_{date}{ext}'.format(file=tail, date=datetime.now().strftime('%Y%m%d_%H%M%S'), ext=ext)
            dst = os.path.join(head, newfile)
            x = shutil.copy2(src, dst)
            print('File backed up to {}'.format(x))
        else:
            x = shutil.copy2(src, dst)
            print('File backed up to {}'.format(x))
    except shutil.SameFileError as e:
        print('Both source and destination are identical.')


if __name__ == '__main__':
    backup_db(append_date=True)
    # copy_db()
    # copy_db(dst=r'E:\Movie_DB.db')
    # copy_db(dst=r'D:\Libraries\Documents\Visual Studio Projects\MovieApi\MovieApi\Movie_DB.db')
    # copy_db(dst=r'C:\inetpub\wwwroot\MovieApi\Movie_DB.db')
    copy_db(dst=[APPDB,
                 r'E:\Movie_DB.db',
                 r'D:\Libraries\Documents\Visual Studio Projects\MovieApi\MovieApi\Movie_DB.db',
                 r'C:\inetpub\wwwroot\MovieApi\Movie_DB.db'])

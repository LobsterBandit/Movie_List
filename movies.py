import os
import re

from config import SEARCHDIRS, EXTENSIONS


def file_details(locations, extensions):
    """
    Walk through given directory and create a list of lists containing for each file:
        - filename
        - root directory
        - file size
        - title (from regex of filename)
        - year (from regex of filename)
    :rtype : list
    """
    mlist = []

    for x in locations:
        # skips path in location[] if not a valid directory
        # ie: external hdd is not connected or network drive unavailable (VNC path)
        if not os.path.isdir(x):
            continue
            
        for root, dirs, files in os.walk(x):
            for mfile in files:
                if mfile.endswith(extensions):
                    pt = os.path.join(root, mfile)

                    # Check file attributes using os.stat
                    # 0x2 signifies hidden flag per Windows API
                    # https://msdn.microsoft.com/en-us/library/windows/desktop/gg258117.aspx
                    # if file attributes exist and hidden flag is set, skip file
                    attribute = os.stat(pt).st_file_attributes
                    if attribute & 0x2:
                        break

                    # size in bytes
                    st = os.stat(pt).st_size

                    if mfile.find(',') != -1:
                        mfile = mfile.replace(',', '')

                    title, year = title_year(mfile)

                    mlist.append([mfile, st, root, title, year])
    return mlist


def title_year(m_file):
    """
    Regex searching returns the title and year from the filename

    Currently optimized for: "Title (year).extension"
    """
    name = re.compile(r'([\w+\W?]+)\s\(([0-9]{4})\)[\s\w*]*\.\w{2,4}')

    fsearch = name.search(m_file)
    if fsearch:
        title = fsearch.group(1)
        year = fsearch.group(2)
    else:
        print('No match for {}'.format(m_file))
        title = None
        year = None

    return title, year


if __name__ == "__main__":
    """
    Create a list of movies in the provided location.
    Includes filename, size, root, movie title, movie year.
    """
    locations = SEARCHDIRS
    extensions = EXTENSIONS

    mlist = file_details(locations, extensions)
    print(mlist)

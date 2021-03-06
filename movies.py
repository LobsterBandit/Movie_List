import os
import re
import json

from config import SEARCHDIRS, EXTENSIONS, JSONFILE


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

                    mlist.append(dict(filename=mfile,
                                      size=st,
                                      root=root,
                                      title=title,
                                      year=year
                                      )
                                 )

    return mlist


def title_year(m_file):
    """
    Regex searching returns the title and year from the filename

    Currently optimized for: "Title (year).extension"
    """
    name = re.compile(r'([\w+\W?]+)\s\(([0-9]{4})\)[\s\w]*[\d\.\d]*[\s\w]*\.\w{2,4}')

    fsearch = name.search(m_file)
    if fsearch:
        title = fsearch.group(1)
        year = fsearch.group(2)
    else:
        print('No match for {}'.format(m_file))
        title = None
        year = None

    return title, year


def json_output(result, json_file=JSONFILE):
    """
    Output 'result' as JSON to the specified file
        - filename defaults to that supplied by config.py
    """
    with open(json_file, 'w') as f:
        json.dump(result, f, indent=4)
    print('Query output created at {}'.format(json_file))


if __name__ == "__main__":
    """
    Create a list of movies in the provided location.
    Includes filename, size, root, movie title, movie year.
    """
    locations = SEARCHDIRS
    extensions = EXTENSIONS

    mlist = file_details(locations, extensions)
    json_output(mlist)

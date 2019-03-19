__all__ = ['station', 'update', 'stationlist', 'metadata']


def station(ident, directory):
    """ Download IGRAv2 Station from NOAA

    Args:
        ident (str): IGRA ID
        directory (str): output directory

    """
    import urllib
    import os
    from .support import message
    os.makedirs(directory, exist_ok=True)
    url = "ftp://ftp.ncdc.noaa.gov/pub/data/igra/data/data-por/%s-data.txt.zip" % ident
    message(url, ' to ', directory + '/%s-data.txt.zip' % ident, verbose=1)

    urllib.request.urlretrieve(url, directory + '/%s-data.txt.zip' % ident)

    if os.path.isfile(directory + '/%s-data.txt.zip' % ident):
        message("Downloaded: ", directory + '/%s-data.txt.zip' % ident, verbose=1)
    else:
        message("File not found: ", directory + '/%s-data.txt.zip' % ident, verbose=1)


def update(ident, directory, year='2019'):
    import urllib
    import os
    from .support import message
    os.makedirs(directory, exist_ok=True)
    url = "ftp://ftp.ncdc.noaa.gov/pub/data/igra/data/data-y2d/%s-data-beg%s.txt.zip" % (ident, year)
    message(url, ' to ', directory + '/%s-data-beg%s.txt.zip' % (ident, year), verbose=1)
    urllib.request.urlretrieve(url, directory + '/%s-data-beg%s.txt.zip' % (ident, year))

    if os.path.isfile(directory + '/%s-data-beg%s.txt.zip' % (ident, year)):
        message("Downloaded: ", directory + '/%s-data-beg%s.txt.zip' % (ident, year), verbose=1)
    else:
        message("File not found: ", directory + '/%s-data-beg%s.txt.zip' % (ident, year), verbose=1)


def stationlist(directory):
    import urllib
    import os
    from .support import message
    os.makedirs(directory, exist_ok=True)
    urllib.request.urlretrieve("ftp://ftp.ncdc.noaa.gov/pub/data/igra/igra2-station-stationlist.txt",
                               filename=directory + '/igra2-station-stationlist.txt')

    if os.path.isfile(directory + '/igra2-station-stationlist.txt'):
        message("Download complete, reading table ...")
        return _igralist(directory + '/igra2-station-stationlist.txt')
    else:
        message("File not found: ", directory + '/igra2-station-stationlist.txt', verbose=1)


def metadata(directory):
    import urllib
    import os
    from .support import message
    os.makedirs(directory, exist_ok=True)
    urllib.request.urlretrieve("ftp://ftp.ncdc.noaa.gov/pub/data/igra/history/igra2-_metadata.txt",
                               filename=directory + '/igra2-_metadata.txt')

    if not os.path.isfile(directory + '/igra2-_metadata.txt'):
        message("File not found: ", directory + '/igra2-_metadata.txt', verbose=1)
    else:
        message("Downloaded: ", directory + '/igra2-_metadata.txt', verbose=1)


def _igralist(filename):
    """Read IGRA Radiosondelist

    or download

    Parameters
    ----------
    new         bool
    filename    str
    verbose     int

    Returns
    -------
    DataFrame
    """
    import numpy as np
    import pandas as pd

    try:
        infile = open(filename)
        tmp = infile.read()
        data = tmp.splitlines()

    except IOError as e:
        print("File not found: " + filename)
        raise e
    else:
        infile.close()

    out = pd.DataFrame(columns=['id', 'wmo', 'lat', 'lon', 'alt', 'state', 'name', 'start', 'end', 'total'])

    for i, line in enumerate(data):
        id = line[0:11]

        try:
            id2 = "%06d" % int(line[5:11])  # substring

        except:
            id2 = ""

        lat = float(line[12:20])
        lon = float(line[21:30])
        alt = float(line[31:37])
        state = line[38:40]
        name = line[41:71]
        start = int(line[72:76])
        end = int(line[77:81])
        count = int(line[82:88])
        out.loc[i] = (id, id2, lat, lon, alt, state, name, start, end, count)

    out.loc[out.lon <= -998.8, 'lon'] = np.nan  # repalce missing values
    out.loc[out.alt <= -998.8, 'alt'] = np.nan  # repalce missing values
    out.loc[out.lat <= -98.8, 'lat'] = np.nan  # replace missing values
    out['name'] = out.name.str.strip()
    out = out.set_index('id')
    return out


def uadb(ident, directory, email, pwd, **kwargs):
    """ Download UADB TRHC Station from UCAR

    Args:
        ident (str): WMO ID
        directory (str): output directory

    """
    import requests
    import os
    from .support import message

    os.makedirs(directory, exist_ok=True)
    ident = str(int(ident))  # remove 00

    url = 'https://rda.ucar.edu/cgi-bin/login'
    values = {'email': email, 'passwd': pwd, 'action': 'login'}
    # Authenticate
    ret = requests.post(url, data=values)
    if ret.status_code != 200:
        print('Bad Authentication')
        print(ret.text)
        exit(1)

    fileurl = "http://rda.ucar.edu/data/ds370.1/uadb_trhc_%s.txt" % ident
    message(url, ' to ', directory + '/uadb_trhc_%s.txt' % ident, verbose=1)
    try:
        req = requests.get(fileurl, cookies=ret.cookies, allow_redirects=True, stream=True)
        filesize = int(req.headers['Content-length'])
        with open(directory + '/uadb_trhc_%s.txt' % ident, 'wb') as outfile:
            chunk_size = 1048576
            for chunk in req.iter_content(chunk_size=chunk_size):
                outfile.write(chunk)
                if chunk_size < filesize:
                    _check_file_status(directory + '/uadb_trhc_%s.txt' % ident, filesize)

        _check_file_status(directory + '/uadb_trhc_%s.txt' % ident, filesize)
    except Exception as e:
        print("Error: ", repr(e))
        if kwargs.get('debug', False):
            raise e
        return

    if os.path.isfile(directory + '/uadb_trhc_%s.txt' % ident):
        message("\nDownloaded: ", directory + '/uadb_trhc_%s.txt' % ident, verbose=1)
    else:
        message("\nFile not found: ", directory + '/uadb_trhc_%s.txt' % ident, verbose=1)


def _check_file_status(filepath, filesize):
    import sys, os
    sys.stdout.write('\r')
    sys.stdout.flush()
    size = int(os.stat(filepath).st_size)
    percent_complete = (size / filesize) * 100
    sys.stdout.write('%.3f %s' % (percent_complete, '% Completed'))
    sys.stdout.flush()

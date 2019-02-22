__all__ = ['station', 'update', 'list', 'metadata']


def station(ident, directory):
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


def update(ident, directory):
    import urllib
    import os
    from .support import message
    os.makedirs(directory, exist_ok=True)
    # todo add wildcard for beg2018 (probably every year, thus only at current year
    url = "ftp://ftp.ncdc.noaa.gov/pub/data/igra/data/data-y2d/%s-data-beg2018.txt.zip" % ident
    message(url, ' to ', directory + '/%s-data-beg2018.txt.zip' % ident, verbose=1)
    urllib.request.urlretrieve(url, directory + '/%s-data-beg2018.txt.zip' % ident)

    if os.path.isfile(directory + '/%s-data-beg2018.txt.zip' % ident):
        message("Downloaded: ", directory + '/%s-data-beg2018.txt.zip' % ident, verbose=1)
    else:
        message("File not found: ", directory + '/%s-data-beg2018.txt.zip' % ident, verbose=1)


def list(directory):
    import urllib
    import os
    from .support import message
    os.makedirs(directory, exist_ok=True)
    urllib.request.urlretrieve("ftp://ftp.ncdc.noaa.gov/pub/data/igra/igra2-station-list.txt",
                               filename=directory + '/igra2-station-list.txt')

    if os.path.isfile(directory + '/igra2-station-list.txt'):
        message("Download complete, reading table ...")
        return _igralist(directory + '/igra2-station-list.txt')
    else:
        message("File not found: ", directory + '/igra2-station-list.txt', verbose=1)


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

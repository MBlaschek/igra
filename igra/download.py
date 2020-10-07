__all__ = ['station', 'update', 'stationlist', 'metadata']


def station(ident, directory, server=None, verbose=1):
    """ Download IGRAv2 Station from NOAA

    Args:
        ident (str): IGRA ID
        directory (str): output directory
        server (str): download url
        verbose (int): verboseness

    """
    import urllib
    import os
    from .support import message
    os.makedirs(directory, exist_ok=True)
    if server is None:
        server = 'https://www1.ncdc.noaa.gov/pub/data/igra/data/data-por/'
    url = "%s/%s-data.txt.zip" % (server, ident)
    message(url, ' to ', directory + '/%s-data.txt.zip' % ident, verbose=verbose)

    urllib.request.urlretrieve(url, directory + '/%s-data.txt.zip' % ident)

    if os.path.isfile(directory + '/%s-data.txt.zip' % ident):
        message("Downloaded: ", directory + '/%s-data.txt.zip' % ident, verbose=verbose)
    else:
        message("File not found: ", directory + '/%s-data.txt.zip' % ident, verbose=verbose)


def update(ident, directory, year='2018', verbose=1):
    """ Download an update from the IGRAv2 archive (data-2yd)
    Usually there is an updated file from the running year(e.g. 2019, then 2018 should be given)

    Args:
        ident (str): IGRA id
        directory (str): update directory
        year (str): year string
        verbose (int): verbosness

    """
    import urllib
    import os
    from .support import message
    os.makedirs(directory, exist_ok=True)
    url = "https://www1.ncdc.noaa.gov/pub/data/igra/data/data-y2d/%s-data-beg%s.txt.zip" % (ident, year)
    message(url, ' to ', directory + '/%s-data-beg%s.txt.zip' % (ident, year), verbose=verbose)
    urllib.request.urlretrieve(url, directory + '/%s-data-beg%s.txt.zip' % (ident, year))

    if os.path.isfile(directory + '/%s-data-beg%s.txt.zip' % (ident, year)):
        message("Downloaded: ", directory + '/%s-data-beg%s.txt.zip' % (ident, year), verbose=verbose)
    else:
        message("File not found: ", directory + '/%s-data-beg%s.txt.zip' % (ident, year), verbose=verbose)


def stationlist(directory, verbose=1):
    """ Download the IGRAv2 station list

    Args:
        directory (str): save directory for the raw list
        verbose (int): verbosness

    Returns:
        DataFrame : station informations
    """
    import urllib
    import os
    from .support import message
    from .read import stationlist as read_list
    os.makedirs(directory, exist_ok=True)
    urllib.request.urlretrieve("https://www1.ncdc.noaa.gov/pub/data/igra/igra2-station-list.txt",
                               filename=directory + '/igra2-station-list.txt')

    if os.path.isfile(directory + '/igra2-station-list.txt'):
        message("Download complete, reading table ...", verbose=verbose)
        return read_list(directory + '/igra2-station-list.txt', verbose=verbose)
    else:
        message("File not found: ", directory + '/igra2-station-list.txt', verbose=verbose)


def metadata(directory, verbose=1):
    """ Download IGRAv2 meta information on radiosonde changes

    Args:
        directory (str): save directory
        verbose (int): verboseness

    """
    import urllib
    import os
    from .support import message
    os.makedirs(directory, exist_ok=True)
    urllib.request.urlretrieve("https://www1.ncdc.noaa.gov/pub/data/igra/history/igra2-metadata.txt",
                               filename=directory + '/igra2-metadata.txt')

    if not os.path.isfile(directory + '/igra2-metadata.txt'):
        message("File not found: ", directory + '/igra2-metadata.txt', verbose=verbose)
    else:
        message("Downloaded: ", directory + '/igra2-metadata.txt', verbose=verbose)


def uadb(ident, directory, email, pwd, verbose=1, **kwargs):
    """ Download UADB TRHC Station from UCAR

    Args:
        ident (str): WMO ID
        directory (str): output directory
        email (str): email adress for UCAR account
        pwd (str): password for UCAR account
        verbose (int): verboseness
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
        message('Bad Authentication', verbose=verbose)
        message(ret.text, verbose=verbose)
        exit(1)

    fileurl = "http://rda.ucar.edu/data/ds370.1/uadb_trhc_%s.txt" % ident
    message(url, ' to ', directory + '/uadb_trhc_%s.txt' % ident, verbose=verbose)
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
        message("Error: ", repr(e), verbose=verbose)
        if kwargs.get('debug', False):
            raise e
        return

    if os.path.isfile(directory + '/uadb_trhc_%s.txt' % ident):
        message("\nDownloaded: ", directory + '/uadb_trhc_%s.txt' % ident, verbose=verbose)
    else:
        message("\nFile not found: ", directory + '/uadb_trhc_%s.txt' % ident, verbose=verbose)


def _check_file_status(filepath, filesize):
    """ UCAR method to check if download was complete

    Args:
        filepath:
        filesize:

    Returns:

    """
    import sys
    import os
    sys.stdout.write('\r')
    sys.stdout.flush()
    size = int(os.stat(filepath).st_size)
    percent_complete = (size / filesize) * 100
    sys.stdout.write('%.3f %s' % (percent_complete, '% Completed'))
    sys.stdout.flush()

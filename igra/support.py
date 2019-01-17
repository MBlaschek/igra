
__all__ = ['now', 'message']


def now():
    """ Datetime string

    Returns:
        str : datetime now
    """
    import datetime
    return datetime.datetime.now().isoformat()


def message(*args, mname=None, verbose=0, level=0, logfile=None, **kwargs):
    if logfile is not None:
        # with open(kwargs['filename'], 'a' if not kwargs.get('force', False) else 'w') as f:
        with open(logfile, 'a') as f:
            f.write(_print_string(*args, **kwargs) + "\n")

    elif verbose > level:
        text = _print_string(*args, **kwargs)
        if mname is not None:
            text = "[%s] " % mname + text

        print(text)
    else:
        pass


def _print_string(*args, adddate=False, **kwargs):
    if adddate:
        return "[" + now() + "] " + " ".join([str(i) for i in args])
    else:
        return " ".join([str(i) for i in args])

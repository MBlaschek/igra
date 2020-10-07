
__all__ = ['now', 'message', 'kw_handle']


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


def kw_handle(kw, update=False, **kwargs):
    for ikey, ival in kwargs.items():
        if ikey not in kw.keys():
            kw[ikey] = ival
        elif update:
            kw[ikey] = ival
        else:
            pass
    return kw

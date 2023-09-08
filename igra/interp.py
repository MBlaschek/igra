# -*- coding: utf-8 -*-


__all__ = ['dataframe']


def dataframe(data, level_column, levels=None, variables=None, keep_old_levels=True, **kwargs):
    """ Interpolate a database DataFrame according to pressure levels in level_column

    Interpolate:
    1. Select only levels with enough (min_levels) t and r values
    2. Interpolate each profile (date) vertically to levels

    Interpolation is only done at dates with enough Data

    Args:
        data (DataFrame):  Database with columns of non-uniform pressure levels
        level_column (str):  Database column with pressure levels
        levels (list, ndarray):  new pressure levels for interpolation
        variables (list): Variables to interpolate
        keep_old_levels (bool) : keep old levels in database ?

    Returns:
    DataFrame : interpolated DataFrame with new pressure levels
    """
    import pandas as pd
    from . import std_plevels
    from .support import message

    if not isinstance(data, pd.DataFrame):
        raise ValueError()

    if levels is None:
        levels = std_plevels

    data.index.name = 'date'

    if variables is not None:
        variables = list(set(variables + [level_column]))  # add p
        data = data.loc[:, data.columns.isin(variables)]
    # only use numeric columns
    data = data.select_dtypes(include=['number'])
    # Is there anything to work with?
    if len(data.columns.tolist()) < 2:
        raise ValueError("Requires at least 2 columns(%s,+) %s" % (level_column, ",".join(variables)))

    # Interpolate
    n = data.shape
    data = data.groupby('date').apply(table, level_column, levels)
    if not keep_old_levels:
        data = data.drop('flag_int', axis=1)

    # Change multi-index
    data = data.reset_index().drop('level_1', axis=1).sort_values(by=['date', level_column]).set_index('date',
                                                                                                       drop=True)
    m = data.shape
    message(n, ' >> ', m, **kwargs)
    return data


def table(data, level_column, levels):
    """ Wrapper Function for _np_profile to handle a DataFrame

    Args:
        data (DataFrame): Input DataFrame for a timestamp
        level_column (str): pressure level column
        levels (ndarray or list): new pressure levels

    Returns:
    DataFrame : new DataFrame with size of levels
    """
    import numpy as np
    import pandas as pd
    df = data.sort_values(level_column)
    pin = df[level_column].values
    #
    # Are there levels missing?
    #
    if np.in1d(pin, levels).sum() != np.size(levels):
        # df.drop(level_column, 1, inplace=True)   # slow
        #
        # Index of pressure
        #
        j = int(np.where(df.columns == level_column)[0])
        #
        # combine all levels
        #
        new_plevs = np.unique(np.sort(np.concatenate([pin, levels])))
        #
        # Iterate columns
        #
        data = np.full((new_plevs.size, df.shape[1] + 1), np.nan)
        for i in range(df.shape[1]):
            if i == j:
                data[:, i] = new_plevs
            else:
                data[:, i] = profile(df.values[:, i], pin, new_plevs)
        #
        # Fill in interpolation flag
        #
        data[:, -1] = np.where(np.in1d(new_plevs, pin), 0, 1)
        data = pd.DataFrame(data, columns=list(df.columns) + ['flag_int'])
        return data
    else:
        df['flag_int'] = 0
        # return df.reset_index().drop('date', 1)
        # Pandas API change, 2023
        return df.reset_index().drop('date', axis=1)
    


def profile(data, plevs, new_plevs):
    """ Modified np.interp Function for filtering NAN

    Args
    ----
        data : ndarray
            Input Data
        plevs : ndarray
            Input pressure levels
        new_plevs : ndarray
            Output pressure levels

    Returns
    -------
    ndarray
        size of new_plevs
    """
    import numpy as np
    data = np.squeeze(data)  # remove 1-dims
    ix = np.isfinite(data)  # only finite values
    s = ix.sum()  # enough data left ?
    if s > 2:
        # plevs, data = numpy.unique([plevs[ix], data[ix]], axis=1)   # slow 75%
        # Speed improvement
        plevs, data = plevs[ix], data[ix]
        plevs, ix = np.unique(plevs, return_index=True)
        data = data[ix]
        # End Improvement
        # todo add uncertainty from interpolation, due to spacing
        # summe der ableitung zum quadrat mal unsicherheit quadrat
        data = np.interp(np.log(new_plevs), np.log(plevs), data, left=np.nan, right=np.nan)
        return data

    return np.full_like(new_plevs, np.nan)  # Nothing to do, but keep shape
    
# ENDE

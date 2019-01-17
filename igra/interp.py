# -*- coding: utf-8 -*-


__all__ = ['dataframe']


def dataframe(data, level_column, levels=None, variables=None, min_levels=3, keep_old_levels=False, **kwargs):
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
        min_levels (int): minimum required levels per profile for interpolation
        keep_old_levels (bool) : keep old levels in database ?
        verbose (int): verbosness

    Returns:
    DataFrame : interpolated DataFrame with new pressure levels
    """
    import pandas as pd
    from . import message
    from .. import config

    if not isinstance(data, pd.DataFrame):
        raise ValueError()

    if levels is None:
        levels = config.std_plevels

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
    data = data.groupby(data.index).apply(table, level_column, levels, min_levels=min_levels,
                                          keep=keep_old_levels)
    # Change multi-index
    data = data.reset_index().drop('level_1', axis=1).sort_values(by=['date', level_column]).set_index('date',
                                                                                                       drop=True)
    m = data.shape
    message(n, ' >> ', m, **kwargs)
    return data


def table(data, level_column, levels, min_levels=3, keep=False):
    """ Wrapper Function for _np_profile to handle a DataFrame

    Args:
        data (DataFrame): Input DataFrame for a timestamp
        level_column (str): pressure level column
        levels (ndarray or list): new pressure levels
        min_levels (int): minimum required pressure levels
        keep (bool): keep old pressure levels

    Returns:
    DataFrame : new DataFrame with size of levels
    """
    import numpy as np
    import pandas as pd

    # data = data.iloc[np.unique(data[level_column], return_index=True)[1], :]   # subset
    data = data.sort_values(level_column)   # no subset
    pin = data[level_column].values
    data.drop(level_column, 1, inplace=True)
    if (data.count() > min_levels).sum() == 0:
        return  # removes too small groups

    names = data.columns.tolist()
    if keep:
        alllevels = np.unique(np.sort(np.concatenate([pin, levels])))
        # 0 RAW, 1 Both, 2 NEW
        orig = np.where(np.in1d(alllevels, levels), 2, 1) - np.where(np.in1d(alllevels, pin), 1, 0)
        levels = alllevels

    data = np.apply_along_axis(profile, 0, data.values, pin, levels)
    data = pd.DataFrame(data, columns=names)
    data[level_column] = levels
    if keep:
        data['orig'] = orig
    return data


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
    # data.groupby(pressure).mean()  # remove duplicates with slightly different values
    data = np.squeeze(data)  # remove 1-dims
    ix = np.isfinite(data)  # only finite values
    s = ix.sum()  # enough data left ?
    if s > 0:
        #if s > min_levels:
        plevs, data = np.unique([plevs[ix], data[ix]], axis=1)
        # todo add uncertainty from interpolation, due to spacing
        # summe der ableitung zum quadrat mal unsicherheit quadrat
        data = np.interp(np.log(new_plevs), np.log(plevs), data, left=np.nan, right=np.nan)
        return data
        # jx = np.in1d(plevs[ix], new_plevs)  # index of finite values
        # if len(jx) > 0:
        #     kx = np.in1d(new_plevs, plevs[ix])  # index of finite values in new pressure levels
        #     out = np.full_like(new_plevs, np.nan)
        #     out[kx] = data[ix][jx]
        #     return out  # just a few values
    return np.full_like(new_plevs, np.nan)  # Nothing to do, but keep shape

#
# def interp_profile(data, plevs, new_plevs, min_levels=3):
#     """ Modified np.interp Function for filtering NAN
#
#     Args:
#         data (ndarray): Input Data
#         plevs (ndarray): Input pressure levels
#         new_plevs (ndarray): Output pressure levels
#         min_levels (int): minimum required pressure levels
#
#     Returns:
#     ndarray : size of new_plevs
#     """
#     data = np.squeeze(data)  # remove 1-dims
#     ix = np.isfinite(data)  # only finite values
#     s = ix.sum()
#     if s > 0:
#         if s > min_levels:
#             data = np.interp(np.log(new_plevs), np.log(plevs[ix]), data[ix], left=np.nan, right=np.nan)
#             return data
#         jx = np.in1d(plevs[ix], new_plevs)  # index of finite values
#         if len(jx) > 0:
#             kx = np.in1d(new_plevs, plevs[ix])  # index of finite values in new pressure levels
#             out = np.full_like(new_plevs, np.nan)
#             out[kx] = data[ix][jx]
#             return out  # just a few values
#     return np.full_like(new_plevs, np.nan)  # Nothing to do
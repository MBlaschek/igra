[![PyPI version](https://badge.fury.io/py/igra.svg)](https://badge.fury.io/py/igra)

# IGRA

Author: M. Blaschek
Date: Dezember 2019

Version: 23.05

This Python 3 Module is intended to read IGRA v2 NCDC data to pandas DataFrames or Xarray Datasets (interpolated to standard pressure levels).

# Install

The code uses Python3 as a standard.

Dependencies:

* numpy
* pandas
* netCDF4
* xarray

Download the Source code from GitHub

```shell
git clone https://github.com/MBlaschek/igra
```

or use the package on [PyPI igra](https://pypi.org/igra)

```shell
pip install igra
```



# Usage

## Download station list 

Read the station list into pandas DataFrame (from file `igra2-station-list.txt` in the IGRAv2 repository)

```python
>>> import igra
>>> stations = igra.download.stationlist('/tmp')
Download complete, reading table ...
Data read from: /tmp/igra2-station-list.txt
Data processed 2787
>>> stations
                wmo      lat      lon     alt state                            name start   end  total
id                                                                                                    
ACM00078861  078861  17.1170 -61.7830    10.0                   COOLIDGE FIELD (UA)  1947  1993  13896
AEM00041217  041217  24.4333  54.6500    16.0        ABU DHABI INTERNATIONAL AIRPOR  1983  2019  36252
AEXUAE05467          25.2500  55.3700     4.0                               SHARJAH  1935  1942   2477
AFM00040911  040911  36.7000  67.2000   378.0                        MAZAR-I-SHARIF  2010  2014   2179
AFM00040913  040913  36.6667  68.9167   433.0                                KUNDUZ  2010  2013   4540
AFM00040938  040938  34.2170  62.2170   977.0                                 HERAT  1978  1988   1107
AFM00040948  040948  34.5500  69.2167  1791.0                         KABUL AIRPORT  1961  2019  17809
AFM00040990  040990  31.5000  65.8500  1010.0                      KANDAHAR AIRPORT  1976  2014   5934
AGM00060355  060355  36.8830   6.9000     3.0                                SKIKDA  1974  1976    639
AGM00060360  060360  36.8330   7.8170     4.0                                ANNABA  1973  2008  30088
AGM00060390  060390  36.6833   3.2167    25.0                          DAR-EL-BEIDA  1948  2019  68372
AGM00060402  060402  36.7170   5.0670     6.0                       BEJAIA-AEROPORT  1973  1988  12372
AGM00060419  060419  36.2830   6.6170   694.0                           CONSTANTINE  1973  2008  21262
AGM00060425  060425  36.2170   1.3330   141.0                                 CHLEF  1973  1977   3213
AGM00060430  060430  36.3000   2.2330   715.0                               MILIANA  1973  1990  14988
...
```

## Download station 

a radiosonde station with the `id` from the station list into `tmp` directory

```python
>>> igra.download.station("AUM00011035", "/tmp")
https://www1.ncdc.noaa.gov/pub/data/igra/data/data-por/AUM00011035-data.txt.zip  to  /tmp/AUM00011035-data.txt.zip
Downloaded:  /tmp/ACM00078861-data.txt.zip
```

## Read station

The downloaded station file can be read to standard pressure levels (default) or table like with all significant levels (different amount of levels per sounding) using `return_table=True`. It is also possible to interpolate to different standard pressure levels with `levels=...`.

Usually the standard pressure levels need to be reported, thus no interpolation should be required.
```python
>>> print(igra.std_plevels)
[1000.0, 2000.0, 3000.0, 5000.0, 7000.0, 10000.0, 15000.0, 20000.0, 25000.0, 30000.0, 40000.0, 50000.0, 70000.0, 
85000.0, 92500.0, 100000.0]
>>> data, station = igra.read.igra("AUM00011035", "/tmp/ACM00078861-data.txt.zip")  
[AUM00011035] [2019-12-09T12:25:42.761655] AUM00011035 [1000.0, 2000.0, 3000.0, 5000.0, 7000.0, 10000.0, 15000.0, 20000.0, 25000.0, 30000.0, 40000.0, 50000.0, 70000.0, 85000.0, 92500.0, 100000.0]
[AUM00011035] [2019-12-09T12:25:42.761692] Reading ascii data into dataframes
[AUM00011035] [2019-12-09T12:25:57.710039] IGRAv2 Lines read: 3758652 Header count: 79638
[AUM00011035] [2019-12-09T12:26:11.583290] Missing pressure values 588657
[AUM00011035] [2019-12-09T12:26:11.583346] Interpolating to standard pressure levels
[AUM00011035] [2019-12-09T12:28:18.356667] (3090358, 7)  >>  (3331343, 8)
[AUM00011035] [2019-12-09T12:28:18.373608] Converting to xarray
[AUM00011035] [2019-12-09T12:28:18.377815] Adding Metadata
[AUM00011035] [2019-12-09T12:28:18.378166] Converting temperature and humidity
[AUM00011035] [2019-12-09T12:28:18.546226] Collecting Station information
>>> data
<xarray.Dataset>
 Dimensions:   (date: 78059, pres: 16)
 Coordinates:
   * date      (date) datetime64[ns] 1949-02-08T04:00:00 ... 2019-10-01
   * pres      (pres) float64 1e+03 2e+03 3e+03 5e+03 ... 8.5e+04 9.25e+04 1e+05
 Data variables:
     gph       (date, pres) float64 nan nan nan nan ... 1.491e+03 791.0 nan
     temp      (date, pres) float64 nan nan nan nan nan ... 274.4 280.0 285.2 nan
     rhumi     (date, pres) float64 nan nan nan nan nan ... nan nan nan nan nan
     dpd       (date, pres) float64 nan nan nan nan nan ... 7.0 21.0 7.0 8.0 nan
     windd     (date, pres) float64 nan nan nan nan nan ... 295.0 290.0 300.0 nan
     winds     (date, pres) float64 nan nan nan nan nan ... 21.0 14.0 10.0 nan
     flag_int  (date, pres) float64 1.0 1.0 1.0 1.0 1.0 ... 0.0 0.0 0.0 0.0 1.0
 Attributes:
     ident:         AUM00011035
     source:        NOAA NCDC
     dataset:       IGRAv2
     processed:     UNIVIE, IMG
     interpolated:  to pres levs (#16)
>>> station
<xarray.Dataset>
 Dimensions:  (date: 78059)
 Coordinates:
   * date     (date) datetime64[ns] 1949-02-08T04:00:00 ... 2019-10-01
 Data variables:
     numlev   (date) int64 14 10 12 13 10 15 15 15 ... 37 41 38 136 131 39 105
     lat      (date) float64 48.25 48.25 48.25 48.25 ... 48.25 48.25 48.25 48.25
     lon      (date) float64 16.36 16.36 16.36 16.36 ... 16.36 16.36 16.36 16.36
 Attributes:
     ident:      AUM00011035
     source:     NOAA NCDC
     dataset:    IGRAv2
     processed:  UNIVIE, IMG

```

## Download a UADB Station

a radiosonde station with the `wmo`  from station list into `tmp` directory

However, you need to register for this data at RDA UCAR. You will need to enter your Email address and password to download the files.
```python
>>> igra.download.uadb("78861", "/tmp", "EMail-Adress", "Password")
https://rda.ucar.edu/cgi-bin/login  to  /tmp/uadb_trhc_78861.txt
100.000 % Completed
Downloaded:  /tmp/uadb_trhc_78861.txt
```
## Read a UADB Station

The downloaded station file can be read to standard pressure levels (default) or table like with all significant levels (different amount of levels per sounding) using `return_table=True`. It is also possible to interpolate to different standard pressure levels with `levels=...`.

Usually the standard pressure levels need to be reported, thus no interpolation should be required.

```python
>>> data, station = igra.read.uadb("078861","/tmp/uadb_trhc_78861.txt")    
[078861] [2019-12-09T13:22:15.726180] 078861 [1000.0, 2000.0, 3000.0, 5000.0, 7000.0, 10000.0, 15000.0, 20000.0, 25000.0, 30000.0, 40000.0, 50000.0, 70000.0, 85000.0, 92500.0, 100000.0]
[078861] [2019-12-09T13:22:15.726269] Reading ascii data into dataframes
[078861] [2019-12-09T13:22:17.448871] UADB Lines read: 579008 skipped: 0 Header: 8747
[078861] [2019-12-09T13:22:18.708963] Missing pressure values 167254
[078861] [2019-12-09T13:22:18.709015] Interpolating to standard pressure levels
[078861] [2019-12-09T13:22:33.040262] (403008, 6)  >>  (414833, 7)
[078861] [2019-12-09T13:22:33.040344] Converting to xarray
[078861] [2019-12-09T13:22:33.043989] Adding Metadata
[078861] [2019-12-09T13:22:33.044279] Converting temperature and humidity
[078861] [2019-12-09T13:22:33.063961] Collecting Station information
>>> data
<xarray.Dataset>
Dimensions:  (date: 8729, pres: 16)
Coordinates:
  * date     (date) datetime64[ns] 1961-04-01 1961-04-09 ... 1993-04-28T12:12:00
  * pres     (pres) float64 1e+03 2e+03 3e+03 5e+03 ... 8.5e+04 9.25e+04 1e+05
Data variables:
    gph      (date, pres) float64 nan nan nan nan ... 1.527e+03 797.0 124.0
    temp     (date, pres) float64 nan nan nan nan ... 281.5 288.5 291.6 297.9
    rhumi    (date, pres) float64 nan nan nan nan ... 0.313 0.674 0.9393 0.799
    windd    (date, pres) float64 nan nan nan nan ... 220.0 140.0 134.8 130.0
    winds    (date, pres) float64 nan nan nan nan nan ... 11.3 3.1 6.2 7.761 9.2
    flag_int (date, pres) float64 1.0 1.0 1.0 1.0 1.0 ... 0.0 0.0 0.0 nan 0.0
Attributes:
    ident:         078861
    source:        NCAR RSA
    dataset:       UADB, ds370.1
    processed:     UNIVIE, IMG
    interpolated:  to pres levs (#16)
>>> station
<xarray.Dataset>
 Dimensions:  (date: 8743)
 Coordinates:
   * date     (date) datetime64[ns] 1961-04-01 1961-04-09 ... 1993-04-28T12:00:00
 Data variables:
     uid      (date) int64 8041502 8041503 8041504 ... 58207091 58209344 58211593
     numlev   (date) int64 17 42 20 43 54 20 56 47 ... 94 99 98 115 89 108 98 104
     lat      (date) float64 17.12 17.12 17.12 17.12 ... 17.12 17.12 17.12 17.12
     lon      (date) float64 298.2 298.2 298.2 298.2 ... 298.2 298.2 298.2 298.2
     alt      (date) float64 3.0 3.0 3.0 3.0 3.0 3.0 ... 5.0 5.0 5.0 5.0 5.0 5.0
     stype    (date) int64 3 3 3 3 3 3 3 3 3 3 3 3 3 ... 3 3 3 3 3 3 3 3 3 3 3 3
 Attributes:
     ident:      078861
     source:     NCAR RSA
     dataset:    UADB, ds370.1
     processed:  UNIVIE, IMG)
```

## Interpolate to custom pressure levels

For example you could use the 32 lowest ERA-Interim pressure levels.
```python
>>> print(igra.era_plevels)
[1000.0, 2000.0, 3000.0, 5000.0, 7000.0, 10000.0, 12500.0, 15000.0, 17500.0, 20000.0, 22500.0, 25000.0, 30000.0, 
35000.0, 40000.0, 45000.0, 50000.0, 55000.0, 60000.0, 65000.0, 70000.0, 75000.0, 77500.0, 80000.0, 82500.0, 85000.0, 
87500.0, 90000.0, 92500.0, 95000.0, 97500.0, 100000.0]

>>> data, station = igra.read.uadb("078861","/tmp/uadb_trhc_78861.txt", levels=igra.era_plevels)                         
```

## Read as DataFrame 

The data is available as ASCII, therefore the closest representation is a pandas DataFrame. This is how the data is read and in the above steps converted to an xarray representation. 

```python
>>> data,station = igra.read.ascii_to_dataframe("/tmp/ACM00078861-data.txt.zip")                                         IGRAv2 Lines read: 508055 Header count: 13896
>>> station
                     numlev     lat     lon
date                                       
1947-01-08 01:00:00      10  17.117 -61.783
1947-01-10 01:00:00      10  17.117 -61.783
1947-01-11 02:00:00       5  17.117 -61.783
1947-01-12 02:00:00       9  17.117 -61.783
1947-01-13 03:00:00       4  17.117 -61.783
...                     ...     ...     ...
1993-04-20 12:00:00      93  17.117 -61.783
1993-04-21 12:00:00     105  17.117 -61.783
1993-04-22 12:00:00      82  17.117 -61.783
1993-04-26 12:00:00     100  17.117 -61.783
1993-04-27 12:00:00      87  17.117 -61.783
1993-04-28 12:00:00      99  17.117 -61.783

[13896 rows x 3 columns]

>>> data
                         pres      gph  temp  rhumi   dpd  windd  winds
date                                                                   
1947-01-08 01:00:00  101600.0     10.0  25.4   82.0   NaN   70.0    8.0
1947-01-08 01:00:00  100000.0    156.0  24.3   83.0   NaN   70.0    9.0
1947-01-08 01:00:00   85000.0   1559.0  14.5   93.0   NaN   80.0   10.0
1947-01-08 01:00:00   70000.0   3187.0   8.8   13.0   NaN  110.0    6.0
1947-01-08 01:00:00   50000.0   5894.0  -8.1   38.0   NaN   90.0    7.0
1947-01-08 01:00:00   40000.0   7587.0 -20.0   18.0   NaN    NaN    NaN
1947-01-08 01:00:00   30000.0   9666.0 -33.2    NaN   NaN   80.0   20.0
1947-01-08 01:00:00   25000.0  10926.0 -41.7    NaN   NaN    NaN    NaN
1947-01-08 01:00:00   20000.0  12416.0 -49.2    NaN   NaN   10.0    7.0
1947-01-08 01:00:00   15000.0  14263.0 -61.3    NaN   NaN    NaN    NaN
...                       ...      ...   ...    ...   ...    ...    ...
1993-04-28 12:00:00     960.0  31525.0 -38.3    NaN   NaN    NaN    NaN
1993-04-28 12:00:00     900.0  31976.0 -34.9    NaN   NaN    NaN    NaN
1993-04-28 12:00:00     880.0  32100.0   NaN    NaN   NaN   95.0   18.5
1993-04-28 12:00:00     810.0  32700.0   NaN    NaN   NaN   95.0    9.2
1993-04-28 12:00:00     700.0  33730.0 -31.5    NaN  49.0    NaN    NaN
1993-04-28 12:00:00     680.0      NaN -31.9    NaN   NaN    NaN    NaN

[494160 rows x 7 columns]
```

# License

MIT License

Copyright (c) 2019 Michael Blaschek

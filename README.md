# IGRA
Author: M. Blaschek
Date: 19.3.2019

This Python 3 Module is intended to read IGRA v2 NCDC data to pandas DataFrames or Xarray Datasets (interpolated to standard pressure levels).

## Usage

* Download station list and read as pandas DataFrame
```python
>>> import igra
>>> stations = igra.download.stationlist('./tmp')

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

* Download station into `tmp` directory
```python
>>> igra.download.station("ACM00078861", "./tmp")
ftp://ftp.ncdc.noaa.gov/pub/data/igra/data/data-por/ACM00078861-data.txt.zip  to  ./tmp/ACM00078861-data.txt.zip
Downloaded:  ./tmp/ACM00078861-data.txt.zip
```

* Read to standard pressure levels

Usually these levels need to be reported. Therefore no interpolation should be necessary.
```python
>>> print(igra.std_plevels)
[1000.0, 2000.0, 3000.0, 5000.0, 7000.0, 10000.0, 15000.0, 20000.0, 25000.0, 30000.0, 40000.0, 50000.0, 70000.0, 
85000.0, 92500.0, 100000.0]
>>> isonde = igra.read.igra("ACM00078861", dataset, levels=None)  
READ: 508055
>>> isonde
<xarray.Dataset>
Dimensions:  (date: 13864, pres: 16)
Coordinates:
  * date     (date) datetime64[ns] 1947-01-08T01:00:00 ... 1993-04-28T12:00:00
  * pres     (pres) float64 1e+03 2e+03 3e+03 5e+03 ... 8.5e+04 9.25e+04 1e+05
Data variables:
    gph      (date, pres) float64 nan nan nan nan ... 1.527e+03 797.0 124.0
    temp     (date, pres) float64 nan nan nan nan ... 281.5 288.5 291.6 297.9
    rhumi    (date, pres) float64 nan nan nan nan nan ... nan nan nan nan nan
    dpd      (date, pres) float64 nan nan nan nan nan ... 11.0 16.0 6.0 1.0 3.7
    windd    (date, pres) float64 nan nan nan nan ... 220.0 140.0 138.3 130.0
    winds    (date, pres) float64 nan nan nan nan nan ... 11.3 3.0 6.1 8.2 9.2
    numlev   (date) int64 10 10 5 9 4 11 9 10 10 ... 89 89 93 105 82 100 87 99
    lat      (date) float64 17.12 17.12 17.12 17.12 ... 17.12 17.12 17.12 17.12
    lon      (date) float64 -61.78 -61.78 -61.78 -61.78 ... -61.78 -61.78 -61.78
Attributes:
    ident:         ACM00078861
    source:        NOAA NCDC
    dataset:       IGRAv2
    processed:     UNIVIE, IMG
    interpolated:  to pres levs (#16)
```

* Download a UADB Station into `tmp` directory

Need to register for this data at RDA Ucar. You will need to enter your Email adress and password to download the files.
```python
>>> igra.download.uadb("78861", "./tmp", "EMail-Adress", "Password")
https://rda.ucar.edu/cgi-bin/login  to  ./tmp/uadb_trhc_78861.txt
100.000 % Completed
Downloaded:  ./tmp/uadb_trhc_78861.txt

```
* Read a UADB Station at standard presssure levels
```python
>>> isonde = igra.read.uadb("078861","./tmp/uadb_trhc_78861.txt")    
READ: 579008 Skipped: 0
>>> isonde
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
    uid      (date) int64 8041502 8041503 8041504 ... 58207091 58209344 58211593
    numlev   (date) int64 17 42 20 43 54 20 56 47 ... 94 99 98 115 89 108 98 104
    lat      (date) float64 17.12 17.12 17.12 17.12 ... 17.12 17.12 17.12 17.12
    lon      (date) float64 298.2 298.2 298.2 298.2 ... 298.2 298.2 298.2 298.2
    alt      (date) float64 3.0 3.0 3.0 3.0 3.0 3.0 ... 5.0 5.0 5.0 5.0 5.0 5.0
    stype    (date) int64 3 3 3 3 3 3 3 3 3 3 3 3 3 ... 3 3 3 3 3 3 3 3 3 3 3 3
Attributes:
    ident:         078861
    source:        NCAR RSA
    dataset:       UADB, ds370.1
    processed:     UNIVIE, IMG
    interpolated:  to pres levs (#16)
```
 
* Interpolate to other pressure levels

For example you could use the 32 lowest ERA-Interim pressure levels.
```python
>>> print(igra.era_plevels)
[1000.0, 2000.0, 3000.0, 5000.0, 7000.0, 10000.0, 12500.0, 15000.0, 17500.0, 20000.0, 22500.0, 25000.0, 30000.0, 
35000.0, 40000.0, 45000.0, 50000.0, 55000.0, 60000.0, 65000.0, 70000.0, 75000.0, 77500.0, 80000.0, 82500.0, 85000.0, 
87500.0, 90000.0, 92500.0, 95000.0, 97500.0, 100000.0]

>>> isonde = igra.read.uadb("078861","./tmp/uadb_trhc_78861.txt", levels=igra.era_plevels)                                            
READ: 579008 Skipped: 0

```


* Read only DataFrame data
```python
>>> idata,istation = igra.read.ascii_to_dataframe("./tmp/ACM00078861-data.txt.zip")                                                   
READ: 508055
>>> istation
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

>>> idata
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

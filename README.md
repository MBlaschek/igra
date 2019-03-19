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
Read to standard levels
>>> print(igra.std_plevels)
>>> isonde = igra.read.igra("ACM00078861", "./tmp/ACM00078861-data.txt.zip", levels=None)  
```

* Download a UADB Station into `tmp` directory

* Interpolate to other pressure levels

* Read only DataFrame data


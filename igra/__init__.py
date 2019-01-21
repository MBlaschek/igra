# -*- coding: utf-8 -*-

from . import download
from . import read
from . import support


std_plevels = [1000., 2000., 3000., 5000., 7000., 10000., 15000., 20000., 25000., 30000., 40000., 50000., 70000.,
               85000., 92500., 100000.]
era_plevels = [1000., 2000., 3000., 5000., 7000., 10000., 12500., 15000., 17500., 20000., 22500., 25000., 30000.,
               35000., 40000., 45000., 50000., 55000., 60000., 65000., 70000., 75000., 77500., 80000., 82500.,
               85000., 87500., 90000., 92500., 95000., 97500., 100000.]

__version__ = '0.1'
__author__ = 'MB'
__status__ = 'dev'
__date__ = 'Do Jän 17 14:44:22 CET 2019'
__institute__ = 'Univie, IMGW'
__github__ = 'git@github.com:MBlaschek/igra.git'
__doc__ = """
Copied doc from IGRAv2 at ftp://ftp.ncdc.noaa.gov/pub/data/igra/

Integrated Global Radiosonde Archive (IGRA) V2beta Readme File

Imke Durre (imke.durre@noaa.gov) - last updated September 2014


TABLE OF CONTENTS

I.    OVERVIEW
II.   WHAT'S NEW IN IGRA 2
III.  DOWNLOAD QUICK START
IV.   CONTENTS  OF FTP DIRECTORY
--------------------------------------------------------------------------------
--------------------------------------------------------------------------------

I. OVERVIEW

This file provides guidance for how to navigate the FTP directory for
IGRA v2beta, the beta release of version 2 of the Integrated Global
Radiosonde Archive. It provides a brief overview of what is new in IGRA 2,
step-by-step instructions for downloading desired Data and _metadata,
and an explanation of the contents of the directory and all of its subdirectories.
The formats of the various types of files available are described in
separate documents.

In the context of this dataset, the designation "beta" means that all
scientific development has been completed, and the dataset is now in the
documentation and review phase that is a prerequisite for it to officially
replace IGRA 1 as NCDC's baseline upper-air dataset.

Send any feedback to Imke Durre at imke.durre@noaa.gov.

--------------------------------------------------------------------------------
--------------------------------------------------------------------------------

II. WHAT'S NEW IN IGRA 2

Following is a summary of what is new and different in IGRA 2 compared to
IGRA 1.

  - More Data: IGRA 2 contains nearly twice as many stations and 30% more
    soundings than IGRA 1.

  - Longer Records: The earliest year with Data in IGRA 2 is 1905, and
    there are several hundred stations with Data before 1946. In IGRA 1,
    only one station's record extends back to before 1946, and its record
    begins in 1938.

  - Ships and Ice Islands: IGRA now contains Data from 112 floating stations,
    including 17 fixed weather ships and buoys, 72 mobile ships, and 23
    Russian ice islands.

  - Additional Variables:
    1. Reported relative humidity and time elapsed since launch are now
       provided in the sounding Data files whenever they are available. This
       allows for the inclusion of humidity observations prior to 1969,
       the first year with dewpoint depression in IGRA 1.
    2. The derived-parameter files now include both reported and calculated
       relative humidity. In soundings in which humidity is reported only
       as relative humidity, all moisture-related derived parameters are based
       on the reported relative humidity. In all other soundings, they are
       based on dewpoint depression/calculated relative humidity.
    3. In addition to monthly means of geopotential height, temperature,
       an wind, monthly means of vapor pressure are now also available.
    For details on these variables and associated changes in Data format,
    see the respective format descriptions.

  - Additional Data Sources:
    1. IGRA 2 is constructed from a total of 33 Data
       sources, including 10 of the 11 Data sources used in IGRA 1.
    2. To improve spatial coverage, Data received via the Global
       Telecommunications System (GTS) by the U.S. Air Force
       14th Weather Squadron replace the less complete NCDC/NCEP-based
       1973-1999 GTS Data which was the largest contributor of xData to
       IGRA 1. This change particularly improves the spatial coverage
       over China in the 1970s and 1980s.
    3. Daily updates now come not only from the GTS, but, for U.S. stations,
       also directly from the U.S. National Weather Service (NWS), resulting
       in higher-precision, higher-vertical resolution Data for U.S.
       stations in near real-time.
    4. Global coverage prior to the 1970s was enhanced primarily by the
       "C-Cards" and "MIT" read_datasets from the National Centers for
       Atmospheric Research as well as Version 1.01 of the Comprehensive
       Historical Upper Air Network from the Institute for Atmospheric
       and Climate Science at ETH Zurich in Switzerland.
    5. Additional Data sources include pilot balloon observations for
       the United States that were digitized under the Climate Data
       Modernization Program (CDMP), Radiosonde and pilot balloon
       observations for several countries in Africa from CDMP and
       Meteo-France, ship and ice island observations from NCDC's archive,
       Antarctic Radiosonde observations provided by the British Antarctic
       Survey, the Historical Arctic Radiosonde Archive from the National
       Geophysical Data Center, and 1990s Indonesian Radiosonde xData
       provided by the Japan Agency for Marine-Earth Science and Technology.

  - Eleven-character Station IDs: To accommodate stations other than those
    with world Meteorological Organization (WMO) station numbers, IGRA now
    uses 11-character station identifiers that consist of a two-character
    country code, a one-character station network code, and an
    eight-character station identifier.
    The station IDs for WMO stations, which account for approximately 80% of
    the IGRA 2 stations, contain a network code of "M" followed by "000"
    followed by the five-digit WMO identification number. For example, the
    IGRA 2 station identifier for Key West (WMO# 72201) is USM00072201.
    The remaining stations are identified by ship call signs (network
    code "V"), Weather Bureau, Army, Navy (WBAN) numbers ("W"),
    International Civil Aviation Organization call signs ("I"), and
    specially constructed identifiers ("X").
    For more details, see the format description of the station list.

  - Changed station list format: The order of fields in the station list
    has been changed for consistency with some of NCDC's other read_datasets. In
    addition, the identification of stations as GCOS Upper Air Network (GUAN)
    and Lanzante/Klein/Seidel (LKS) stations has been removed. Relevant LKS
    stations are captured within the RATPAC product, and the latest list of
    GUAN stations is best obtained directly from the WMO.

  - Additional Information in Sounding Headers:
    1. Header records in sounding Data files now include two xData source codes,
       one for pressure levels and one for non-pressure levels.
    2. In order to be able to indicate the position of mobile stations at
       each observation time, fields for the latitude and longitude have
       been added to the sounding headers in Data files. For fixed stations,
       including moored ships, the coordinates entered into these fields are
       always the same as those shown in the IGRA station list since the
       actual position is generally not known on a sounding-by-sounding
       basis at those stations. Coordinates are not included in the sounding
       headers of the derived-parameter files since sounding-derived
       parameters are provided only for fixed stations.
    For more details, see the format description of the Data files.

  - Soundings Without Observation Hour: Unlike IGRA 1, IGRA 2 contains
    soundings from some Data sources in which the time of day at which
    an observation was made is indicated only by the release time, i.e.,
    the time at which the balloon was launched, and the
    nominal/observation hour is missing (= 99). Since conventions for
    determining the observation hour from the release time vary over
    time and among agencies, no attempt has been made to infer the
    observation hour from the release time in IGRA 2.

  - Modified Level Type Indicators: The meaning of the first digit of
    the level type indicator in sounding records has changed as follows:

    Blank is no longer used.
    1 continues to indicate a standard pressure level.
    2 indicates a non-standard pressure level regardless of whether it
      contains thermodynamic Data or only wind xData.
    3 indicates a non-pressure level, which always only contains wind
      observations in IGRA 2.

  - Non-Pressure Surface Levels: Unlike in IGRA 1, IGRA 2 contains surface
    levels that do not contain a pressure value. Such levels only appear in
    soundings that consist entirely of Data levels whose vertical coordinate is
    identified only by height.

  - Methodological Changes:
    1. The process of choosing which Data sources contribute to each station
       record as well as the process of merging multiple Data sources into
       one station record were redesigned to increase automation, accommodate
       a greater variety of Data sources and station identifiers, and preserve
       a larger number of pilot balloon observations.
    2. In addition, some minor improvements were made to the quality assurance
       procedures, including, most notably, the addition of basic checks on
       elapsed time and relative humidity as well as improved selection of
       a single surface level within soundings in which multiple levels are
       identified as surface.
    3. The compositing procedure was redesigned. Stations are now composited
       when they are within 5 km of each other and their records do not contain
       soundings at concurrent observation times.
    All of these modifications will be described in greater detail in a
    future article.

  - Additional Station History Information:
    1. The IGRA _metadata file, which contains documented information about
       the instrumentation and observing practices at many stations, has been
       augmented with additional records extracted from the Gaffen (1996)
       collection that formed the basis for the original IGRA _metadata.
       The additional records are for nearly 700 IGRA 2 stations for
       which no Data was available in IGRA 1.
    2. To provide information on instrumentation used in recent years for which
       documented station history information is not available in the IGRA
       IGRA _metadata file, the WMO Radiosonde/sounding system and measuring
       equipment codes contained in Global Telecommunications System messages
       are also supplied in separate files for the years 2000-2013. Note that
       these codes have not been checked for accuracy and are provided
       as received.

--------------------------------------------------------------------------------
--------------------------------------------------------------------------------

III. DOWNLOAD QUICK START

http://www1.ncdc.noaa.gov/pub/Data/igra/v2beta/ .

--------------------------------------------------------------------------------
--------------------------------------------------------------------------------
"""

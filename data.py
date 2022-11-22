"""
# -- ------------------------------------------------------------------------------------------------------------------------   -- #
# -- project: Project 1: Fundamental Analysis.                                                                                   -- #
# -- script: data.py : Python script with the main functionality                                                                -- #
# -- author: EstebanMqz                                                                                                         -- #
# -- license: GNU General Public License v3.0                                                                                   -- #
# -- repository: https://github.com/EstebanMqz/MyST_Project/blob/main/data.py                                                     -- #
# -- ------------------------------------------------------------------------------------------------------------------------   -- #
"""
from os import listdir
from os.path import isfile, join
import pandas as pd
import functions as fn
from datetime import datetime
from datetime import datetime, timedelta, date
import MetaTrader5 as mt5
import pytz

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_rep', True)
pd.set_option('display.width', None)

def read_indicator(indicator,date):
    """
    Function that reads a .csv or .txt file contaning data 
    of economic indicators Actual, Previous and Consensus estimates.

    Parameters
    ----------
    + indicator: Economic indicator contained in files with Datetime,
    Actual, Previous and Consensus estimates va
    lues in cols (string).
    + date: start_date for data extraction of given indicator ('YYYY-MM-DD').
    -------
    Returns: Historic data with Datetime, Actual, Previous and Consensus 
    estimates values in cols. (dataframe).
    """
    ind_raw=pd.read_csv(indicator)
    ind_raw.drop('Revised', inplace=True, axis=1)
    ind_raw.DateTime=pd.to_datetime(ind_raw.DateTime)
    ind_raw=ind_raw[~(ind_raw['DateTime'] < date)]

    return ind_raw
    

def fx_rate(pairs, account, pw):
    """
    Function that downloads exchange rates data with MetaTrader 5 api.

    Parameters
    ----------
    + indicator: Economic indicator with Datetime, Actual, Previous and 
    Consensus estimates values in cols. for its data.
    + date: start_date for data extraction of given indicator.
    -------
    Returns: Historic data with OHCLV, spread and real_volume cols. (dataframe).
    """
    #MT5 data download
    mt5.initialize(login = account, server = 'MetaQuotes-Demo', password = pw)
    if not mt5.initialize():
        print("initialize() failed, error code =",mt5.last_error()) #Establish connection to MetaTrader 5 terminal
        quit()

    timezone = pytz.timezone("Etc/UTC") # Set time zone to UTC
    utc_from = datetime(2018, 1, 1, tzinfo=timezone) #'datetime' object in UTC time zone to avoid local time offset.
    utc_to = datetime(2020, 3, 1, tzinfo=timezone)
    # get 10 EURUSD H4 bars starting from 01.10.2020 in UTC time zone
    rates = mt5.copy_rates_range(pairs, mt5.TIMEFRAME_M30, utc_from, utc_to)
    mt5.shutdown() # Shut down connection to Mt5
    rates_frame = pd.DataFrame(rates) #Create df with data
    rates_frame['time']=pd.to_datetime(rates_frame['time'], unit='s') #Convert time to datetime with secs format,

    return rates_frame   






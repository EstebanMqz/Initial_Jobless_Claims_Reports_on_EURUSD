
"""
# -- ------------------------------------------------------------------------------------------------------------------------   -- #
# -- project: Project 1: Fundamental Analysis                                                                                   -- #
# -- script: functions.py : Python script with the main functionality                                                           -- #
# -- author: EstebanMqz                                                                                                         -- #
# -- license: GNU General Public License v3.0                                                                                   -- #
# -- repository: https://github.com/EstebanMqz/MyST_Project/blob/main/functions.py                                              -- #
# -- ------------------------------------------------------------------------------------------------------------------------   -- #
"""

import pandas as pd
import pandas_datareader as pdr
import numpy as np


def case_operation(data_raw):
    """
    Function that adds Case and Type column to the dataframe of the economic indicator

        Parameters
        ----------
        fx_rates: fx_rates with OHLCV (dataframe).
        title_1: Upper subplot title (str). 
        title_2: Lower subplot title (str). 

        Returns
        -------
        Returns candlesticks time-series with Moving Average in n-windows, Bollinger Bands (n-window dependent) and Volumes.
    """

    pd.options.mode.chained_assignment = None
    
    data_raw['Case'] = ''
    for i in range(len(data_raw)):
        if data_raw.Actual[i] >= data_raw.Consensus[i] and data_raw.Consensus[i] >= data_raw.Previous[i]:
            data_raw.Case.iloc[i] = 'A'
        elif data_raw.Actual[i] >= data_raw.Consensus[i] and data_raw.Consensus[i] < data_raw.Previous[i]:
            data_raw.Case.iloc[i] = 'B'
        elif data_raw.Actual[i] < data_raw.Consensus[i] and data_raw.Consensus[i] >= data_raw.Previous[i]:
            data_raw.Case.iloc[i] = 'C' 
        elif data_raw.Actual[i] < data_raw.Consensus[i] and data_raw.Consensus[i] < data_raw.Previous[i]:
            data_raw.Case.iloc[i] = 'D'

    data_raw['EURUSD']= ''
    for i in range(len(data_raw)):
        if data_raw.Case[i] == 'A' or data_raw.Case[i] == 'B':
            data_raw.EURUSD[i] = 'Buy'
        elif data_raw.Case[i] == 'C' or data_raw.Case[i] == 'D':
            data_raw.EURUSD[i] = 'Sell'
        else:
            data_raw.EURUSD[i] = 'NA'
            
    return data_raw


def Optimization(index, rate):
    """
        Optimization function for EURUSD exchange rates from Initial Jobless Claims economic indicator.

        Parameters
        ----------
        index: Economic Index (IJC) Actual Consensus and Previous data (dataframe).
        rates: EURUSD fx_rates MetaTrader5 (dataframe).

        Returns
        -------
        Optimization data for timestamp in index and rates with
        cases scenarios, direction, pips (ups & downs) and vol (dataframe)
    """

    DateTime, Case, Direction, pip_up, pip_down, volatility = ([] for i in range(6))
    
    for i in range(len(rate['time'])):
        for j in range(len(index['DateTime'])):
            
            if index['DateTime'][j]==rate['time'][i]:
                DateTime.append(index['DateTime'][j])
                Case.append(index.Case[j])

                if index['EURUSD'][j] == 'Sell':
                    Direction.append(-1)

                elif index['EURUSD'][j] == 'Buy':
                    Direction.append(1)

                # pips Alcistas
                pip_up.append(abs(np.round((rate.close[i-30]-rate.open[i+30])*10000)))
                # pips Bajistas
                pip_down.append(abs(np.round((rate.open[i-30]-rate.close[i+30])*10000)))
                # volatilidad 
                volatility.append(np.round(abs((rate.high[i-30]- rate.high[i+30])-(rate.low[i-30]- rate.low[i+30]))*10000)) 
    
    df = pd.DataFrame({"DateTime" : DateTime, "Case" : Case, "Direction" : Direction,
    "pip_up" : pip_up, "pip_down" : pip_down, " volatility" : volatility}, index = None)


    return df




    


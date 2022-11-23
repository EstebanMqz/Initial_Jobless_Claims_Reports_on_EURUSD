
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

    data_raw['Operation']= ''
    for i in range(len(data_raw)):
        if data_raw.Case[i] == 'A' or data_raw.Case[i] == 'B':
            data_raw.Operation[i] = 'Sell'
        elif data_raw.Case[i] == 'C' or data_raw.Case[i] == 'D':
            data_raw.Operation[i] = 'Buy'
        else:
            data_raw.Operation[i] = 'NA'
            
    return data_raw



    


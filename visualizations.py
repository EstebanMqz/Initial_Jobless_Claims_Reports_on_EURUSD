"""
# -- ------------------------------------------------------------------------------------------------------------------------   -- #
# -- project: Project 1: Fundamental Analysis                                                                                   -- #
# -- script: visualizations.py : Python script with the main functionality                                                      -- #
# -- author: EstebanMqz                                                                                                         -- #
# -- license: GNU General Public License v3.0                                                                                   -- #
# -- repository: https://github.com/EstebanMqz/MyST_Project/blob/main/visualizations.py                                           -- #
# -- ------------------------------------------------------------------------------------------------------------------------   -- #
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import kaleido
import plotly.graph_objects as go #plotly
from statsmodels.tsa.stattools import pacf
from statsmodels.tsa.stattools import acf
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller
from plotly.subplots import make_subplots 
import warnings
import time 
import plotly.express as px
import statsmodels.api as sm #qq plot
import pylab


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_rep', True)
pd.set_option('display.width', None)


def plotly_graph2(x, y1, y2, name1, name2, x_label, y_label, title):
    """
    Function that plots a two-traced line+marker graph with plotly for Actual values and 
    Consensus estimates from time-series weekly statements reports.

        Parameters
        ----------
        x: Datetime values should be set as index for plotly chart. 
        y1: Values of reports results (Ac, Pr, Est) in df cols. 
        y2: Values of reports results (Ac, Pr, Est) in df cols.  
        name1: Label of y1 trace (str). 
        name2: Label of y2 trace (str). 
        x_label: xlabel for plot (str). 
        y_label: y_label for plot (str).          
        title: Title of the plot (str). 

        Returns
        -------
        Returns 2 traces (y1,y2) in a didactic graph with plotly for x.
    """
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y1, mode='lines+markers',
    name=name1, line=dict(color='black'), marker=dict(symbol=2, color='blue')))
    fig.add_trace(go.Scatter(x=x, y=y2, mode='lines+markers',
    name=name2, line=dict(color='black'), marker=dict(symbol=2, color='green')))
    fig.update_layout(title=title, xaxis_title=x_label, yaxis_title=y_label)
    fig.update_xaxes(showspikes=True)
    fig.update_yaxes(showspikes=True)

    return fig.show()#,fig.show("png")


def plotly_graph1(x, y, name, x_label, y_label, title):
    """
    Function that plots a one-trace line+marker graph with plotly for time-series 
    reports Differences between Actual and Consensus in weekly statements.

        Parameters
        ----------
        x: Datetime values should be set as index for plotly chart. 
        y: Values of reports results Difference (Actual-Consensus) in df cols. 
        name: Label of y trace (str). 
        x_label: xlabel for plot (str). 
        y_label: y_label for plot (str).          
        title: Title of the plot (str). 
        Returns
        -------
        Returns 1 trace equal to y = difference (A-C) showing if forecasts are Beaten or Missed. 
    """
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines+markers',
    name=name, line=dict(color='black'), marker=dict(symbol=2, color='yellow')))
    fig.add_hline(y=0, line_dash="dash", line_width=3, line_color="darkred")
    fig.add_hrect(y0=0, y1=45, line_width=0, fillcolor="red", opacity=0.15)
    fig.add_hrect(y0=0, y1=-35, line_width=0, fillcolor="green", opacity=0.15)
    fig.update_layout(title=title, xaxis_title=x_label, yaxis_title=y_label)
    fig.update_xaxes(showspikes=True)
    fig.update_yaxes(showspikes=True)

    return fig.show()#,fig.show("png")



def plotly_graph(x, y, name, x_label, y_label, title):
    """
    Function that plots a one-trace line+marker graph with plotly for gral. time-series.

        Parameters
        ----------
        x: Datetime values should be set as index for plotly chart. 
        y: Values present in dataframe cols. 
        name: Label of y trace (str). 
        x_label: xlabel for plot (str). 
        y_label: y_label for plot (str).          
        title: Title of the plot (str). 
        Returns
        -------
        Returns a one-trace line+marker graph with plotly for gral. time-series analysis.
    """
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x,y=y,mode='lines',name=name,line=dict(color='blue')))
    fig.add_hline(y=1, line_dash="dash", line_width=2, line_color="darkred")
    fig.update_layout(title=title, xaxis_title=x_label, yaxis_title=y_label)
    fig.update_xaxes(showspikes=True)
    fig.update_yaxes(showspikes=True)

    return fig.show()#,fig.show("png")

def OHCLV_csticks(fx_rates, title_1, title_2, n):
    """
    Function that plots candlesticks, BB and MA for the given stock/forex with given temporality in dataframe (fx_rates).

        Parameters
        ----------
        fx_rates: fx_rates with OHLCV (dataframe).
        title_1: Upper subplot title (str). 
        title_2: Lower subplot title (str).
        n: MA & Std. ~ Window (default = 30)

        Returns
        -------
        Returns candlesticks time-series with Moving Average (n ~ window), Bollinger Bands (n ~ Window) and Volumes.
    """
    fx_rates['sma'] = fx_rates['close'].rolling(n).mean()
    fx_rates['std'] = fx_rates['close'].rolling(n).std(ddof = 0)

    fig = make_subplots(rows = 2, cols = 1, shared_xaxes = False, 
    subplot_titles = (title_1, title_2), vertical_spacing = 0.5, row_width = [0.2, 1])

    # Upper Bound
    fig.add_trace(go.Scatter(x = fx_rates['time'],
                            y = fx_rates['sma'] + (fx_rates['std'] * 2),
                            line_color = 'black',
                            line = {'dash': 'dash'},
                            name = 'outer', showlegend=True,
                            opacity = 0.3),
                row = 1, col = 1)
                
    # Moving Average (n~Windows)
    fig.add_trace(go.Scatter(x = fx_rates['time'],
                        y = fx_rates['sma'],
                        line_color = 'black', showlegend=True,
                        name = 'sma'),
                row = 1, col = 1)
    
    # Candlestick Plot
    fig.add_trace(go.Candlestick(x = fx_rates['time'],
                                open = fx_rates['open'],
                                high = fx_rates['high'],
                                low = fx_rates['low'],
                                close = fx_rates['close'], showlegend=True,
                                name = 'candlesticks'),
                row = 1, col = 1)

    # Lower Bound 
    fig.add_trace(go.Scatter(x = fx_rates['time'],
                            y = fx_rates['sma'] - (fx_rates['std'] * 2),
                            line_color = 'purple',
                            line = {'dash': 'dash'},
                            name = 'bands', showlegend=True,
                            opacity = 0.3),
                row = 1, col = 1)
    
    # Volume Plot
    fig.add_trace(go.Bar(x = fx_rates['time'], y = fx_rates['tick_volume'], showlegend=False), 
                row = 2, col = 1)

    return fig.show()#,fig.show("png")


def indicator_scenarios(indicator, title):
    """
    Function that plots an histogram of Case Scenarios and a Counter dataframe for Type 
    of operations executed assuming the plotted scenarios.

        Parameters
        ----------
        indicator: Economic indicator with added cols. Case scenarios and Type (Buy or Sell) as (dataframe).
        title: Plot title (str). 

        Returns
        -------
        Returns histogram of scenarios and a dataframe of type of operations.
    """
    Cases = indicator.groupby('EURUSD') 
    Actual = pd.DataFrame(Cases['EURUSD'].count()) 
    Actual.rename(columns = {'EURUSD':'Counter', 'Cases': 'Cases'}, inplace = True) 
    Actual = Actual.sort_values(by=['Counter'], ascending=False) 
    fig = px.histogram(indicator, x="Case", title=title, color='Case')
    fig.show()#, fig.show("png")
    return Actual

def create_corr_plot(index, plot_pacf=False):
    """
    Function that graphs lines+marker AutoCorrelation and Partial AutoCorrelation 
    plot intended to model economic index Actual values.

        Parameters
        ----------
        index: Actual values from economic index (col) 

        Returns
        -------
        lines+marker AutoCorrelation and Partial AutoCorrelation 
        plots in a didactic graph with plotly.
    """
    corr_array = pacf(index.dropna(), alpha=0.05) if plot_pacf else acf(index.dropna(), alpha=0.05)
    lower_y = corr_array[1][:,0] - corr_array[0]
    upper_y = corr_array[1][:,1] - corr_array[0]

    fig = go.Figure()
    [fig.add_scatter(x=(x,x), y=(0,corr_array[0][x]), mode='lines+markers',line_color='#3f3f3f') 
     for x in range(len(corr_array[0]))]
    fig.add_scatter(x=np.arange(len(corr_array[0])), y=corr_array[0], mode='markers', marker_color='#1f77b4',
                   marker_size=4)

    fig.add_scatter(x=np.arange(len(corr_array[0])), y=upper_y, mode='lines', line_color='rgba(255,255,255,0)')
    fig.add_scatter(x=np.arange(len(corr_array[0])), y=lower_y, mode='lines',fillcolor='rgba(32, 146, 230,0.3)',
            fill='tonexty', line_color='rgba(255,255,255,0)')
    fig.update_traces(showlegend=False)
    fig.update_yaxes(zerolinecolor='black')
    
    title='Partial Autocorrelation (PACF)' if plot_pacf else 'Autocorrelation (ACF)'
    fig.update_layout(title=title)
    fig.show()

def qq(index):
    """
    Function that graphs a QQ-plot intended to model economic index Actual values.

        Parameters
        ----------
        index: Actual values from economic index (col) 

        Returns
        -------
        QQ-plot for given data.
    """
    sm.qqplot(index, line= 'q', fit  = True)
    pylab.show()    


def Stationarity(x, y, n):
    """
    Function that plots a time-series and its Trend, Seasonality and Residuals 
    returning the Augmented Dickey Fuller p-value for given n periods.

        Parameters
        ----------
        x: DateTime values from economic index (col). #data_raw['DateTime']
        y: Actual values from economic index (col). #data_raw['Actual']
        n: Periods for decomposition (int).

        Returns
        -------
        lines+marker Series, Trend, Seasonality and Residuals plots in a didactic graph with plotly.
    """

    decomposition = seasonal_decompose(y, period = n)

    trend = decomposition.trend
    seasonal = decomposition.seasonal
    residual = decomposition.resid

    fig = make_subplots(rows = 4, cols = 1, shared_xaxes = False, 
                        subplot_titles = ('Actual', 'Trend', 'Seasonal', 'Residuals'),
                        vertical_spacing = 0.15, row_width = [0.25, 0.25, 0.25, 0.25])

    fig.add_trace(go.Scatter(x=x, y=y, mode='lines+markers', name='Actual',
         line=dict(color='black'), marker=dict(symbol=2, color='black')))

    fig.add_trace(go.Scatter(x=x, y=trend, mode='lines+markers', name='Trend',
         line=dict(color='black'), marker=dict(symbol=2, color='blue')), row = 2, col = 1)

    fig.add_trace(go.Scatter(x=x, y=seasonal, mode='lines+markers', name='Seasonal',
         line=dict(color='black'), marker=dict(symbol=2, color='green')), row = 3, col = 1)

    fig.add_trace(go.Scatter(x=x, y=residual, mode='lines+markers', name='Residuals',
         line=dict(color='black'), marker=dict(symbol=2, color='gray')), row = 4, col = 1)

    fig.show()
   
    return "p-value:", adfuller(y)[1], 


def Box(data, y, title):
    """
    Function that plots a box and whisker plot for data.

        Parameters
        ----------
        data: Economic index data with previous, actual and consensus as (col).
        y: Actual values from economic index (col). 
        title: Title (str). 

        Returns
        -------
        Didactic box and whisker plot to detect outliers.
    """

    fig = px.box(data, y=y, points="all")
    fig.update_layout(title=title, yaxis_title="Values")
    
    return fig.show()


    
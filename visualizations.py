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
import plotly.graph_objects as go #plotly
import warnings
import time 
import plotly.express as px


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_rep', True)
pd.set_option('display.width', None)


def plotly_graph(x, y1, y2, name1, name2, x_label, y_label, title):
    """
    Function that plots a line+marker graph with plotly.

        Parameters
        ----------
        x: Values Dataframe to be plotted as index with plotly. #data_raw['DateTime']
        y1: Values of reports results (Ac, Pr, Est). #data_raw['Actual']
        y2: Values of reports results (Ac, Pr, Est). #data_raw['Consensus']
        name1: Label of y1 trace (str). #data_raw.columns[1]
        name2: Label of y2 trace (str). #data_raw.columns[2]
        x_label: xlabel for plot (str). #data_raw.columns[0]
        y_label: y_label for plot (str). # "Wk. thousands"        
        title: Title of the plot (str). "Initial Jobless Claims"

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

    return fig.show()


    

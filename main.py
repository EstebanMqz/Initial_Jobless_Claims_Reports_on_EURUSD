"""
# -- ------------------------------------------------------------------------------------------------------------------------   -- #
# -- project: Project 1: Fundamental Analysis.                                                                                  -- #
# -- script: main.py : Python script with the main functionality                                                                -- #
# -- author: EstebanMqz                                                                                                         -- #
# -- license: GNU General Public License v3.0                                                                                   -- #
# -- repository: https://github.com/EstebanMqz/MyST_LAB_4/blob/main/main.py                                                     -- #
# -- ------------------------------------------------------------------------------------------------------------------------   -- #
"""
import chart_studio.plotly as py   
import plotly.graph_objects as go  
import plotly.io as pio            
pio.renderers.default = "browser"  
import functions as fn
import visualizations as vs
import data as dt
import pandas as pd
from os import path
import fire



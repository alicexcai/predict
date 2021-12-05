import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px

import requests, os
from gwpy.timeseries import TimeSeries
from gwosc.locate import get_urls
from gwosc import datasets
from gwosc.api import fetch_event_json

from copy import deepcopy
import base64

import matplotlib as mpl
mpl.use("agg")
from matplotlib.backends.backend_agg import RendererAgg
_lock = RendererAgg.lock


# -- Set page config
apptitle = 'Data Visualizer'

st.set_page_config(page_title=apptitle, page_icon=":eyeglasses:")

# -- Create sidebar for plot controls
st.sidebar.markdown("## Select Visualization Parameters")

num_graphs = st.sidebar.slider('Number of graphs', 1, 10, 1)  # min, max, default

regression = st.sidebar.checkbox('Regression', value=True)
if regression == True:
    regression_type = st.sidebar.selectbox('Regression Type', 
        ['Ordinary Least Squares', 
         'Locally WEighted Scatterplot Smoothing',
         'Moving Averages: Rolling',
         'Moving Averages: Exponential',
         'Moving Averages: Expanding'])

# Title the app
st.title('Data Visualizer')
st.markdown("""
 Visualize your data by changing the parameters in the sidebar.
""")
dataframe = pd.read_csv('./example_data.csv')
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    dataframe = pd.read_csv(uploaded_file)
    st.subheader("Raw Data")
    st.write(dataframe)

parameter_list = dataframe.columns.tolist()


def graph_data(dataframe, parameter_list, graph_key):
    
    graph_title = st.text_input("Enter your graph title:", "Graph Title", key=graph_key)
    col1, col2 = st.columns(2)

    graph_xdata = col1.selectbox('X Data', parameter_list, key=graph_key)
    graph_ydata = col2.multiselect('Y Data', parameter_list, key=graph_key)

    # st.subheader("Datatype: ", dataframe[graph1_ydata].dtype)
    
    # Types of regressions: https://plotly.com/python/linear-fits/   
    regression_options = {
        'Ordinary Least Squares': ['ols', None], 
        'Locally WEighted Scatterplot Smoothing': ['lowess', dict(frac=0.1)], 
        'Moving Averages: Rolling': ['rolling', dict(window=5)],
        'Moving Averages: Exponential': ['ewm', dict(halflife=2)],
        'Moving Averages: Expanding': ['expanding', None],
        }
    
    graph_fig = px.scatter(
        dataframe,
        x=graph_xdata,
        y=graph_ydata,
        trendline= None if regression != True else regression_options[regression_type][0],
        trendline_options= None if regression != True else regression_options[regression_type][1],
    )
    
    st.subheader(graph_title)
    st.write(graph_fig)

for i in range(num_graphs):
    graph_data(dataframe, parameter_list, i)

with st.expander("See notes"):

    st.markdown("""
About the example data:                

This work examines the effects of different agent types on prediction market outcomes and effects of prediction market environments on agent utilities.

Agent types:
- Random
- Biased
- Analytic
- Myopic

Key questions:
 * How do different agent types affect prediction market outcomes?
 * How do different prediction market environments affect payoffs for different agent types?
 
""")


st.subheader("About this app")
st.markdown("""
This app allows users to easily visualize and analyze statistics for their data.
""")
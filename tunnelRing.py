# -*- coding: utf-8 -*-
"""
Created on Fri Apr  9 12:39:27 2021

@author: iminano
"""


import comtypes
from comtypes import client
import streamlit as st
import numpy as np
import pandas as pd
import math
import os
import sys
import comtypes.client


st.write("""

# SAP 2000: Tunnel ring modeller

""")

st.sidebar.header('User Input Values')




def user_input_features():

    Diameter = st.sidebar.text_input('Tunnel mean diameter, D [m]',10)

    	##st.sidebar.add_rows

    nel = st.sidebar.slider('Number of elements, nel', min_value=1, max_value = 1000, step = 1)

    	##st.sidebar.add_rows

    # No_Of_Years = st.sidebar.selectbox('Select No Of Years',Year_List, 2)



    data = {'Diameter': Diameter,'Number of elements': nel}
    features = pd.DataFrame(data, index=[0])
    return features

df = user_input_features()

def nelLength(df):
    l=(2*np.pi*(0.5*float(df["Diameter"][0]))**2)/(int(df["Number of elements"][0]))
    return l

st.subheader('User Entered parameters : ')

st.write(df)

st.subheader('The calculated element length is:')


st.write(np.round(nelLength(df),2), 'm')
df_1=nelLength(df)




import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import os

st.set_page_config(layout="wide")
pd.options.plotting.backend = "plotly"

@st.cache
def return_data():
    data = {}
    data['Load'] = pd.read_csv("./data_input/Load.csv",sep=';')
    # data['Load'] .index = pd.to_datetime(data['Load']['DateTime']).dt.round('H')
    data['HRO'] = pd.read_csv("./data_input/HRO_tab.csv")
    data['HRO'].index = pd.to_datetime(data['HRO'][['Year','Month','Day']])
    data['HRO'].drop(['Year','Month','Day'],axis=1,inplace=True)
    data['HRE'] = pd.read_csv("./data_input/HRE_tab.csv")
    data['HRE'].index = pd.to_datetime(data['HRE'][['Year','Month','Day']])
    data['HRE'].drop(['Year','Month','Day'],axis=1,inplace=True)
    data['TA'] = pd.read_csv("./data_input/TA_tab.csv")
    data['TA'].index = pd.to_datetime(data['TA'][['Year','Month','Day']])
    data['TA'].drop(['Year','Month','Day'],axis=1,inplace=True)
    data['TP'] = pd.read_csv("./data_input/TP_tab.csv")
    data['TP'].index = pd.to_datetime(data['TP'][['Year','Month','Day']])
    data['TP'].drop(['Year','Month','Day'],axis=1,inplace=True)
    return data

data = return_data()
liste = ["HRO","HRE","TA","TP"]


liste_load = st.multiselect('Load',data['Load'].drop(['DateTime'],axis=1).columns,default=['AT','FR','DE'])
fig = data['Load'][liste_load].plot()
fig.update_layout(
    hovermode='x',
    title='Load'
    )
st.plotly_chart(fig,use_container_width=True)

liste_HRE = st.multiselect('HRE',data['HRE'].columns,default=['AT','FR','DE'])
fig = data['HRE'][liste_HRE].plot()
fig.update_layout(
    hovermode='x',
    title='HRE'
    )
st.plotly_chart(fig,use_container_width=True)

liste_HRO = st.multiselect('HRO',data['HRO'].columns,default=['AT','FR','DE'])
fig = data['HRO'][liste_HRO].plot()
fig.update_layout(
    hovermode='x',
    title='HRO'
    )
st.plotly_chart(fig,use_container_width=True)

liste_TA = st.multiselect('TA',data['TA'].columns,default=['AT34','FRC1','DE21'])
fig = data['TA'][liste_TA].plot()
fig.update_layout(
    hovermode='x',
    title='TA'
    )
st.plotly_chart(fig,use_container_width=True)

liste_TP = st.multiselect('TP',data['TP'].columns,default=['AT34','FRC1','DE21'])
fig = data['TP'][liste_TP].plot()
fig.update_layout(
    hovermode='x',
    title='TP'
    )
st.plotly_chart(fig,use_container_width=True)

col_1, col_2 = st.columns(2)

with col_1:
    jeu_donne_1 = st.selectbox('Données 1',liste)
    colonne_1 = st.selectbox('Feature 1',data[jeu_donne_1].columns)

with col_2:
    jeu_donne_2 = st.selectbox('Données 2',liste)
    colonne_2 = st.selectbox('Feature 2',data[jeu_donne_2].columns)

a = pd.concat((data[jeu_donne_1][[colonne_1]],data[jeu_donne_2][[colonne_2]]),axis=1)

fig = go.Figure(go.Scatter(
    x = a.iloc[:,0],
    y = a.iloc[:,1],
    mode='markers'
))
fig.update_layout(height=800)
st.plotly_chart(fig,use_container_width=True)

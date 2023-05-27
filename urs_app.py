import streamlit as st
import pandas as pd
import numpy as np
import viz_utility as vutil
import altair as alt


#Initalize
metric_select = 'Select Metric'
table_select = 'Select Table'

st.title('MH URS Parsinator - Data Review')

@st.cache_data
def load_data(domain):
    data = vutil.viz_data_get(domain)
    return data

domain_select = st.selectbox(
    'What domain would you like to review?',
    ('Select Domain','NOMS'))

data = load_data(domain_select)

if not data.empty:
    metric_select = st.selectbox(
        'What metric would you like to review?',
        ('Select Metric',)+tuple(data['metric_name'].unique()))
    
if metric_select != 'Select Metric':
    table_select = st.selectbox(
        'What table would you like to review?',
        ('Select Table',)+tuple(data[data['metric_name']==metric_select]['table_name'].unique()))

data_load_state = st.text('Loading data...')
data_load_state.text("Done! (using st.cache_data)")

if st.checkbox('Show raw data'):
    if metric_select != 'Select Metric' and table_select != 'Select Table':
        st.subheader('Raw data')
        st.write(data[(data['metric_name']==metric_select)&(data['table_name']==table_select)])
    elif metric_select != 'Select Metric':
        st.subheader('Raw data')
        st.write(data[(data['metric_name']==metric_select)])
    else:
        st.subheader('Raw data')
        st.write(data)

if (not data.empty) and (metric_select != 'Select Metric') and (table_select != 'Select Table'):
    data['year']=data['year'].astype('str')

    ch = alt.Chart(data[['year','state_name','metric_result']][(data['metric_name']==metric_select)&(data['table_name']==table_select)]).mark_line().encode(x='year',y='metric_result',text='state_name').encode(alt.Color("state_name"))

    st.altair_chart(ch, use_container_width=True)
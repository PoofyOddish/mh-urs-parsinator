import streamlit as st
import pandas as pd
import numpy as np
import viz_utility as vutil
import altair as alt

st.title('MH URS Parsinator - Data Review')
st.header('Single-State Data Explorer')

st.text('To view data, select a state.')
st.text('Data is currently only available for NOMS domain, but ACCESS tab is visible for testing.')

#Initialize
state_select = 'Select State'

@st.cache_data
def load_data():
    data = vutil.viz_data_get()
    return data

@st.cache_data
def load_states():
    data = vutil.url_data_get()
    return data

states = load_states()

state_select = st.selectbox(
        "Which state's data would you like to review?",
        ('Select State',)+tuple(states['state_name'].unique()))

data = load_data()

domains = ["NOMS", "ACCESS"]

if state_select != 'Select State':
    data = data[data.state_name == state_select]
    
    tab1, tab2= st.tabs(domains)
    tabs = [tab1,tab2]

    for i in range(0,len(domains),1):
        domain_data = data[data.domain == domains[i]]

        with tabs[i]:
            for table in domain_data['table_name'].unique().tolist(): 
                table_data = domain_data[domain_data.table_name == table]
                with st.expander(table):
                    for metric in table_data['metric_name'].unique().tolist():
                        st.header(metric)
                        ch = alt.Chart(table_data[table_data['metric_name']==metric]).mark_line().encode(x='year',y='metric_result',text='state_name')
                        st.altair_chart(ch, use_container_width=True)
                        st.divider()




import streamlit as st
import pandas as pd
import numpy as np
import viz_utility as vutil

st.title('MH URS Parsinator - Data Review')

@st.cache_data
def load_data(domain):
    data = vutil.viz_data_get(domain)
    return data

domain_select = st.selectbox(
    'What domain would you like to review?',
    ('Select Domain','NOMS'))

data_load_state = st.text('Loading data...')
data = load_data(domain_select)
data_load_state.text("Done! (using st.cache_data)")

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

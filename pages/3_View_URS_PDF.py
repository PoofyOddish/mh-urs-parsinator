import streamlit as st
import streamlit.components.v1 as components
import viz_utility as vutil

st.title('View URS PDFs')
st.text("I wanted to embed the URS PDFs straight from SAMHSA, but that's not working.")
st.text("Use below options to get an appropriate link to the URS PDF you would like to see.")

#Initialize
state_select = 'Select State'

@st.cache_data
def load_data():
    data = vutil.url_data_get()
    return data

data = load_data()

if not data.empty:
    state_select = st.selectbox(
        "Which state's URS PDF would you like to review?",
        ('Select State',)+tuple(data['state_name'].unique()))
    
if state_select != 'Select State':
    st.subheader('URS Links')
    st.write(data[['year','url']][data.state_name==state_select])



#components.iframe("https://www.samhsa.gov/data/sites/default/files/reports/rpt39371/Alabama.pdf",height=500,scrolling=True)
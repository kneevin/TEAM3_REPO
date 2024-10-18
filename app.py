import requests
import streamlit as st

GET_GRAPH_TYPES = r'http://127.0.0.1:8000/get_graph_types'

st.write("TEAM 3: ADVANCED DASHBOARDING")
if 'graph_types' not in st.session_state:
    st.graph_types = []

@st.dialog("Data Ingestion")
def upload_csv():
    reason = st.file_uploader(
        "Upload .csv file",
        type=['csv'])
    if st.button("Upload"):
        data = requests.get(GET_GRAPH_TYPES).json()
        st.graph_types = list(data.keys())
        st.rerun()


with st.sidebar:
    if st.button("Upload Data Files"):
        upload_csv()




st.write(st.graph_types)
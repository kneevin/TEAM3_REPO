import streamlit as st
from menu import menu
import requests
import pandas as pd

st.title("Upload Data")
menu()

def upload_df(csv_fname):
    fname = csv_fname.name
    url = r'http://127.0.0.1:8000/upload_csv'
    with open(fname, 'rb') as fp:
        res = requests.post(
            url, 
            data={ 'filename': fname, "type": "multipart/form-data" },
            files = {"file": fp}
        )

def display_files(csv_fname):
    if not csv_fname: return

    with open(csv_fname.name) as fp:
        df = pd.read_csv(fp)

    with st.container():
        st.dataframe(
            df,
            use_container_width=True
        )
        st.button("Confirm Table", on_click=lambda : upload_df(csv_fname))



with st.form('csv-file', clear_on_submit=True):
    csv_file = st.file_uploader(
        label="Upload CSV File Here",
        type=['csv'],

    )
    submitted = st.form_submit_button(label="Upload")

if submitted:
    display_files(csv_file)
        


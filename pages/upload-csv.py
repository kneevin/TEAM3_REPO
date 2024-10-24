import streamlit as st
from menu import menu
import pandas as pd

st.title("Upload Data")
menu()

def display_files(csv_fname):
    if not csv_fname: return

    with open(csv_fname.name) as fp:
        df = pd.read_csv(fp)

    with st.container():

        st.dataframe(
            df,
            use_container_width=True
        )



with st.form('csv-file', clear_on_submit=True):
    csv_file = st.file_uploader(
        label="Upload CSV File Here",
        type=['csv'],

    )
    submitted = st.form_submit_button(label="Upload")

if submitted:
    display_files(csv_file)
        


import streamlit as st

def divider():
    with st.sidebar: 
        st.divider()

def team_section():
    with st.sidebar:
        st.title("Team 3 Repository")
        st.page_link("app.py", label="About Us")
        st.page_link("pages/integration-guide.py", label="Integration Guide")

def data_section():
    with st.sidebar:
        st.title("Data")
        st.page_link("pages/view-data.py", label="View Tables")
        st.page_link("pages/upload-csv.py", label="Upload Data")


def dashboard_section():
    with st.sidebar:
        st.title("Dashboarding")
        st.page_link("pages/create-dashboard.py", label="Create Dashboard")
        st.page_link("pages/view-dashboards.py", label="View Dashboards")


def menu():
    team_section()
    divider()

    data_section()
    divider()

    dashboard_section()
    divider()


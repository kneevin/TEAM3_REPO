import streamlit as st
from menu import menu
import json

menu()

st.title("Team 3 Dashboarding")

# members = [
#     "Kevin Le",
#     "Gurjot "
# ]
st.header("Team Members")
st.markdown("""We are team 3:

- Gurjot Chohan (GKC20000@utdallas.edu)
- Joey Huynh (JHH190004@utdallas.edu)
- Kevin Le (KKL190000@utdallas.edu)
- Charles Simmons (CLS200010@utdallas.edu)
- Dylan Tran (DTT190001@utdallas.edu)""")


st.header("High-Level Summary")
st.markdown(
"""This project implements a comprehensive dashboard management application that allows users to upload, visualize, and manage data through an interactive and user-friendly interface. The application provides several core functionalities, ranging from dashboard and tile management to robust file handling and visualization capabilities. Key features include:

- **Dashboard and Tile Management**: Users can create, view, and delete dashboards and tiles. Tiles support various chart types, including bar, line, and pie charts, with customization options for axes and data points.
- **File Management**: Users can upload, select, and parse CSV files to generate visualizations. IPython notebook integration allows users to upload notebooks and extract plots for dashboard use.
- **Chart Generation and Data Visualization**: Users can generate charts based on their CSV data and toggle between raw data views and graph views. The application supports basic charts (bar, line, pie), with plans for future enhancements such as scatter plots and heatmaps.
- **Navigation and Local Storage**: Users can navigate seamlessly between different pages and persist their dashboard configurations across sessions using browser local storage.
- **Error Handling and Pagination**: Error handling is planned for future development to manage issues like file upload errors. Users can also paginate through large datasets within the data table.
- **Backend Integration**: The FastAPI backend and JSON server integration enable file uploads, dashboard state persistence, and the retrieval of saved data. The backend efficiently responds to requests from the frontend for data and plot display.
  
The app has been thoroughly tested, and most core functionalities have been implemented and completed. Future enhancements will focus on improving user experience, adding new chart types, and enhancing error handling.
"""
)


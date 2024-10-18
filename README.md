# Team 3 Repository (Dashboarding)

The team members are:

- Gurjot Chohan (GKC20000@utdallas.edu)
- Joey Huynh (JHH190004@utdallas.edu)
- Kevin Le (KKL190000@utdallas.edu)
- Charles Simmons (CLS200010@utdallas.edu)
- Dylan Tran (DTT190001@utdallas.edu)

## Table of Contents

- [High Level Summary](#high-level-summary)
- [Functional Requirements](#functional-requirements)
- [Integration Guide](#integration-guide)

## High-Level Summary

This project implements a comprehensive dashboard management application that allows users to upload, visualize, and manage data through an interactive and user-friendly interface. The application provides several core functionalities, ranging from dashboard and tile management to robust file handling and visualization capabilities. Key features include:

- **Dashboard and Tile Management**: Users can create, view, and delete dashboards and tiles. Tiles support various chart types, including bar, line, and pie charts, with customization options for axes and data points.
- **File Management**: Users can upload, select, and parse CSV files to generate visualizations. IPython notebook integration allows users to upload notebooks and extract plots for dashboard use.
- **Chart Generation and Data Visualization**: Users can generate charts based on their CSV data and toggle between raw data views and graph views. The application supports basic charts (bar, line, pie), with plans for future enhancements such as scatter plots and heatmaps.
- **Navigation and Local Storage**: Users can navigate seamlessly between different pages and persist their dashboard configurations across sessions using browser local storage.
- **Error Handling and Pagination**: Error handling is planned for future development to manage issues like file upload errors. Users can also paginate through large datasets within the data table.
- **Backend Integration**: The FastAPI backend and JSON server integration enable file uploads, dashboard state persistence, and the retrieval of saved data. The backend efficiently responds to requests from the frontend for data and plot display.
  
The app has been thoroughly tested, and most core functionalities have been implemented and completed. Future enhancements will focus on improving user experience, adding new chart types, and enhancing error handling.

## Functional Requirements

### Dashboard Management

**Description:**  
Users should be able to manage dashboards by creating, viewing, and deleting them.

**Status:**  
*Completed*

**Status Report:**  

- Users can now:
  - Create new dashboards
  - View existing dashboards
  - Delete dashboards as needed
- Initial testing shows that these features work as expected, with no major bugs or issues identified.
- The system handles multiple dashboards efficiently.
- Future enhancements could focus on:
  - Improving the user interface
  - Adding more management features

### Functional Requirement: Tile Management

**Description:**  
Users should be able to manage individual dashboard tiles, adding new tiles, deleting tiles, and viewing tiles in various chart types (e.g., bar, line, pie).

**Status:**  
*Pending Completion*

**Status Report:**  
Users can now add, view, and delete tiles within their dashboards. Various chart types, including bar, line, and pie charts, are available for visualization. The system operates as expected with standard datasets, and no critical issues were encountered during testing. Enhancements for tile customization and further chart types may be considered in future iterations.

### Functional Requirement: File Management

**Description:**  
Users can upload, select, and parse CSV files for chart creation. This includes the ability to upload new CSV files, select previously uploaded files, and parse them for data extraction.

**Status:**  
*Completed*

**Status Report:**  
Users are able to upload CSV files, select previously uploaded files, and parse them for chart creation. Basic functionality has been verified through manual checks, and the feature appears to be working as expected. Further formal testing can be conducted as needed.

### Functional Requirement: Chart Generation

**Description:**  
Users can generate various types of charts (bar, line, pie) by selecting relevant columns from their uploaded CSV data for visualization. The application allows users to customize the X and Y axes and select multiple Y-axis data points for comparison.

**Status:**  
*Completed*

**Status Report:**  
Users can successfully create charts using data from uploaded CSV files and customize the chart types and axis settings. Basic tests show that the system handles multiple chart types and axis customizations as expected. Minor visual optimizations may be required in future iterations.

**Comments:**  
Current functionality supports basic chart types (bar, line, pie). Future enhancements could include more advanced charts like scatter plots or heatmaps.

### Functional Requirement: Data Visualization

**Description:**  
Users can toggle between a data table view and a graph view to visualize CSV data. The data table displays the raw CSV data, while the graph view presents a chart generated from the selected data.

**Status:**  
*Completed*

**Status Report:**  
Users are able to seamlessly toggle between the data table and the graph view, allowing them to visualize the CSV data in either form. The feature has been tested and is functioning as expected.

### Functional Requirement: Pagination for Data Tables

**Description:**  
Users can paginate through large datasets in the data table, with options to control how many rows are displayed per page for better navigation through the data.

**Status:**  
*Completed*

**Status Report:**  
Users can efficiently navigate through large datasets by selecting how many rows to display per page. The feature has been tested and performs well for typical dataset sizes.

### Functional Requirement: Local Storage

**Description:**  
The dashboard’s state, including tiles and configurations, is saved to the browser’s local storage to ensure that data persists between user sessions without requiring server-side storage.

**Status:**  
*Completed*

**Status Report:**  
Users can now preserve their dashboard state, including tiles and configurations, between sessions. Manual tests show that the data persists after refreshing or closing the browser. No major issues were encountered, and the feature operates as intended.

### Functional Requirement: Navigation

**Description:**  
The app allows users to navigate between different pages, including the landing page, individual dashboards, and the tile creation page. Users can easily return to the main dashboard view from any sub-page.

**Status:**  
*Completed*

**Status Report:**  
Users can smoothly transition between the landing page, individual dashboard views, and the tile creation page. Testing has shown that the navigation is intuitive and responsive.

### Functional Requirement: Error Handling

**Description:**  
The app should handle various types of errors, such as issues during file uploads or problems during chart generation, and provide appropriate feedback to the user.

**Status:**  
*Future*

**Status Report:**  
The error handling system is currently planned for future development. The app will implement error detection for common issues, such as invalid file formats during upload or incorrect data

### Functional Requirement: JSON Server Integration

**Description:**  
The app integrates with a JSON server to handle file uploads, file retrieval, and dashboard state persistence. This enables the app to upload and fetch data, as well as store dashboards and their states.

**Status:**  
*Completed*

**Status Report:**  
JSON server integration has been fully implemented. Users can now upload files, retrieve file content, and persist dashboard states on the server. The functionality has been tested, and both file upload and retrieval operations are working as expected.

### Functional Requirement: IPython Notebook Integration

**Description:**  
The app is able to accept IPython notebooks as input and save the plots from the notebook to local storage for use in the dashboards.

**Status:**  
*Completed*

**Status Report:**  
Users can now upload IPython notebooks, and the system extracts the relevant plots for use in dashboards. The feature has been tested and works well with a range of notebook configurations. There are no known critical issues.

### Functional Requirement: FastAPI Backend

**Description:**  
The FastAPI backend is able to search through the saved plots at the request of the React frontend and send them in a response back to the frontend for display in the dashboard.

**Status:**  
*Completed*

**Status Report:**  
The FastAPI backend has been successfully integrated with the frontend. It responds to requests from the React app to retrieve saved plots for display in the dashboard.

## Integration Guide

Here's the steps to spinning up the backend API locally. First, make sure Python's installed then make sure you're in the repository directory and type the following:

```console
python -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
```

To run the backend, simply type

```console
fastapi dev backend.py
```

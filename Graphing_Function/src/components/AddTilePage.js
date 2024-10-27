import { useParams, useNavigate } from 'react-router-dom';
import Graph from './Graph';
import DataTable from './DataTable';
import { useEffect } from 'react';
import { Box, Tab, Tabs, FormControl, MenuItem, InputLabel, Select, Typography, Button, AppBar, Toolbar, Container } from '@mui/material';
import { TabPanel, TabContext } from '@mui/lab';
import TextField from '@mui/material/TextField';
import Autocomplete from '@mui/material/Autocomplete';
import React, {useState } from "react";
import CSVReader from 'react-csv-reader';
import Papa from 'papaparse';
import axios from 'axios';

function AddTilePage({ dashboards, setDashboards }) {
  const { dashboardId } = useParams();
  const navigate = useNavigate();
  const [fileUploaded, setFileUploaded] = useState(false);
  const [file, setfile] = useState('');
  const [savedFiles, setSavedFiles] = useState([]);
  const [headers, setHeaders] = useState([]);
  const [selectedFile, setSelectedFile] = useState('');
  const [chartType, setChartType] = useState('');
  const [y, sety] = useState([]);
  const [x, setx] = useState([]);
  const [activeTab, setActiveTab] = useState('1');
  const [data, setData] = useState([]);
  const [selected, setSelected] = useState([]);
  const handleChange = (event, value) => setSelected(value);
  const handleChartTypeChange = (e) => {
    setChartType(e.target.value);
  };

  useEffect(() => {
    sety(selected.map(z => z.value));
  }, [selected]);

  useEffect(() => {
    fetchSavedFiles();
  }, [file]);

  useEffect(() => {
    const fetchdata = async () => {
    try {
      // Assuming your backend has a GET /tables endpoint to retrieve saved tables
      const response = await axios.get(`http://127.0.0.1:8000/get_column/${selectedFile}`);
        setData(response.data.rows); // Assuming response contains a list of tables
        setHeaders(response.data.headers);
        setFileUploaded(true);
    } catch (error) {
      console.error('Error fetching table data:', error);
    }
    };

    fetchdata();
  }, [selectedFile]);

  const fetchSavedFiles = async () => {
    try {
      // Assuming your backend has a GET /tables endpoint to retrieve saved tables
      const response = await axios.get('http://127.0.0.1:8000/get_tables');
      
      if (response.status === 200) {
        setSavedFiles(response.data['table names']); // Assuming response contains a list of tables
      }
      console.log(response.data['table names'])
    } catch (error) {
      console.error('Error fetching saved tables:', error);
    }
  };

  

  const addfiles = async (file) => {
    if (!file) {
      return;
    }
  
    const formData = new FormData();
    formData.append('file', file);
  
    try {
      // Sending file to the backend via the POST /upload_csv endpoint
      const response = await axios.post('http://127.0.0.1:8000/upload_csv', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

        const fileData = file
        fetchSavedFiles();
        console.log(fileData);
        setSelectedFile(file.name.split('.')[0]); // Set the file name
       
    } catch (error) {
      console.error('Error uploading file:', error);
    }
    setfile(''); // Reset file input after uploading
  };
  

  const handleFileSelect = (event) => {
    const selectedFileName = event.target.value;
    setSelectedFile(selectedFileName);
  };

  const handleAddTile = () => {
    if (selectedFile !== '' && chartType !== '' && x !== '' && y !== null) {
      const updatedDashboards = dashboards.map(dashboard => {
        if (dashboard.id === parseInt(dashboardId)) {
          return {
            ...dashboard,
            tiles: [...dashboard.tiles, { id: Date.now(), filename: selectedFile, graph_type: chartType, x_axis: x, y_axis: y }]
          };
        }
        return dashboard;
      });
      setSelected('');
      setx([]);
      sety([]);
      setChartType('');
      setData([]);
      setHeaders([]);
      setDashboards(updatedDashboards);
      //localStorage.setItem('dashboards', JSON.stringify(updatedDashboards));
      navigate(`/${dashboardId}`);
    }
  };

  const handleTabChange = (event, newValue) => {
    setActiveTab(newValue);
  };

  return (
    <div>
      {/* AppBar at the top */}
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6">
            Chart Generator for CSV
          </Typography>
        </Toolbar>
      </AppBar>

      {/* Main Container */}
      <Container>
        {/* File Upload Section */}
        <Box mt={4}>
          <FormControl fullWidth>
            <InputLabel id="file-select-label">Select File</InputLabel>
            <Select
              labelId="file-select-label"
              value={selectedFile}
              label="Select File"
              onChange={handleFileSelect}
            >
              <MenuItem value="">
                <em>Placeholder</em>
              </MenuItem>
              {savedFiles.map((file, index) => (
                <MenuItem key={index} value={file}>
                  {file}
                </MenuItem>
              ))}
            </Select>

            {/* CSV Reader */}
            <Box mt={2}>
            <input
              type="file"
              accept=".csv"
              onChange={(e) => {
                const file = e.target.files[0]; // Get the selected file
                addfiles(file); // Pass the file to the addfiles function
              }}
            />
          </Box>
          </FormControl>
        </Box>

        {/* Tabs for Data and Graph Display */}
        {fileUploaded && (
          <Box mt={4}>
            <TabContext value={activeTab}>
              <Tabs value={activeTab} onChange={handleTabChange} aria-label="navigation tabs">
                <Tab label="Table" value="1" />
                <Tab label="Graphs" value="2" />
              </Tabs>

              {/* Data Table Tab */}
              <TabPanel value="1">
                {console.log(data)}
                <DataTable headers={headers} data={data} />
              </TabPanel>

              {/* Graph Tab */}
              <TabPanel value="2">
                <FormControl fullWidth sx={{ m: 1, minWidth: 300 }}>
                  <InputLabel id="chart_type">Chart Type</InputLabel>
                  <Select
                    labelId="chart_type"
                    value={chartType}
                    label="Chart Type"
                    onChange={(e) => setChartType(e.target.value)}
                  >
                    <MenuItem value="bar">Bar Chart</MenuItem>
                    <MenuItem value="line">Line Chart</MenuItem>
                    <MenuItem value="pie">Pie Chart</MenuItem>
                  </Select>
                </FormControl>

                <FormControl fullWidth sx={{ m: 1, minWidth: 300 }}>
                  <InputLabel id="x_value">X-Axis</InputLabel>
                  <Select
                    labelId="x_value"
                    value={x}
                    label="X-Axis"
                    onChange={(e) => setx(e.target.value)}
                  >
                    {headers.map((header, index) => (
                      <MenuItem key={index} value={index}>
                        {header}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>

                <FormControl fullWidth sx={{ m: 1, minWidth: 300 }}>
                  <Autocomplete
                    multiple
                    id="checkboxes-tags-demo"
                    options={headers.map((header, index) => ({ label: header, value: index }))}
                    disableCloseOnSelect
                    onChange={handleChange}
                    getOptionLabel={(option) => option.label}
                    value={selected}
                    isOptionEqualToValue={(option, value) => option.value === value.value}
                    renderInput={(params) => (
                      <TextField {...params} label="Y-Axis" placeholder="Y-Axis" />
                    )}
                  />
                </FormControl>

                {/* Graph Component */}
                <Graph headers= {headers} data={data} chartType={chartType} x={x} y={y} />
                              {/* Button to Add Tile */}
              <Box mt={2}>
                {(selectedFile !== '' && chartType !== '' && x !== '' && y !== null) && 
                <Button variant="contained" onClick={handleAddTile}>
                  Add Tile to Dashboard
                </Button>}
              </Box>
              </TabPanel>
            </TabContext>
          </Box>
        )}
      </Container>
    </div>
  );
}

export default AddTilePage;

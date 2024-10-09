import { useParams, useNavigate } from 'react-router-dom';
import Graph from './Graph';
import DataTable from './DataTable';
import { useEffect } from 'react';
import { Box, Tab, Tabs, FormControl, MenuItem, InputLabel, Select, Typography, Button, AppBar, Toolbar, Container } from '@mui/material';
import { TabPanel, TabContext } from '@mui/lab';
import TextField from '@mui/material/TextField';
import Autocomplete from '@mui/material/Autocomplete';
import React, { useContext, useState } from "react";
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

  const fetchSavedFiles = async () => {
    try {
      const response = await axios.get('http://localhost:5002/files');
      setSavedFiles(response.data);
    } catch (error) {
      console.error('Error fetching saved files:', error);
    }
  };

  const addfiles = (file) => {
    if (!file) {
      return;
    }

    Papa.parse(file, {
      header: false,
      complete: async (result) => {
        const fileData = {
          fileName: file.name,
          data: result.data,
          uploadedAt: new Date().toISOString(),
        };
        try {
          const response = await axios.post('http://localhost:5002/files', fileData);

          if (response.status === 201) {
            fetchSavedFiles();
            setFileUploaded(true);
            setData(fileData.data);
            setHeaders(fileData.data[0]);
            setSelectedFile(fileData.fileName);
          }
        } catch (error) {
          console.error('Error uploading file:', error);
        }
      },
      skipEmptyLines: true,
    });
    setfile('');
  };

  const handleFileSelect = (event) => {
    const selectedFileName = event.target.value;
    setSelectedFile(selectedFileName);

    const file = savedFiles.find(f => f.fileName === selectedFileName);
    if (file) {
      setData(file.data);
      setFileUploaded(true);
      setHeaders(file.data[0]);
    }
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
      localStorage.setItem('dashboards', JSON.stringify(updatedDashboards));
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
                <MenuItem key={index} value={file.fileName}>
                  {file.fileName}
                </MenuItem>
              ))}
            </Select>

            {/* CSV Reader */}
            <Box mt={2}>
              <CSVReader onFileLoaded={(data, fileInfo, file) => { addfiles(file); }} />
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
                <DataTable data={data} />
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
                <Graph data={data} chartType={chartType} x={x} y={y} />
              </TabPanel>

              {/* Button to Add Tile */}
              <Box mt={2}>
                <Button variant="contained" onClick={handleAddTile}>
                  Add Tile to Dashboard
                </Button>
              </Box>
            </TabContext>
          </Box>
        )}
      </Container>
    </div>
  );
}

export default AddTilePage;

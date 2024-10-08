import { useParams, useNavigate } from 'react-router-dom';
import Graph from './Graph';
import DataTable from './DataTable';
import { useEffect } from 'react';
import { Box, Tab, Tabs, FormControl, MenuItem,InputLabel, Select, Typography, Button} from '@mui/material';
import { TabPanel, TabContext } from '@mui/lab';
import TextField from '@mui/material/TextField';
import Autocomplete from '@mui/material/Autocomplete';
import CheckBoxOutlineBlankIcon from '@mui/icons-material/CheckBoxOutlineBlank';
import CheckBoxIcon from '@mui/icons-material/CheckBox';
import React, { useContext, useState } from "react";
import CSVReader from 'react-csv-reader';
import { AppBar, Toolbar, Container } from '@mui/material';
import Papa from 'papaparse';
import axios from 'axios';

function AddTilePage({ dashboards, setDashboards }) {
  const { dashboardId } = useParams(); // Get the dashboardId from the URL
  const navigate = useNavigate();
  const [fileUploaded, setFileUploaded] = useState(false);
  const [file, setfile] = useState(); 
  const [savedFiles, setSavedFiles] = useState([]);
  const [headers, setHeaders] = useState([]);
  const [selectedFile, setSelectedFile] = useState('');
  const [chartType, setChartType] = useState('');
  const [y, sety] = useState([]);
  const [x, setx] = useState([]);
  const [activeTab, setActiveTab] = useState('1');
  const [data, setData] = useState([]);
  const handleChange = (event, value) => setSelected(value);
  const handleChartTypeChange = (e) => {
    setChartType(e.target.value);
  };

  const handleTabChange = (event, newValue) => {
    setActiveTab(newValue);
  };

  const [selected, setSelected] = useState([]);
  useEffect(() => {
    sety(selected.map(z => z.value))
}, [selected])

  useEffect(() => {
    fetchSavedFiles();
  }, [file]);
  

  const fetchSavedFiles = async () => {
    try {
      const response = await axios.get('http://localhost:5002/files');
      setSavedFiles(response.data);
      console.log(savedFiles);
    } catch (error) {
      console.error('Error fetching saved files:', error);
    }
  };
  // Function to add a new dashboard
  const addfiles =  (file) => {
    if (!file) {
      console.log("fail"); 
      return;
    }
     
      Papa.parse(file, {
        header: false, // Parse CSV with headers
        complete: async (result) => {
          const fileData = {
            fileName: file.name,
            data: result.data,
            uploadedAt: new Date().toISOString(),
          };
          try {
            // POST the file data to the backend (json-server)
            const response = await axios.post('http://localhost:5002/files', fileData);

            if (response.status === 201) {
              console.log('File(s) uploaded successfully!');
              fetchSavedFiles(); // Refresh the saved files list
              setFileUploaded(true); 
              setData(fileData.data); 
              setHeaders(fileData.data[0]) ; 
              //console.log(fileData.data)
              setSelectedFile(fileData.fileName);
            } else {
              console.log('Error saving file data.');
            }
          } catch (error) {
            console.error('Error uploading file:', error);
            console.log('Error uploading file.');
          }
        },
        skipEmptyLines: true,
        

    });
    //setData(''); 
    setfile(''); 
  };

  const handleFileSelect = (event) => {
    const selectedFileName = event.target.value;
    setSelectedFile(selectedFileName);

    const file = savedFiles.find(f => f.fileName === selectedFileName);
    if (file) {
      
      setData(file.data); // Update the data variable with parsed CSV data
      setFileUploaded(true); 
      setHeaders(file.data[0]) ; 
      console.log(file.data); 
      console.log(headers); 
    }
  };

  const handleAddTile = () => {
      
    if (selectedFile !== '' && chartType !=='' && x !== '' && y !== null) {
      console.log(selectedFile); 
      console.log(x); 
      console.log(y); 
      console.log(chartType); 
      const updatedDashboards = dashboards.map(dashboard => {
        if (dashboard.id === parseInt(dashboardId)) {
          return {
            ...dashboard,
            tiles: [...dashboard.tiles, { id: Date.now(), filename: selectedFile, graph_type: chartType, x_axis: x, y_axis:y }]
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
      localStorage.setItem('dashboards', JSON.stringify(updatedDashboards)); // Update localStorage
      navigate('/landing'); // Navigate back to the main dashboard page
    }
  };

  

  return (
    <div>
      {/* Static AppBar */}
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6">
            Chart Generator for CSV
          </Typography>
        </Toolbar>
      </AppBar>
      <Container>
        {/* First Section: File Upload Card */}
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
          {savedFiles.map((file, index) =>
            (
            <MenuItem key={index} value={file.fileName}>
              {file.fileName}
            </MenuItem>
          )
          )}

        </Select>
        
        
        <CSVReader onFileLoaded={(data, fileInfo, file) => {addfiles(file)}} />
      </FormControl>
          
        </Box>
        {/* Second Section: Tabs and Content */}
        {fileUploaded &&     <Box mt={4}>
    <TabContext value={activeTab}>
      <Tabs value={activeTab} onChange={handleTabChange} aria-label="navigation tabs">
        <Tab label="Table" value="1" />
        <Tab label="Graphs" value="2" />
      </Tabs>

      <TabPanel value="1">
      <DataTable data={data} />
      </TabPanel>

      <TabPanel value="2">
      <FormControl sx={{ m: 1, minWidth: 300 }}>
        <InputLabel id="chart_type">Chart Type</InputLabel>
        <Select
          labelId="chart_type"
          value={chartType}
          label="chart_type"
          onChange={handleChartTypeChange}
        >
          <MenuItem value="bar">Bar Chart</MenuItem>
          <MenuItem value="line">Line Chart</MenuItem>
          <MenuItem value="pie">Pie Chart</MenuItem>
        </Select>
      </FormControl>
      <FormControl sx={{ m: 1, minWidth: 300 }}>
        <InputLabel id="x_value">X-Axis</InputLabel>
        <Select
          labelId="x_value"
          value={x}
          label="X-Axis"
          onChange={(e) => setx(e.target.value)}
        >
            {headers.map((header, index) => (
            <MenuItem value={index}>{header}</MenuItem>
          ))}
        </Select>
      </FormControl>
      <FormControl sx={{ m: 1, minWidth: 300 }}>
      <Autocomplete
        multiple
        id="checkboxes-tags-demo"
        options={headers.map((header, index) => ({label:header, value:index}))}
        disableCloseOnSelect
        onChange={handleChange}
        getOptionLabel={(option) => option.label}
        value={selected}
        isOptionEqualToValue={(option, value) => option.value === value.value}
        renderOption={(props, option, { selected2 }) => {
            const { key, ...optionProps } = props;
            return (
            <ul key={key} {...optionProps}>
                <MenuItem
                style={{ marginRight: 8 }}
                checked={selected2}
                />
                {option.label}
            </ul>
            );
            
        }}
        renderInput={(params) => (
            <TextField {...params} label="Y-Axis" placeholder="Y-Axis" />
        )}
    />
    </FormControl>
      <Graph data={data} chartType={chartType} x = {x} y = {y}/>
      </TabPanel>
      <Button variant="contained" onClick={handleAddTile}>Add Tile to DashBoard</Button>
    </TabContext>
  </Box>
  
    }
        </Container>
    </div>





   
  );
}

export default AddTilePage;

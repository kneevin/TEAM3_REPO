import React, { useContext, useState } from "react";
import { useEffect } from 'react';
import CSVReader from 'react-csv-reader';
import { useNavigate } from 'react-router-dom';
import { AppBar, Toolbar, Typography, Container, Grid, Card, CardContent, Button, Box, Tab, Tabs } from '@mui/material';
import Dashboard from './Dashboard';
import {FormControl, MenuItem, InputLabel,Select} from '@mui/material';
import Papa from 'papaparse';
import axios from 'axios';

const CSVUploader = ({ setData, data}) => {

  const [fileUploaded, setFileUploaded] = useState(false);
  const [graphtype, setGraphtype] = useState('');
  const [x, setX] = useState('');
  const [y, setY] = useState([]); // Copy the y array
  const [file, setfile] = useState(); 
  const [savedFiles, setSavedFiles] = useState([]);
  const [selectedFile, setSelectedFile] = useState('');

  //useEffect(() => {
   // addfiles();
  //}, [file]);

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
    console.log("fail2"); 
      Papa.parse(file, {
        header: true, // Parse CSV with headers
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
              //console.log(fileData.data)
              //setSelectedFile(file.fileName);
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
      console.log(file.data)
      setData(file.data); // Update the data variable with parsed CSV data
      setFileUploaded(true); 
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
        {fileUploaded && <Dashboard data={data} />}
        </Container>
    </div>
  );
};

export default CSVUploader;

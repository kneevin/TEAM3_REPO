import React, { useState } from 'react';
import CSVReader from 'react-csv-reader';
import { useNavigate } from 'react-router-dom';
import { AppBar, Toolbar, Typography, Container, Grid, Card, CardContent, Button, Box, Tab, Tabs } from '@mui/material';
import Dashboard from './Dashboard';


const CSVUploader = ({ setData, data}) => {

    const [fileUploaded, setFileUploaded] = useState(false);

  const handleFileUpload = (data) => {
    setData(data);
    setFileUploaded(true);
  };

  return (
    <div>
      {/* Static AppBar */}
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6">
            React Material-UI File Upload App
          </Typography>
        </Toolbar>
      </AppBar>
      <Container>
        {/* First Section: File Upload Card */}
        <Box mt={4}>
          <Card>
            <CardContent>
              <Typography variant="h5">Upload a CSV File</Typography>
              <CSVReader onFileLoaded={handleFileUpload} />
            </CardContent>
          </Card>
        </Box>
        {/* Second Section: Tabs and Content */}
        {fileUploaded && <Dashboard data={data} />}
        </Container>
    </div>
  );
};

export default CSVUploader;

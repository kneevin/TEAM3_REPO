import React, { useState, useEffect } from 'react';
import Dashboard from './DashBoard2';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import Modal from '@mui/material/Modal';
import { FormControl } from '@mui/material';
import { alignProperty } from '@mui/material/styles/cssUtils';

const Landing = () => {
// Load dashboards from localStorage or initialize an empty array
const [dashboards, setDashboards] = useState(JSON.parse(localStorage.getItem('dashboards')) || []);
const [dashboardName, setDashboardName] = useState('');
const [open, setOpen] = React.useState(false);
const handleOpen = () => setOpen(true);
const handleClose = () => setOpen(false);

const style = {
  position: 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  width: 200,
  bgcolor: 'background.paper',
  border: '2px solid #000',
  boxShadow: 24,
  display: 'flex',
  alignItems: 'center',
  flexDirection: 'column',
  p: 4,
  m: 1,
  
};
// Persist the dashboards in localStorage whenever they change
useEffect(() => {
  localStorage.setItem('dashboards', JSON.stringify(dashboards));
}, [dashboards]);

// Function to add a new dashboard
const addDashboard = () => {
  if (dashboardName.trim()) {
    setDashboards([
      ...dashboards,
      { id: Date.now(), name: dashboardName, tiles: [] } // Add empty tiles array for each dashboard
    ]);
    setDashboardName('');
    handleClose();
  }
};


// Function to update a specific dashboard's tiles
const updateDashboardTiles = (dashboardId, updatedTiles) => {
  const updatedDashboards = dashboards.map(dashboard =>
    dashboard.id === dashboardId ? { ...dashboard, tiles: updatedTiles } : dashboard
  );
  setDashboards(updatedDashboards);
};

const deleteDashboard = (dashboardId) => {
    const updatedDashboards = dashboards.filter(dashboard => dashboard.id !== dashboardId);
    setDashboards(updatedDashboards);
  };

return (
  <div className="App">
    <h1>Dashboard Creator</h1>
    <Button variant="contained" onClick={handleOpen}>Add Dashboard</Button>
    <Modal open={open} onClose={handleClose} contentLabel="Enter Name">
      <Box sx={style}>
          <Typography id="modal-modal-title" variant="h6" component="h2"> 
          Name Dashboard 
        </Typography>
          <input 
            type="text" 
            value={dashboardName} 
            onChange={(e) => setDashboardName(e.target.value)} 
            placeholder="Enter dashboard name"
          />
          <Box>
          <Button type="submit" onClick={addDashboard}>Save</Button>
          <Button onClick={handleClose}>Cancel</Button></Box>

      </Box>
    </Modal>
    
    <div>
      {dashboards.map((dashboard) => (
        <Dashboard
          key={dashboard.id}
          dashboard={dashboard}
          updateDashboardTiles={updateDashboardTiles}
          deleteDashboard={deleteDashboard}
        />
      ))}
    </div>
  </div>
);
    
};

export default Landing;
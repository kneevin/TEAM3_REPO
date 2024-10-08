import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import AddTilePage from './components/AddTilePage';
import Dashboard from '././components/DashBoard2';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import Modal from '@mui/material/Modal';
import SingleDashboard from './components/SingleDashboard'; 
import TextField from '@mui/material/TextField';

function App() {
  const [data, setData] = useState([]);
  const [dashboards, setDashboards] = useState(JSON.parse(localStorage.getItem('dashboards')) || []);
  
  useEffect(() => {
    localStorage.setItem('dashboards', JSON.stringify(dashboards));
  }, [dashboards]);
  
  const [dashboardName, setDashboardName] = useState('');
  const [open, setOpen] = useState(false);
  
  const handleOpen = () => setOpen(true);
  const handleClose = () => setOpen(false);

  const style = {
    position: 'absolute',
    top: '50%',
    left: '50%',
    transform: 'translate(-50%, -50%)',
    width: 300, // increase the width for better user input experience
    bgcolor: 'background.paper',
    border: '2px solid #000',
    boxShadow: 24,
    display: 'flex',
    alignItems: 'center',
    flexDirection: 'column',
    p: 4,
  };

  const addDashboard = () => {
    if (dashboardName.trim()) {
      setDashboards([
        ...dashboards,
        { id: Date.now(), name: dashboardName, tiles: [] }
      ]);
      setDashboardName('');
      handleClose();
    }
  };

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
    <Router>
      <Routes>
        <Route 
          path="/" 
          element={
            <>
              <Box sx={{ padding: 2 }}>
                <Typography variant="h4" align="center" gutterBottom>
                  Dashboard Center
                </Typography>
                <Box display="flex" justifyContent="center" sx={{ marginBottom: 2 }}>
                  <Button variant="contained" color="primary" onClick={handleOpen}>
                    Add Dashboard
                  </Button>
                </Box>

                <Modal open={open} onClose={handleClose}>
                  <Box sx={style}>
                    <Typography variant="h6" component="h2" align="center">
                      Name Dashboard
                    </Typography>
                    <TextField
                      fullWidth
                      variant="outlined"
                      margin="normal"
                      label="Enter dashboard name"
                      value={dashboardName}
                      onChange={(e) => setDashboardName(e.target.value)}
                    />
                    <Box display="center" justifyContent="space-between" sx={{ marginTop: 2 }}>
                      <Button variant="contained" color="primary" onClick={addDashboard} sx={{ marginRight: 2}}>
                        Save
                      </Button>
                      
                      <Button variant="outlined" onClick={handleClose} sx={{ marginLeft: 2}}>
                        Cancel
                      </Button>
                    </Box>
                  </Box>
                </Modal>

                <Box>
                  {dashboards.map((dashboard) => (
                    <Dashboard
                      key={dashboard.id}
                      dashboard={dashboard}
                      updateDashboardTiles={updateDashboardTiles}
                      deleteDashboard={deleteDashboard}
                    />
                  ))}
                </Box>
              </Box>
            </>
          }
        />
        <Route path="/add-tile/:dashboardId" element={<AddTilePage dashboards={dashboards} setDashboards={setDashboards} />} />
        <Route path="/:dashboardId" element={<SingleDashboard dashboards={dashboards} updateDashboardTiles={updateDashboardTiles} />} />
      </Routes>
    </Router>
  );
}

export default App;

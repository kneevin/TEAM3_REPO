import React, { useState } from 'react';
import Dashboard from './DashBoard';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import Modal from '@mui/material/Modal';
import {useNavigate } from 'react-router-dom';
import TextField from '@mui/material/TextField';

const Landing = ({dashboards = [], setDashboards}) => {
  const navigate = useNavigate();
  
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
      const key =  Date.now(); 
      setDashboards([
        ...dashboards,
        { id: key, name: dashboardName, tiles: [] }
      ] || []);
      setDashboardName('');
      handleClose();
      navigate(`/${key}`); 

    }
  };

  const deleteDashboard = (dashboardId) => {
    const updatedDashboards = dashboards.filter(dashboard => dashboard.id !== dashboardId);
    setDashboards(updatedDashboards || []);
  };

return (
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
                <div>
                  {dashboards.length > 0 ? (
                    dashboards.map((dashboard) => (
                      <Dashboard
                        key={dashboard.id}
                        dashboard={dashboard}
                        deleteDashboard={deleteDashboard}
                      />
                    ))
                  ) : (
                    <p>No dashboards available</p>
                  )}
                </div>
                </Box>
              </Box>
);
    
};

export default Landing;
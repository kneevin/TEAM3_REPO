// Landing.js
import React, { useState } from 'react';
import DashBoard from './DashBoard';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import Modal from '@mui/material/Modal';
import { useNavigate } from 'react-router-dom';
import TextField from '@mui/material/TextField';
import { Tabs, Tab } from '@mui/material';
import DashboardIcon from '@mui/icons-material/Dashboard';
import EditIcon from '@mui/icons-material/Edit';
import AddIcon from '@mui/icons-material/Add';
import SearchIcon from '@mui/icons-material/Search';

const Landing = ({ dashboards = [], layouts = [], setDashboards, setLayouts}) => {
  const navigate = useNavigate();
  const [dashboardName, setDashboardName] = useState('');
  const [open, setOpen] = useState(false);
  const [selectedTab, setSelectedTab] = useState('1'); // Track the active tab

  const handleOpen = () => setOpen(true);
  const handleClose = () => setOpen(false);
  const handleTabChange = (event, newValue) => setSelectedTab(newValue);

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
      const key = Date.now();
      setDashboards([...dashboards, { id: key, name: dashboardName, tiles: [] }]);
      setLayouts([...layouts, { id: key, name: dashboardName, layout: [] }])
      setDashboardName('');
      handleClose();
      navigate(`/${key}`);
    }
  };

  const deleteDashboard = (dashboardId) => {
    const updatedDashboards = dashboards.filter(dashboard => dashboard.id !== dashboardId);
    const updateLayouts = layouts.filter(dashboard => dashboard.id !== dashboardId);
    setDashboards(updatedDashboards);
    setLayouts(updateLayouts); 
  };

  return (
    <Box sx={{ display: 'flex', height: '100vh', backgroundColor: '#ffffff' }}>
      {/* Sidebar */}
      <Box
        sx={{
          width: '250px',
          backgroundColor: '#ffffff',
          borderRight: '1px solid #e0e0e0',
          padding: '20px',
        }}
      >
        {/* Logo */}
        <Box sx={{ padding: '20px 0', marginBottom: '30px' }}>
          <Typography variant="h6" sx={{ color: '#1a1a1a' }}>
            Dashboard
          </Typography>
        </Box>

        {/* Navigation Menu */}
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
          <Button
            startIcon={<DashboardIcon />}
            sx={{
              justifyContent: 'flex-start',
              padding: '12px 16px',
              textTransform: 'none',
              color: '#1a1a1a',
              backgroundColor: selectedTab === '1' ? '#f0f7ff' : 'transparent',
              '&:hover': {
                backgroundColor: '#f0f7ff'
              }
            }}
            onClick={() => setSelectedTab('1')}
          >
            View Dashboards
          </Button>
          <Button
            startIcon={<EditIcon />}
            sx={{
              justifyContent: 'flex-start',
              padding: '12px 16px',
              textTransform: 'none',
              color: '#1a1a1a',
              backgroundColor: selectedTab === '2' ? '#f0f7ff' : 'transparent',
              '&:hover': {
                backgroundColor: '#f0f7ff'
              }
            }}
            onClick={() => setSelectedTab('2')}
          >
            Edit Dashboards
          </Button>
          <Button
            startIcon={<AddIcon />}
            sx={{
              justifyContent: 'flex-start',
              padding: '12px 16px',
              textTransform: 'none',
              color: '#1a1a1a',
              backgroundColor: selectedTab === '3' ? '#f0f7ff' : 'transparent',
              '&:hover': {
                backgroundColor: '#f0f7ff'
              }
            }}
            onClick={handleOpen}
          >
            Add Dashboard
          </Button>
        </Box>
      </Box>
      <Modal 
        open={open} 
        onClose={handleClose}
        sx={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center'
        }}
      >
        <Box
          sx={{
            backgroundColor: '#ffffff',
            borderRadius: '12px',
            padding: '32px',
            width: '400px',
            boxShadow: '0 4px 20px rgba(0,0,0,0.1)',
            border: '1px solid #eaeaea',
            '& .MuiTextField-root': {
              marginTop: '24px',
              marginBottom: '24px',
            }
          }}
        >
          <Typography 
            variant="h6" 
            component="h2" 
            sx={{ 
              color: '#1a1a1a',
              fontWeight: 600,
              marginBottom: '8px'
            }}
          >
            Create New Dashboard
          </Typography>
          
          <Typography 
            variant="body2" 
            sx={{ 
              color: '#666666',
              marginBottom: '16px'
            }}
          >
            Enter a name for your new dashboard
          </Typography>

          <TextField
            fullWidth
            variant="outlined"
            placeholder="Dashboard name"
            value={dashboardName}
            onChange={(e) => setDashboardName(e.target.value)}
            sx={{
              '& .MuiOutlinedInput-root': {
                backgroundColor: '#f8f9fa',
                '&:hover fieldset': {
                  borderColor: '#2196f3',
                },
                '&.Mui-focused fieldset': {
                  borderColor: '#2196f3',
                }
              }
            }}
          />

          <Box 
            sx={{ 
              display: 'flex', 
              justifyContent: 'flex-end', 
              gap: 2,
              marginTop: 3
            }}
          >
            <Button 
              variant="outlined" 
              onClick={handleClose}
              sx={{
                textTransform: 'none',
                borderColor: '#e0e0e0',
                color: '#666666',
                '&:hover': {
                  backgroundColor: '#f8f9fa',
                  borderColor: '#e0e0e0'
                }
              }}
            >
              Cancel
            </Button>
            
            <Button 
              variant="contained" 
              onClick={addDashboard}
              sx={{
                textTransform: 'none',
                backgroundColor: '#2196f3',
                '&:hover': {
                  backgroundColor: '#1976d2'
                }
              }}
            >
              Create Dashboard
            </Button>
          </Box>
        </Box>
      </Modal>
      {/* Main Content */}
      <Box sx={{ 
        flexGrow: 1, 
        backgroundColor: '#f8f9fa',
        padding: '30px',
        overflowY: 'auto'
      }}>
        <Box sx={{ maxWidth: '1200px', margin: '0 auto' }}>
          {/* Content header */}
          <Box sx={{ 
            display: 'flex', 
            justifyContent: 'space-between', 
            alignItems: 'center',
            marginBottom: '30px'
          }}>
            <Typography variant="h5" sx={{ fontWeight: 600 }}>
              {selectedTab === '1' ? 'View Dashboards' : 'Edit Dashboards'}
            </Typography>
            
            {/* Search bar */}
            <TextField
              size="small"
              placeholder="Search..."
              InputProps={{
                startAdornment: <SearchIcon sx={{ color: '#666', mr: 1 }} />,
              }}
              sx={{
                width: '300px',
                '& .MuiOutlinedInput-root': {
                  backgroundColor: '#ffffff',
                  borderRadius: '8px',
                }
              }}
            />
          </Box>

          {/* Dashboard grid */}
          <Box sx={{ 
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))',
            gap: '24px'
          }}>
            {dashboards.map(dashboard => (
              <DashBoard 
                key={dashboard.id} 
                dashboard={dashboard} 
                deleteDashboard={selectedTab === '2' ? deleteDashboard : null} 
              />
            ))}
          </Box>
        </Box>
      </Box>
    </Box>
  );
};

export default Landing;

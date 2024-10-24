import React from 'react';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import { useNavigate } from "react-router-dom";

function DashBoard({ dashboard, deleteDashboard }) {
  const navigate = useNavigate();

  const modalStyle = {
    position: 'absolute',
    top: '50%',
    left: '50%',
    transform: 'translate(-50%, -50%)',
    width: 300, // wider for better input visibility
    bgcolor: 'background.paper',
    border: '2px solid #000',
    boxShadow: 24,
    p: 4,
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
  };

  const viewDashboard = () => {
    navigate(`/${dashboard.id}`); 
  };

  return (
    <Box 
      className="dashboard" 
      sx={{
        border: '1px solid #ddd',
        borderRadius: 2,
        padding: 2,
        marginBottom: 2,
        boxShadow: 3
      }}
    >
      <Typography variant="h5" gutterBottom>
        {dashboard.name}
      </Typography>

      <Box sx={{ display: 'flex', gap: 2, marginBottom: 2 }}>
        <Button 
          variant="contained" 
          color="primary" 
          onClick={viewDashboard}
        >
          View Dashboard
        </Button>
        <Button 
          variant="contained" 
          color="error" 
          onClick={() => deleteDashboard(dashboard.id)}
        >
          Delete Dashboard
        </Button>
      </Box>
      
    </Box>
  );
}

export default DashBoard;

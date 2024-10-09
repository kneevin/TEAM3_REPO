import { useParams, useNavigate } from 'react-router-dom';
import { Box, Typography, Button, TextField } from '@mui/material';
import React, { useState } from "react";
import Modal from '@mui/material/Modal';
import Tile from './Tile';

function SingleDashboard({ dashboards, updateDashboardTiles }) {
  const { dashboardId } = useParams(); // Get the dashboardId from the URL
  const dashboard = dashboards.find(d => d.id === parseInt(dashboardId));

  const [tiles, setTiles] = useState(dashboard.tiles || []);
  const [tileContent, setTileContent] = useState('');
  const [open, setOpen] = useState(false);
  
  const handleOpen = () => setOpen(true);
  const handleClose = () => setOpen(false);
  const navigate = useNavigate();

  const modalStyle = {
    position: 'absolute',
    top: '50%',
    left: '50%',
    transform: 'translate(-50%, -50%)',
    width: 400, // Adjusted width for better layout
    bgcolor: 'background.paper',
    border: '2px solid #000',
    boxShadow: 24,
    p: 4,
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
  };

  // Function to add a new tile
  const addTile = () => {
    navigate(`/add-tile/${dashboard.id}`);
    updateDashboardTiles(dashboard.id, tiles);
  };

  const returnDashboard = () => {
    navigate('/'); 
  };

  const deleteTile = (tileId) => {
    const updatedTiles = tiles.filter(tile => tile.id !== tileId);
    setTiles(updatedTiles);
    updateDashboardTiles(dashboard.id, updatedTiles);
  };

  return (
    <Box sx={{ padding: 2 }}>
      <Typography variant="h4" gutterBottom>
        {dashboard.name}
      </Typography>
      
      <Box sx={{ display: 'flex', gap: 2, marginBottom: 2 }}>
        <Button variant="contained" color="primary" onClick={returnDashboard}>
          Return to Dashboard
        </Button>
        <Button variant="contained" color="secondary" onClick={handleOpen}>
          Add Tile
        </Button>
      </Box>

      <Modal open={open} onClose={handleClose}>
        <Box sx={modalStyle}>
          <Typography variant="h6" component="h2" gutterBottom>
            Add New Tile
          </Typography>
          <TextField
            fullWidth
            variant="outlined"
            margin="normal"
            label="Enter tile content"
            value={tileContent}
            onChange={(e) => setTileContent(e.target.value)}
          />
          <Box sx={{ display: 'flex', gap: 4, marginTop: 2 }}>
            <Button variant="contained" color="primary" onClick={addTile}>
              Save
            </Button>
            <Button variant="outlined" onClick={handleClose}>
              Cancel
            </Button>
          </Box>
        </Box>
      </Modal>

      <Box className="tiles-container" sx={{ display: 'flex', gap: 2, flexWrap: 'wrap', marginTop: 2 }}>
        {tiles.map((tile) => (
          <Tile key={tile.id} tile={tile} deleteTile={() => deleteTile(tile.id)} />
        ))}
      </Box>
    </Box>
  );
}

export default SingleDashboard;

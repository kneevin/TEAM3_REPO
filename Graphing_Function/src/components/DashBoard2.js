import { useState, useEffect } from 'react';
import React from 'react';
import Tile from './Tile';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import Modal from '@mui/material/Modal';
import { useNavigate } from "react-router-dom";

function DashBoard2({ dashboard, updateDashboardTiles, deleteDashboard }) {
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
    width: 300, // wider for better input visibility
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

  const viewDashboard = () => {
    navigate(`/${dashboard.id}`); 
  };

  const deleteTile = (tileId) => {
    const updatedTiles = tiles.filter(tile => tile.id !== tileId);
    setTiles(updatedTiles);
    updateDashboardTiles(dashboard.id, updatedTiles);
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

      {/* Uncomment and style this if you need the Add Tile functionality */}
      {/* <Button variant="contained" color="secondary" onClick={handleOpen}>Add Tile</Button>
        <Modal open={open} onClose={handleClose}>
          <Box sx={modalStyle}>
            <Typography variant="h6" component="h2"> 
              Name Dashboard 
            </Typography>
            <input 
              type="text" 
              value={tileContent} 
              onChange={(e) => setTileContent(e.target.value)} 
              placeholder="Enter dashboard name"
            />
            <Box sx={{ display: 'flex', gap: 2, marginTop: 2 }}>
              <Button variant="contained" color="primary" onClick={addTile}>Save</Button>
              <Button variant="outlined" onClick={handleClose}>Cancel</Button>
            </Box>
          </Box>
        </Modal>
      
      <Box className="tiles-container" sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
        {tiles.map((tile) => (
          <Tile key={tile.id} tile={tile} deleteTile={() => deleteTile(tile.id)} />
        ))}
      </Box> */}
      
    </Box>
  );
}

export default DashBoard2;

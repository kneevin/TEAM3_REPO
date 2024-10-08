import { useParams, useNavigate } from 'react-router-dom';
import { Box,Typography, Button} from '@mui/material';
import React, { useState } from "react";
import Modal from '@mui/material/Modal';
import Tile from './Tile';

function SingleDashboard({ dashboards, updateDashboardTiles }) {
  const { dashboardId } = useParams(); // Get the dashboardId from the URL
   const dashboard = dashboards.find(d => d.id === parseInt(dashboardId));
  
      const [tiles, setTiles] = useState(dashboard.tiles || []);
    const [tileContent, setTileContent] = useState('');
    const [open, setOpen] = React.useState(false);
      const handleOpen = () => setOpen(true);
      const handleClose = () => setOpen(false);
      const navigate = useNavigate();
     
  
      
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
  
    // Function to add a new tile
    const addTile = () => {
      navigate(`/add-tile/${dashboard.id}`);
      updateDashboardTiles(dashboard.id, tiles);
    };
  
    const returnDashboard = () =>{
      navigate('/landing'); 
    }
  
    const deleteTile = (tileId) => {
      const updatedTiles = tiles.filter(tile => tile.id !== tileId);
      setTiles(updatedTiles);
      updateDashboardTiles(dashboard.id, updatedTiles);
    };
  
    return (
      <div className="dashboard">
          <h2>{dashboard.name}</h2>
          <Button variant="contained" onClick={returnDashboard}>return</Button>
          <Button variant="contained" onClick={handleOpen}>Add Tile</Button>
              <Modal open={open} onClose={handleClose} contentLabel="Enter Name">
              <Box sx={style}>
                  <Typography id="modal-modal-title" variant="h6" component="h2"> 
                  Name Dashboard 
                  </Typography>
                  <input 
                      type="text" 
                      value={tileContent} 
                      onChange={(e) => setTileContent(e.target.value)} 
                      placeholder="Enter dashboard name"
                  />
                  <Box>
                  <Button type="submit" onClick={addTile}>Save</Button>
                  <Button onClick={handleClose}>Cancel</Button></Box>
  
              </Box>
              </Modal>

              <div className="tiles-container">
        {tiles.map((tile) => (
          <Tile key={tile.id} tile={tile} deleteTile={() => deleteTile(tile.id)}/>
        ))}
        </div>
          
      
      </div>
    );
  }
export default SingleDashboard;
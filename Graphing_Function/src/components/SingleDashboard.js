import { useParams, useNavigate } from 'react-router-dom';
import { Box, Typography, Button, TextField } from '@mui/material';
import React, { useState } from "react";
import Modal from '@mui/material/Modal';
import Tile from './Tile';
import { Responsive, WidthProvider } from 'react-grid-layout';
import 'react-grid-layout/css/styles.css';
import 'react-resizable/css/styles.css';

const ResponsiveGridLayout = WidthProvider(Responsive);

function SingleDashboard({ dashboards, layouts,  updateDashboardTiles, updateDashboardLayout, setLayouts, setDashboards }) {
  const { dashboardId } = useParams(); // Get the dashboardId from the URL
  const dashboard = dashboards.find(d => d.id === parseInt(dashboardId));

  const [tiles, setTiles] = useState(dashboard.tiles || []);
  const [tileContent, setTileContent] = useState('');
  const [open, setOpen] = useState(false);
  const [currentLayout, setCurrentLayout] = useState(() => {
    const dashboardLayout = layouts.find(layout => layout.id === parseInt(dashboardId));
    return dashboardLayout ? dashboardLayout.layout : generateLayout();
  });

  const [containerWidth, setContainerWidth] = useState(1200);

  const handleOpen = () => setOpen(true);
  const handleClose = () => setOpen(false);
  const navigate = useNavigate();

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

  // Handle layout change
  const onLayoutChange = (layout) => {
    setCurrentLayout(layout);
    // Update the specific layout in the layouts array
    const updatedLayouts = layouts.map(l => {
      if (l.id === parseInt(dashboardId)) {
        return { ...l, layout: layout };
      }
      return l;
    });
    setLayouts(updatedLayouts);
    updateDashboardLayout(dashboard.id, layout);
  };

  // Generate initial layout if none exists
  const generateLayout = () => {
    return tiles.map((tile, index) => ({
      i: tile.id.toString(),
      x: (index * 4) % 12,
      y: Math.floor(index / 3),
      w: 4,
      h: 4,
    }));
  };

  const tileStyle = {
    backgroundColor: '#ffffff',
    borderRadius: '12px',
    boxShadow: '0 4px 6px rgba(0,0,0,0.1)',
    padding: '20px',
    height: 'calc(100% - 20px)',
    width: 'calc(100% - 20px)',
    position: 'relative',
    overflow: 'visible',
    transition: 'box-shadow 0.3s ease',
    '&:hover': {
      boxShadow: '0 6px 12px rgba(0,0,0,0.15)'
    }
  };

  return (
    <Box sx={{ padding: 3, backgroundColor: '#f8f9fa', minHeight: '100vh' }}>
      <Box className="dashboard-header" sx={{ mb: 3, borderRadius: '10px' }}>
        <Typography variant="h4" gutterBottom>
          {dashboard.name}
        </Typography>
        
        <Box sx={{ display: 'flex', gap: 2 }}>
          <Button 
            variant="contained" 
            className="custom-button"
            sx={{ backgroundColor: '#ffffff', color: '#1a237e' }}
            onClick={returnDashboard}
          >
            Return to Dashboard
          </Button>
          <Button 
            variant="contained" 
            className="custom-button"
            sx={{ backgroundColor: '#3949ab' }}
            onClick={handleOpen}
          >
            Add Tile
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
            Add New Tile
          </Typography>
          
          <Typography 
            variant="body2" 
            sx={{ 
              color: '#666666',
              marginBottom: '16px'
            }}
          >
            Choose your visualization type
          </Typography>

          <TextField
            fullWidth
            variant="outlined"
            placeholder="Enter tile content"
            value={tileContent}
            onChange={(e) => setTileContent(e.target.value)}
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
              onClick={addTile}
              sx={{
                textTransform: 'none',
                backgroundColor: '#2196f3',
                '&:hover': {
                  backgroundColor: '#1976d2'
                }
              }}
            >
              Create Tile
            </Button>
          </Box>
        </Box>
      </Modal>

      <ResponsiveGridLayout
        className="layout"
        layouts={{ lg: currentLayout }}
        breakpoints={{ lg: 1200, md: 996, sm: 768, xs: 480, xxs: 0 }}
        cols={{ lg: 12, md: 10, sm: 6, xs: 4, xxs: 2 }}
        rowHeight={100}
        onLayoutChange={onLayoutChange}
        onWidthChange={(width, margin, cols) => {
          setContainerWidth(width);
        }}
        compactType={null}
        preventCollision={false}
        isResizable={true}
        isDraggable={true}
        margin={[20, 20]}
        containerPadding={[20, 20]}
        useCSSTransforms={true}
        draggableCancel=".cancelSelectorName"
      >
        {tiles.map((tile) => {
          const layoutItem = currentLayout.find(item => item.i === tile.id.toString());
          const gridItemWidth = layoutItem ? (layoutItem.w / 12) * containerWidth : undefined;
          
          return (
            <Box 
              key={tile.id.toString()} 
              sx={{
                ...tileStyle,
                position: 'relative',
                overflow: 'visible'
              }}
            >
              <Tile
                tile={tile}
                deleteTile={() => deleteTile(tile.id)}
                dashboards={dashboards}
                setDashboards={setDashboards}
                width={gridItemWidth-45}
                height={layoutItem ? layoutItem.h * 100: undefined}
                layoutItem={layoutItem}
              />
            </Box>
          );
        })}
      </ResponsiveGridLayout>
    </Box>
  );
}

export default SingleDashboard;

import { useParams, useNavigate } from 'react-router-dom';
import { Box, Typography, Button, TextField } from '@mui/material';
import React, { useState } from "react";
import Tile from './Tile';
import { Responsive, WidthProvider } from 'react-grid-layout';
import 'react-grid-layout/css/styles.css';
import 'react-resizable/css/styles.css';

const ResponsiveGridLayout = WidthProvider(Responsive);

function Read_OnlyDash({ dashboards, setDashboards,layouts }) {
  const { dashboardId } = useParams();
  const dashboard = dashboards.find(d => d.id === parseInt(dashboardId));
  const [tiles, setTiles] = useState(dashboard.tiles || []);
  
  // Get the layout configuration for this dashboard
  const dashboardLayout = layouts.find(layout => layout.id === parseInt(dashboardId));
  const currentLayout = dashboardLayout ? dashboardLayout.layout : [];

  const navigate = useNavigate();
  const [containerWidth, setContainerWidth] = useState(1200);
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


  const returnDashboard = () => {
    navigate('/'); 
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
    <Box sx={{ padding: 2 }}>
      <Typography variant="h4" gutterBottom>
        {dashboard.name}
      </Typography>
      
      <Box sx={{ display: 'flex', gap: 2, marginBottom: 2 }}>
        <Button variant="contained" color="primary" onClick={returnDashboard}>
          Return to Dashboard
        </Button>
      </Box>

      <ResponsiveGridLayout
        className="layout"
        layouts={{ lg: currentLayout }}
        breakpoints={{ lg: 1200, md: 996, sm: 768, xs: 480, xxs: 0 }}
        cols={{ lg: 12, md: 10, sm: 6, xs: 4, xxs: 2 }}
        rowHeight={100}
        isDraggable={false}
        onWidthChange={(width, margin, cols) => {
          setContainerWidth(width);
        }}
        isResizable={false}
        compactType={null}
        preventCollision={false}
        margin={[20, 20]}
        containerPadding={[20, 20]}
        useCSSTransforms={true}
      >
        {tiles.map((tile) => {
          const layoutItem = currentLayout.find(item => item.i === tile.id.toString());
          const gridItemWidth = layoutItem ? (layoutItem.w / 12) * containerWidth : undefined;
          return (
            <div key={tile.id.toString()} style={tileStyle}>
              <Tile
                tile={tile}
                deleteTile={null}
                dashboards={dashboards}
                setDashboards={setDashboards}
                width={gridItemWidth -45 }
                height={layoutItem ? layoutItem.h * 100 : undefined}
                layoutItem={layoutItem}
              />
            </div>
          );
        })}
      </ResponsiveGridLayout>
    </Box>
  );
}

export default Read_OnlyDash;

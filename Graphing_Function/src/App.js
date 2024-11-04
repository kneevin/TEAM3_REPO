import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import AddTilePage from './components/AddTilePage';
import Landing from './components/Landing'
import SingleDashboard from './components/SingleDashboard'; 
import Read_OnlyDash from './components/Read_OnlyDash';
import './App.css';


function App() {
  const [dashboards, setDashboards] = useState(() => {
    const storedDashboards = localStorage.getItem('dashboards');
    return storedDashboards ? JSON.parse(storedDashboards) : [];
  });

  const [layouts, setLayouts] = useState(() => {
    const storedLayout = localStorage.getItem('layouts');
    return storedLayout ? JSON.parse(storedLayout) : [];
  });

  useEffect(() => {
    localStorage.setItem('layouts', JSON.stringify(layouts));
  }, [layouts]);


  useEffect(() => {
    localStorage.setItem('dashboards', JSON.stringify(dashboards));
  }, [dashboards]);

  const updateDashboardTiles = (dashboardId, updatedTiles) => {
    const updatedDashboards = dashboards.map(dashboard =>
      dashboard.id === dashboardId ? { ...dashboard, tiles: updatedTiles } : dashboard
    );
    setDashboards(updatedDashboards);
  };

  const updateDashboardLayout = (dashboardId, updatedTilesLayout) => {
    const updatedLayout = layouts.map(layout =>
      layout.id === parseInt(dashboardId) ? { ...layout, layout: updatedTilesLayout } : layout
    );
    console.log(updatedLayout); 
    setLayouts(updatedLayout);
  };

  return (
    <Router>
      <Routes>
        <Route path="/" element={<Landing dashboards={dashboards} layouts= {layouts} setDashboards={setDashboards} setLayouts={setLayouts}/>}/>
        <Route path="/add-tile/:dashboardId" element={dashboards &&  <AddTilePage dashboards={dashboards} layouts= {layouts}  setDashboards={setDashboards} setLayouts={setLayouts}/>} />
        <Route path="/:dashboardId" element={dashboards && <SingleDashboard dashboards={dashboards} layouts= {layouts}  updateDashboardTiles={updateDashboardTiles} updateDashboardLayout={updateDashboardLayout}  setLayouts={setLayouts} setDashboards={setDashboards}/>} />
        <Route path="/read_only/:dashboardId" element={dashboards && <Read_OnlyDash dashboards={dashboards}  setDashboards={setDashboards} layouts= {layouts} />} />
      </Routes>
    </Router>
  );
}

export default App;

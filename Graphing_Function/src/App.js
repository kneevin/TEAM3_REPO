import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import AddTilePage from './components/AddTilePage';
import Landing from './components/Landing'
import SingleDashboard from './components/SingleDashboard'; 


function App() {
  const [dashboards, setDashboards] = useState(() => {
    const storedDashboards = localStorage.getItem('dashboards');
    return storedDashboards ? JSON.parse(storedDashboards) : [];
  });

  useEffect(() => {

    localStorage.setItem('dashboards', JSON.stringify(dashboards));
  }, [dashboards]);

  const updateDashboardTiles = (dashboardId, updatedTiles) => {
    const updatedDashboards = dashboards.map(dashboard =>
      dashboard.id === dashboardId ? { ...dashboard, tiles: updatedTiles } : dashboard
    );
    setDashboards(updatedDashboards);
  };

  return (
    <Router>
      <Routes>
        <Route path="/" element={<> <Landing dashboards={dashboards} setDashboards={setDashboards} /> </>}/>
        <Route path="/add-tile/:dashboardId" element={dashboards &&  <AddTilePage dashboards={dashboards} setDashboards={setDashboards} />} />
        <Route path="/:dashboardId" element={dashboards && <SingleDashboard dashboards={dashboards} updateDashboardTiles={updateDashboardTiles} />} />
      </Routes>
    </Router>
  );
}

export default App;

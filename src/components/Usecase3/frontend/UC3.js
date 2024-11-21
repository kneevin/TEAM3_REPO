import React, {Suspense, useState} from 'react';
import AddTilePage from './components/AddTilePage.js';
import Landing from './components/Landing.js'
import SingleDashboard from './components/SingleDashboard.js'; 
import Read_OnlyDash from './components/Read_OnlyDash.js';
import './UC3.css';
import Loading from "../../../components/loading.js";

function UC3() {
  const [currentView, setCurrentView] = useState('landing');
  const [params, setParams] = useState({});

  const renderComponent = () => {
    switch(currentView) {
      case 'landing':
        return <Landing onNavigate={handleNavigation} />;
      case 'addTile':
        return <AddTilePage dashboardId={params.dashboardId} onNavigate={handleNavigation} />;
      case 'singleDashboard':
        return <SingleDashboard dashboardId={params.dashboardId} onNavigate={handleNavigation} />;
      case 'readOnlyDash':
        return <Read_OnlyDash dashboardId={params.dashboardId} onNavigate={handleNavigation} />;
      default:
        return <Landing onNavigate={handleNavigation} />;
    }
  };

  const handleNavigation = (view, newParams = {}) => {
    setParams(newParams);
    setCurrentView(view);
  };

  return (
      <Suspense
        fallback={
          <div className="h-screen flex justify-center items-center">
            <Loading />
          </div>
        }
      >
        {renderComponent()}
      </Suspense>
  );
}

export default UC3;

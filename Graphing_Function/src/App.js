import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import CSVUploader from './components/CSVUploader';
import Dashboard from './components/Dashboard';

function App() {
  const [data, setData] = useState([]);

  return (
    <Router>
      <Routes>
        <Route path="/" element={<CSVUploader setData={setData} data={data}/>} />
      </Routes>
    </Router>
  );
}

export default App;

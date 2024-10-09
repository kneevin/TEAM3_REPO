import React, { useContext, useState, useEffect } from "react";
import axios from 'axios';
import Graph from './Graph'; 

function Tile({ tile, deleteTile}) {
  const [savedFiles, setSavedFiles] = useState([]);
  const [data, setData] = useState([]);
  useEffect(() => {
    fetchSavedFiles(tile.filename)
}, [])
  const fetchSavedFiles = async (filename) => {
    try {
      const response = await axios.get('http://localhost:5002/files');
      const file = response.data.find(f => f.fileName === filename);
      if (file) {
        setData(file.data); 
        console.log(file.data);
      }
      
    } catch (error) {
      console.error('Error fetching saved files:', error);
    }
  };

  return (
    <div className="tile">
      {data.length !== 0 && <Graph data={data} chartType={tile.graph_type} x = {tile.x_axis} y = {tile.y_axis}></Graph>}
      {console.log(data)}
      <button onClick={deleteTile}>Delete Tile</button>
    </div>
  );
}

export default Tile;

import React, {useState, useEffect } from "react";
import axios from 'axios';
import Graph from './Graph'; 

function Tile({ tile, deleteTile}) {
  const [headers, setHeaders] = useState([]);
  const [data, setData] = useState([]);

useEffect(() => {
  const fetchdata = async () => {
  try {
    // Assuming your backend has a GET /tables endpoint to retrieve saved tables
    const response = await axios.get(`http://127.0.0.1:8000/get_column/${tile.filename}`);
      setData(response.data.rows); // Assuming response contains a list of tables
      setHeaders(response.data.headers);
  } catch (error) {
    console.error('Error fetching table data:', error);
  }
  };

  fetchdata();
}, []);

  return (
    <div className="tile">
      {data.length !== 0 && <Graph headers= {headers} data={data} chartType={tile.graph_type} x = {tile.x_axis} y = {tile.y_axis}></Graph>}
      {console.log(data)}
      <button onClick={deleteTile}>Delete Tile</button>
    </div>
  );
}

export default Tile;

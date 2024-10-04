import React, { useState} from 'react';
import { Bar, Line, Pie } from 'react-chartjs-2';
import { Chart, registerables } from 'chart.js';
Chart.register(...registerables);

const Graph = ({ data, chartType, x, y }) => {
    const [chartData, setChartData] = useState(null);

    const labels = data.map(z => z[x]);
    const values = data.map(row => parseFloat(row[y])); // Adjust to your CSV value column
    

    const generateChart = () => {
        const labels = data.map(row => row[x]);
        const datasets = y.map((col) => ({
          label: data[0][col],
          data: data.map(row => parseFloat(row[col])),
          borderColor: `hsl(${col * 50}, 70%, 50%)`,
          backgroundColor: `hsl(${col * 50}, 70%, 70%)`,
        }));

    
        setChartData({ labels, datasets });
      };
    


  return (
    <div>
    <button onClick={generateChart}>Generate Chart</button>
        {chartData && chartType === 'bar' && <Bar data={chartData} />}
      {chartData && chartType === 'line' && <Line data={chartData} />}
      {chartData && chartType === 'pie' && <Pie data={chartData} />}
    </div>
  );
};

export default Graph;

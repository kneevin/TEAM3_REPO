import React from 'react';
import { Bar, Line, Pie } from 'react-chartjs-2';
import { Chart, registerables } from 'chart.js';
Chart.register(...registerables);

const Graph = ({ data, chartType, x, y }) => {

    const labels = data.map(row => row[x]);
    const datasets = y.map((col) => ({
      label: data[0][col],
      data: data.map(row => parseFloat(row[col])),
      borderColor: `hsl(${col * 50}, 70%, 50%)`,
      backgroundColor: `hsl(${col * 50}, 70%, 70%)`,
    }));
  return (
    <div>
      {chartType === 'bar' && <Bar data={{ labels, datasets }} />}
      {chartType === 'line' && <Line data={{ labels, datasets }} />}
      {chartType === 'pie' && <Pie data={{ labels, datasets }} />}
    </div>
  );
};

export default Graph;

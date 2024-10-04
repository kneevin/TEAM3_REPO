import React from 'react';
import html2canvas from 'html2canvas';
import jsPDF from 'jspdf';

const ExportDashboard = () => {
  const exportToPDF = () => {
    const dashboard = document.getElementById('dashboard');
    html2canvas(dashboard).then((canvas) => {
      const imgData = canvas.toDataURL('image/png');
      const pdf = new jsPDF();
      pdf.addImage(imgData, 'PNG', 0, 0);
      pdf.save('dashboard.pdf');
    });
  };

  return (
    <button onClick={exportToPDF}>Export Dashboard</button>
  );
};

export default ExportDashboard;

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { BrowserRouter as Router, Route, Link, Routes, useNavigate, useParams } from 'react-router-dom';

const UploadFile = () => {
  const [file, setFile] = useState(null);
  const navigate = useNavigate();

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('http://localhost:8000/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      alert('File uploaded successfully');
      const filename = response.data.filename;
      navigate(`/images/${filename}`);
    } catch (error) {
      console.error('Error uploading file:', error);
      alert('Failed to upload file');
    }
  };

  return (
    <div>
      <h1>Upload Notebook (.ipynb)</h1>
      <input type="file" onChange={handleFileChange} accept=".ipynb" />
      <button onClick={handleUpload}>Publish</button>
    </div>
  );
};

const ViewImages = () => {
  const [images, setImages] = useState([]);
  const { filename } = useParams();

  useEffect(() => {
    const fetchImages = async () => {
      try {
        const response = await axios.get(`http://localhost:8000/notebook/${filename}`);
        setImages(response.data);
      } catch (error) {
        console.error('Error fetching images:', error);
      }
    };

    fetchImages();
  }, [filename]);

  return (
    <div>
      <h1>Generated Images from {filename}</h1>
      <div>
        {images.map((imgBase64, index) => (
          <img
            key={index}
            src={`data:image/png;base64,${imgBase64}`}
            alt={`img-${index}`}
            width="300"
          />
        ))}
      </div>
    </div>
  );
};

const NotebookList = () => {
  const [notebooks, setNotebooks] = useState([]);

  useEffect(() => {
    const fetchNotebooks = async () => {
      try {
        const response = await axios.get('http://localhost:8000/notebooks');
        setNotebooks(response.data);
      } catch (error) {
        console.error('Error fetching notebooks:', error);
      }
    };

    fetchNotebooks();
  }, []);

  return (
    <div>
      <h1>Uploaded Notebooks</h1>
      <ul>
        {notebooks.map((notebook, index) => (
          <li key={index}>
            <Link to={`/images/${notebook}`}>{notebook}</Link>
          </li>
        ))}
      </ul>
    </div>
  );
};

const App = () => {
  return (
    <Router>
      <nav>
        <ul>
          <li><Link to="/">Upload Notebook</Link></li>
          <li><Link to="/notebooks">View Notebooks</Link></li>
        </ul>
      </nav>
      <Routes>
        <Route path="/" element={<UploadFile />} />
        <Route path="/images/:filename" element={<ViewImages />} />
        <Route path="/notebooks" element={<NotebookList />} />
      </Routes>
    </Router>
  );
};

export default App;

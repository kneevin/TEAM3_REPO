import { useParams, useNavigate } from 'react-router-dom';
import Graph from './Graph';
import DataTable from './DataTable';
import { useEffect } from 'react';
import { Box, Tab, Tabs, FormControl, MenuItem, InputLabel, Select, Typography, Button, Container, IconButton} from '@mui/material';
import { TabPanel, TabContext } from '@mui/lab';
import TextField from '@mui/material/TextField';
import Autocomplete from '@mui/material/Autocomplete';
import React, { useState } from "react";
import { DateRangePicker } from '@mui/lab';
import axios from 'axios';
import CloseIcon from '@mui/icons-material/Close';
function AddTilePage({ dashboards, layouts, setDashboards, setLayouts}) {
  const { dashboardId } = useParams();
  const navigate = useNavigate();
  const [fileUploaded, setFileUploaded] = useState(false);
  const [file, setFile] = useState('');
  const [savedFiles, setSavedFiles] = useState([]);
  const [headers, setHeaders] = useState([]);
  const [columnTypes, setColumnTypes] = useState({}); // State to store column data types
  const [selectedFile, setSelectedFile] = useState('');
  const [chartType, setChartType] = useState('');
  const [y, setY] = useState([]);
  const [x, setX] = useState([]);
  const [activeTab, setActiveTab] = useState('1');
  const [data, setData] = useState([]);
  const [filteredData, setFilteredData] = useState([]);
  const [filters, setFilters] = useState({});
  const [selected, setSelected] = useState([]);
  const handleChange = (event, value) => setY(value);
  const handleChartTypeChange = (e) => setChartType(e.target.value);
  const [selectedColumn, setSelectedColumn] = useState(null);
  const [filterValue, setFilterValue] = useState(null);
  useEffect(() => {
    setY(selected.map(z => z.value));
  }, [selected]);

  useEffect(() => {
    fetchSavedFiles();
  }, [file]);


  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get(`http://127.0.0.1:8000/get_column/${selectedFile}`);
        setData(response.data.rows);
        setHeaders(response.data.headers);
        determineColumnTypes(response.data.rows);
        setFileUploaded(true);
      } catch (error) {
        console.error('Error fetching table data:', error);
      }
    };

    fetchData();
  }, [selectedFile]);

  // Apply filters when data or filters change
  useEffect(() => {
    applyFilters();
  }, [data, filters]);

  const fetchSavedFiles = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:8000/get_tables');
      if (response.status === 200) {
        setSavedFiles(response.data['table names']);
      }
    } catch (error) {
      console.error('Error fetching saved tables:', error);
    }
  };

  const addFiles = async (file) => {
    if (!file) return;
    const formData = new FormData();
    formData.append('file', file);
    try {
      await axios.post('http://127.0.0.1:8000/upload_csv', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      fetchSavedFiles();
      setSelectedFile(file.name.split('.')[0]);
    } catch (error) {
      console.error('Error uploading file:', error);
    }
    setFile('');
  };

  // Determine column data types by inspecting the data
  const determineColumnTypes = (data) => {
    const types = {};
    data[0].forEach((value, index) => {
      if (!isNaN(value)) {
        types[index] = 'number';
      } else if (Date.parse(value)) {
        types[index] = 'date';
      } else {
        types[index] = 'string';
      }
    });
    setColumnTypes(types);
  };

  const applyFilters = () => {
    const filtered = data.filter(row => {
      // Check if the row satisfies all filters
      return Object.keys(filters).every(column => {
        const filterValues = filters[column];
        const columnType = columnTypes[column];
        
        if (!filterValues || filterValues.length === 0) {
          return true; // No filter for this column, so include the row
        }
  
        // Check if row satisfies at least one of the filter values
        return filterValues.some(value => {
          if (columnType === 'number') {
            const [min, max] = value;
            return (!min || row[column] >= min) && (!max || row[column] <= max);
          } else if (columnType === 'date') {
            const [startDate, endDate] = value;
            return (!startDate || new Date(row[column]) >= new Date(startDate)) &&
                   (!endDate || new Date(row[column]) <= new Date(endDate));
          } else {
            // String filter
            return row[column].toString().includes(value);
          }
        });
      });
    });
    
    setFilteredData(filtered);
  };
  
  const handleAddFilter = () => {
    setFilters(prevFilters => ({
      ...prevFilters,
      [selectedColumn]: [...(prevFilters[selectedColumn] || []), filterValue],
    }));
  };

  const handleRemoveFilter = (column, index) => {
    setFilters(prevFilters => ({
      ...prevFilters,
      [column]: prevFilters[column].filter((_, i) => i !== index),
    }));
  };

  const handleFileSelect = (event) => {
    const selectedFileName = event.target.value;
    setSelectedFile(selectedFileName);
  };

  const handleAddTile = () => {
    if (selectedFile && chartType && x !== '' && y !== null) {
        const newTile = {
            id: Date.now(),
            filename: selectedFile,
            graph_type: chartType,
            x_axis: x,
            y_axis: y,
            filters: filters
        };

        // Step 1: Update dashboards with the new tile
        const updatedDashboards = dashboards.map(dashboard => {
            if (dashboard.id === parseInt(dashboardId)) {
                return {
                    ...dashboard,
                    tiles: [...dashboard.tiles, newTile]
                };
            }
            return dashboard;
        });

        // Step 2: Generate a layout for the new tile
        const newLayout = {
            i: String(newTile.id),
            x: 0,
            y: 0,
            w: 2,
            h: 2
        };

        // Step 3: Update the layout for this dashboard
        const updatedLayouts = layouts.map(layout => {
            if (layout.id === parseInt(dashboardId)) {
                return {
                    ...layout,
                    layout: [...layout.layout || [], newLayout]
                };
            }
            return layout;
        });

        setDashboards(updatedDashboards);
        setLayouts(updatedLayouts);
        navigate(`/${dashboardId}`);
        return;
    }
};


  const handleTabChange = (event, newValue) => setActiveTab(newValue);

  return (
    <Box sx={{ 
      backgroundColor: '#f8f9fa',
      minHeight: '100vh'
    }}>
      {/* Replace AppBar with modern header */}
      <Box 
        sx={{
          backgroundColor: '#ffffff',
          borderBottom: '1px solid #e0e0e0',
          padding: '16px 24px'
        }}
      >
        <Container>
          <Box sx={{ 
            display: 'flex', 
            justifyContent: 'space-between',
            alignItems: 'center'
          }}>
            <Typography 
              variant="h5" 
              sx={{ 
                fontWeight: 600,
                color: '#1a1a1a'
              }}
            >
              Create New Tile
            </Typography>
            <Button 
              variant="outlined"
              onClick={() => navigate(`/${dashboardId}`)}
              sx={{
                textTransform: 'none',
                borderColor: '#e0e0e0',
                color: '#666666'
              }}
            >
              Cancel
            </Button>
          </Box>
        </Container>
      </Box>

      <Container sx={{ mt: 4 }}>
        {/* File Selection Section */}
        <Box 
          sx={{
            backgroundColor: '#ffffff',
            borderRadius: '12px',
            padding: '24px',
            marginBottom: '24px',
            border: '1px solid #eaeaea'
          }}
        >
          <Typography 
            variant="h6" 
            sx={{ 
              marginBottom: '16px',
              color: '#1a1a1a',
              fontWeight: 500
            }}
          >
            Select Data Source
          </Typography>

          <FormControl fullWidth>
            <InputLabel id="file-select-label">Select File</InputLabel>
            <Select
              labelId="file-select-label"
              value={selectedFile}
              label="Select File"
              onChange={handleFileSelect}
              sx={{
                backgroundColor: '#f8f9fa',
                '& .MuiOutlinedInput-notchedOutline': {
                  borderColor: '#e0e0e0'
                }
              }}
            >
              {savedFiles.map((file, index) => (
                <MenuItem key={index} value={file}>{file}</MenuItem>
              ))}
            </Select>
            
            <Box 
              mt={2}
              sx={{
                '& input': {
                  display: 'none'
                }
              }}
            >
              <Button
                component="label"
                variant="outlined"
                sx={{
                  textTransform: 'none',
                  borderColor: '#e0e0e0',
                  color: '#666666'
                }}
              >
                Upload New File
                <input
                  type="file"
                  accept=".csv"
                  hidden
                  onChange={(e) => addFiles(e.target.files[0])}
                />
              </Button>
            </Box>
          </FormControl>
        </Box>

        {fileUploaded && (
          <Box 
            sx={{
              backgroundColor: '#ffffff',
              borderRadius: '12px',
              padding: '24px',
              border: '1px solid #eaeaea'
            }}
          >
            <TabContext value={activeTab}>
              <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
                <Tabs 
                  value={activeTab} 
                  onChange={handleTabChange}
                  sx={{
                    '& .MuiTab-root': {
                      textTransform: 'none',
                      color: '#666666',
                      '&.Mui-selected': {
                        color: '#2196f3'
                      }
                    }
                  }}
                >
                  <Tab label="Data Table" value="1" />
                  <Tab label="Create Graph" value="2" />
                </Tabs>
              </Box>

              {/* Table Panel */}
              <TabPanel value="1">
              <Box>
                <FormControl fullWidth sx={{ mb: 2 }}>
                  <Select
                    value={selectedColumn}
                    onChange={(e) => {setSelectedColumn(e.target.value); setFilterValue(null);}}
                  >
                    {headers.map((header, index) => (
                      <MenuItem key={header} value={index}>
                        {header}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>

      {selectedColumn!= null && (
        <Box>
          {columnTypes[selectedColumn] === 'number' && (
            <Box display="flex" alignItems="center" mb={2}>
              <TextField
                label="Min"
                type="number"
                value={filterValue?.[0] || ''}
                onChange={(e) => setFilterValue([Number(e.target.value), filterValue?.[1] || null])}
              />
              <Box mx={1}>to</Box>
              <TextField
                label="Max"
                type="number"
                value={filterValue?.[1] || ''}
                onChange={(e) => setFilterValue([filterValue?.[0] || null, Number(e.target.value)])}
              />
            </Box>
          )}

          {columnTypes[selectedColumn] === 'date' && (
            <DateRangePicker
              startText="Start Date"
              endText="End Date"
              value={filterValue || [null, null]}
              onChange={(newValue) => setFilterValue(newValue)}
              renderInput={(startProps, endProps) => (
                <>
                  <TextField {...startProps} fullWidth />
                  <Box sx={{ mx: 1 }}>to</Box>
                  <TextField {...endProps} fullWidth />
                </>
              )}
            />
          )}

          {columnTypes[selectedColumn] === 'string' && (
            
            <TextField
              label="Contains"
              value={filterValue || ""}
              onChange={(e) => setFilterValue(e.target.value)}
              fullWidth
              sx={{ mb: 2 }}
            />
          )}
        </Box>
      )}
      <Box mt={3}>
        <Button
          variant="contained"
          onClick={handleAddFilter}
        >
          Apply Filters
        </Button>
      </Box>

      <Box mt={2}>
        {Object.keys(filters).map((column, colIndex) => (
          <Box key={colIndex} mb={2}>
            <Typography variant="subtitle1">{`Filters for ${headers[column]}:`}</Typography>
            {(filters[column].map((value, i) => (
              <Box key={i} display="flex" alignItems="center" mt={1}>
                <Typography>
                  {columnTypes[column] === 'number' && `Range: ${value[0] || "Min"} - ${value[1] || "Max"}`}
                  {columnTypes[column] === 'date' && `From: ${value[0]?.toLocaleDateString()} To: ${value[1]?.toLocaleDateString()}`}
                  {columnTypes[column] === 'string' && `Contains: ${value}`}
                </Typography>
                <IconButton onClick={() => handleRemoveFilter(column, i)}>
                  <CloseIcon />
                </IconButton>
              </Box>)
            ))}
          </Box>
        ))}
      </Box>
    </Box>
              <DataTable headers={headers} data={filteredData} />
              </TabPanel>

              {/* Graph Panel */}
              <TabPanel value="2">
                <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
                  <FormControl fullWidth>
                    <InputLabel>Chart Type</InputLabel>
                    <Select
                      value={chartType}
                      label="Chart Type"
                      onChange={handleChartTypeChange}
                      sx={{
                        backgroundColor: '#f8f9fa',
                        '& .MuiOutlinedInput-notchedOutline': {
                          borderColor: '#e0e0e0'
                        }
                      }}
                    >
                      <MenuItem value="bar">Bar Chart</MenuItem>
                      <MenuItem value="line">Line Chart</MenuItem>
                      <MenuItem value="pie">Pie Chart</MenuItem>
                    </Select>
                  </FormControl>

                  <FormControl fullWidth>
                    <InputLabel>X-Axis</InputLabel>
                    <Select
                      value={x}
                      label="X-Axis"
                      onChange={(e) => setX(e.target.value)}
                      sx={{
                        backgroundColor: '#f8f9fa',
                        '& .MuiOutlinedInput-notchedOutline': {
                          borderColor: '#e0e0e0'
                        }
                      }}
                    >
                      {headers.map((header, index) => (
                        <MenuItem key={index} value={index}>{header}</MenuItem>
                      ))}
                    </Select>
                  </FormControl>

                  <Autocomplete
                    multiple
                    options={headers.map((header, index) => ({ label: header, value: index }))}
                    onChange={handleChange}
                    getOptionLabel={(option) => option.label}
                    value={y}
                    isOptionEqualToValue={(option, value) => option.value === value.value}
                    renderInput={(params) => (
                      <TextField 
                        {...params} 
                        label="Y-Axis" 
                        placeholder="Select columns"
                        sx={{
                          backgroundColor: '#f8f9fa',
                          '& .MuiOutlinedInput-notchedOutline': {
                            borderColor: '#e0e0e0'
                          }
                        }}
                      />
                    )}
                  />

                  <Graph headers={headers} data={data} chartType={chartType} x={x} y={y} />

                  <Box sx={{ display: 'flex', justifyContent: 'flex-end', gap: 2, mt: 3 }}>
                    <Button
                      variant="contained"
                      onClick={handleAddTile}
                      sx={{
                        textTransform: 'none',
                        backgroundColor: '#2196f3',
                        '&:hover': {
                          backgroundColor: '#1976d2'
                        }
                      }}
                    >
                      Add Tile to Dashboard
                    </Button>
                  </Box>
                </Box>
              </TabPanel>
            </TabContext>
          </Box>
        )}
      </Container>
    </Box>
  );
}

export default AddTilePage;

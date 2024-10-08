import React, { useState} from 'react';
import Graph from './Graph';
import DataTable from './DataTable';
import { MultiSelect } from "react-multi-select-component";
import { useEffect } from 'react';
import { Box, Tab, Tabs, FormControl, MenuItem, InputLabel,Select, Typography} from '@mui/material';
import { TabPanel, TabContext } from '@mui/lab';
import Checkbox from '@mui/material/Checkbox';
import TextField from '@mui/material/TextField';
import Autocomplete from '@mui/material/Autocomplete';
import CheckBoxOutlineBlankIcon from '@mui/icons-material/CheckBoxOutlineBlank';
import CheckBoxIcon from '@mui/icons-material/CheckBox';

const Dashboard = ({ data }) => {
  const [chartType, setChartType] = useState('');
  const [y, sety] = useState([]);
  const [x, setx] = useState([]);
  const headers = Object.keys(data[0]);
  const [activeTab, setActiveTab] = useState('1');

  const icon = <CheckBoxOutlineBlankIcon fontSize="small" />;
  const checkedIcon = <CheckBoxIcon fontSize="small" />;
  const handleChange = (event, value) => setSelected(value);
  const handleChartTypeChange = (e) => {
    setChartType(e.target.value);
  };

  const handleTabChange = (event, newValue) => {
    setActiveTab(newValue);
  };

  const [selected, setSelected] = useState([]);
  useEffect(() => {
    sety(selected.map(z => z.value))
}, [selected])


  return (
    <div>          
    <Box mt={4}>
    <TabContext value={activeTab}>
      <Tabs value={activeTab} onChange={handleTabChange} aria-label="navigation tabs">
        <Tab label="Table" value="1" />
        <Tab label="Graphs" value="2" />
      </Tabs>

      <TabPanel value="1">
      <DataTable data={data} />
      </TabPanel>

      <TabPanel value="2">
      <FormControl sx={{ m: 1, minWidth: 300 }}>
        <InputLabel id="chart_type">Chart Type</InputLabel>
        <Select
          labelId="chart_type"
          value={chartType}
          label="chart_type"
          onChange={handleChartTypeChange}
        >
          <MenuItem value="bar">Bar Chart</MenuItem>
          <MenuItem value="line">Line Chart</MenuItem>
          <MenuItem value="pie">Pie Chart</MenuItem>
        </Select>
      </FormControl>
      <FormControl sx={{ m: 1, minWidth: 300 }}>
        <InputLabel id="x_value">X-Axis</InputLabel>
        <Select
          labelId="x_value"
          value={x}
          label="X-Axis"
          onChange={(e) => setx(e.target.value)}
        >
            {headers.map((header, index) => (
            <MenuItem value={index}>{data[0][header]}</MenuItem>
          ))}
        </Select>
      </FormControl>
      <FormControl sx={{ m: 1, minWidth: 300 }}>
      <Autocomplete
        multiple
        id="checkboxes-tags-demo"
        options={headers.map((header, index) => ({label:data[0][header], value:index}))}
        disableCloseOnSelect
        onChange={handleChange}
        getOptionLabel={(option) => option.label}
        value={selected}
        isOptionEqualToValue={(option, value) => option.value === value.value}
        renderOption={(props, option, { selected2 }) => {
            const { key, ...optionProps } = props;
            return (
            <li key={key} {...optionProps}>
                <MenuItem
                icon={icon}
                checkedIcon={checkedIcon}
                style={{ marginRight: 8 }}
                checked={selected2}
                />
                {option.label}
            </li>
            );
            
        }}
        renderInput={(params) => (
            <TextField {...params} label="Y-Axis" placeholder="Y-Axis" />
        )}
    />
    </FormControl>
      <Graph data={data} chartType={chartType} x = {x} y = {y}/>
      </TabPanel>
    
    </TabContext>
  </Box>
      
    </div>
  );
};

export default Dashboard;

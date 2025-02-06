import React from 'react';
import Select from 'react-select';

const Dropdown = ({ devices, selectedDevice, onDeviceChange }) => {
  return (
    <Select
      value={selectedDevice}
      onChange={onDeviceChange}
      options={devices}
      placeholder="Select a device"
    />
  );
};

export default Dropdown;
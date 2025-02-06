import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import useDevices from '../components/hooks/useDevices';
import useTemperatureData from '../components/hooks/useTemperatureData';
import Dropdown from '../components/Dropdown';
import TemperatureChart from '../components/TemperatureChart';

const IotVisualizationPage = () => {
  const navigate = useNavigate();
  const devices = useDevices();
  const [selectedDevice, setSelectedDevice] = useState(null);
  const { temperatureData, humidityData } = useTemperatureData(selectedDevice ? selectedDevice.value : null);

  const handleDeviceChange = (selectedOption) => {
    setSelectedDevice(selectedOption);
  };

  const handleBackToHomeClick = () => {
    navigate('/');
  };

  return (
    <div className="IotVisualizationPage" style={{ textAlign: 'center', padding: '20px', fontFamily: 'Arial, sans-serif' }}>
      <h1 style={{ color: '#2c3e50', marginBottom: '20px' }}>IoT Device Temperature and Humidity Visualization</h1>
      <div style={{ marginBottom: '20px' }}>
        <Dropdown devices={devices} selectedDevice={selectedDevice} onDeviceChange={handleDeviceChange} />
      </div>
      <button 
        onClick={handleBackToHomeClick} 
        style={{ 
          marginTop: '20px', 
          padding: '10px 20px', 
          fontSize: '16px', 
          cursor: 'pointer', 
          backgroundColor: '#3498db', 
          color: 'white', 
          border: 'none', 
          borderRadius: '5px', 
          transition: 'background-color 0.3s'
        }}
        onMouseOver={(e) => e.target.style.backgroundColor = '#2980b9'}
        onMouseOut={(e) => e.target.style.backgroundColor = '#3498db'}
      >
        Back to Home
      </button>
      {temperatureData.labels && (
        <div style={{ marginTop: '30px', padding: '20px', backgroundColor: '#ecf0f1', borderRadius: '10px', boxShadow: '0px 4px 6px rgba(0, 0, 0, 0.1)' }}>
          <TemperatureChart temperatureData={temperatureData} humidityData={humidityData} />
        </div>
      )}
    </div>
  );
};

export default IotVisualizationPage;

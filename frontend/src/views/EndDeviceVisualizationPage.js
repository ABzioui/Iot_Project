import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { fetchEndDeviceIpAddresses, fetchEndDeviceData } from '../services/apiService';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';
import Dropdown from '../components/Dropdown';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

const EndDeviceVisualizationPage = () => {
  const navigate = useNavigate();
  const [ipAddresses, setIpAddresses] = useState([]);
  const [selectedIp, setSelectedIp] = useState(null);
  const [deviceData, setDeviceData] = useState({
    cpuData: [],
    diskData: [],
    memoryData: [],
    timestamps: [],
  });

  useEffect(() => {
    const getIpAddresses = async () => {
      try {
        const data = await fetchEndDeviceIpAddresses();
        setIpAddresses(data.map(ip => ({ value: ip, label: ip })));
      } catch (error) {
        console.error('Error fetching IP addresses:', error);
      }
    };
    getIpAddresses();
  }, []);

  const handleIpChange = (selectedOption) => {
    setSelectedIp(selectedOption.value);
    fetchDeviceData(selectedOption.value);
  };

  const fetchDeviceData = async (ip) => {
    try {
      const data = await fetchEndDeviceData(ip);
      const cpuLoad = data.map(item => item.cpu_load);
      const diskUsage = data.map(item => item.disk_usage);
      const memoryUsage = data.map(item => item.memory_usage);
      const timestamps = data.map(item => item.timestamp);

      setDeviceData({
        cpuData: { labels: timestamps, datasets: [{ label: 'CPU Load (%)', data: cpuLoad, fill: false, borderColor: 'rgba(75,192,192,1)', tension: 0.1 }] },
        diskData: { labels: timestamps, datasets: [{ label: 'Disk Usage (%)', data: diskUsage, fill: false, borderColor: 'rgba(255,159,64,1)', tension: 0.1 }] },
        memoryData: { labels: timestamps, datasets: [{ label: 'Memory Usage (%)', data: memoryUsage, fill: false, borderColor: 'rgba(153,102,255,1)', tension: 0.1 }] },
        timestamps,
      });
    } catch (error) {
      console.error('Error fetching device data:', error);
    }
  };

  const handleBackToHomeClick = () => navigate('/');

  return (
    <div className="visualization-container">
      <h1>End Device Visualization</h1>
      <Dropdown devices={ipAddresses} selectedDevice={selectedIp ? { value: selectedIp, label: selectedIp } : null} onDeviceChange={handleIpChange} />
      <button className="back-button" onClick={handleBackToHomeClick}>Back to Home</button>
      <div className="chart-container">
        {deviceData.cpuData.labels && (<><h3>CPU Load Over Time</h3><Line data={deviceData.cpuData} /></>)}
        {deviceData.diskData.labels && (<><h3>Disk Usage Over Time</h3><Line data={deviceData.diskData} /></>)}
        {deviceData.memoryData.labels && (<><h3>Memory Usage Over Time</h3><Line data={deviceData.memoryData} /></>)}
      </div>
      <style>{`
        .visualization-container {
          max-width: 900px;
          margin: auto;
          text-align: center;
          padding: 20px;
          background: #f8f9fa;
          border-radius: 10px;
          box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        .back-button {
          margin-top: 20px;
          padding: 10px 20px;
          font-size: 16px;
          background: #007bff;
          color: white;
          border: none;
          border-radius: 5px;
          cursor: pointer;
          transition: background 0.3s;
        }
        .back-button:hover {
          background: #0056b3;
        }
        .chart-container {
          margin-top: 20px;
          background: white;
          padding: 20px;
          border-radius: 10px;
          box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }
      `}</style>
    </div>
  );
};

export default EndDeviceVisualizationPage;
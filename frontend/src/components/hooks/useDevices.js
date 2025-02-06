import { useState, useEffect } from 'react';
import { fetchDeviceIds } from '../../services/apiService';

const useDevices = () => {
  const [devices, setDevices] = useState([]);

  useEffect(() => {
    const getDevices = async () => {
      try {
        const deviceIds = await fetchDeviceIds();
        setDevices(deviceIds.map((id) => ({ value: id, label: id })));
      } catch (error) {
        console.error("Error fetching devices:", error);
      }
    };

    getDevices();
  }, []);

  return devices;
};

export default useDevices;
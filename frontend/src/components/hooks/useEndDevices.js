import { useState, useEffect } from 'react';
import { fetchEndDeviceIpAddresses } from '../services/apiService';

const useEndDevices = () => {
  const [endDevices, setEndDevices] = useState([]);

  useEffect(() => {
    const getEndDevices = async () => {
      try {
        const ipAddresses = await fetchEndDeviceIpAddresses();
        setEndDevices(ipAddresses.map((ip) => ({ value: ip, label: ip })));
      } catch (error) {
        console.error("Error fetching end device IPs:", error);
      }
    };

    getEndDevices();
  }, []);

  return endDevices;
};

export default useEndDevices;
import { useState, useEffect } from 'react';
import { fetchTemperatureData } from '../../services/apiService';

const useTemperatureData = (deviceId) => {
  const [temperatureData, setTemperatureData] = useState([]);
  const [humidityData, setHumidityData] = useState([]);

  useEffect(() => {
    const getTemperatureData = async () => {
      try {
        const data = await fetchTemperatureData(deviceId);
        const temperatures = data.map(item => item.temperature);
        const humidities = data.map(item => item.humidity);
        const timestamps = data.map(item => item.timestamp);

        setTemperatureData({
          labels: timestamps,
          datasets: [
            {
              label: 'Temperature (°C)',
              data: temperatures,
              fill: false,
              borderColor: 'rgba(75,192,192,1)',
              tension: 0.1,
            },
          ],
        });

        setHumidityData({
          labels: timestamps,
          datasets: [
            {
              label: 'Humidity (%)',
              data: humidities,
              fill: false,
              borderColor: 'rgba(255,159,64,1)',
              tension: 0.1,
            },
          ],
        });
      } catch (error) {
        console.error("Error fetching temperature and humidity data:", error);
      }
    };

    if (deviceId) {
      getTemperatureData();
    }
  }, [deviceId]);

  return { temperatureData, humidityData };
};

export default useTemperatureData;
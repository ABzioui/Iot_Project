import { useState, useEffect } from 'react';
import axios from 'axios';

export const useFetchTemperatureData = (deviceId) => {
  const [temperatureData, setTemperatureData] = useState([]);
  
  useEffect(() => {
    if (deviceId) {
      axios.get(`http://localhost:5010/get-temperature-data?device_id=${deviceId}`)
        .then(response => {
          const data = response.data;
          const temperatures = data.map(item => item.temperature);
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
        })
        .catch(error => console.error(error));
    }
  }, [deviceId]);

  return { temperatureData };
};
import React from 'react';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

const TemperatureChart = ({ temperatureData, humidityData }) => {
  return (
    <div>
      {temperatureData.labels && (
        <div>
          <h3>Temperature Over Time</h3>
          <Line
            data={temperatureData}
            options={{
              responsive: true,
              plugins: {
                legend: {
                  position: 'top',
                },
                title: {
                  display: true,
                  text: 'Temperature (°C)',
                },
              },
              scales: {
                x: {
                  type: 'category',
                  title: {
                    display: true,
                    text: 'Timestamp',
                  },
                },
                y: {
                  type: 'linear',
                  title: {
                    display: true,
                    text: 'Temperature (°C)',
                  },
                },
              },
            }}
          />
        </div>
      )}

      {humidityData.labels && (
        <div>
          <h3>Humidity Over Time</h3>
          <Line
            data={humidityData}
            options={{
              responsive: true,
              plugins: {
                legend: {
                  position: 'top',
                },
                title: {
                  display: true,
                  text: 'Humidity (%)',
                },
              },
              scales: {
                x: {
                  type: 'category',
                  title: {
                    display: true,
                    text: 'Timestamp',
                  },
                },
                y: {
                  type: 'linear',
                  title: {
                    display: true,
                    text: 'Humidity (%)',
                  },
                },
              },
            }}
          />
        </div>
      )}
    </div>
  );
};

export default TemperatureChart;
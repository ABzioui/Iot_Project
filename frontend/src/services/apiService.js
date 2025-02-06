import axios from 'axios';

const API_URL = 'http://localhost:5010';

export const fetchDeviceIds = async () => {
  try {
    const response = await axios.get(`${API_URL}/get-device-ids`);
    return response.data;
  } catch (error) {
    console.error("Error fetching device IDs:", error);
    throw error;
  }
};

export const fetchTemperatureData = async (deviceId) => {
  try {
    const response = await axios.get(`${API_URL}/get-temperature-data?device_id=${deviceId}`);
    return response.data;
  } catch (error) {
    console.error("Error fetching temperature data:", error);
    throw error;
  }
};

export const fetchEndDeviceIpAddresses = async () => {
  try {
    const response = await axios.get(`${API_URL}/get-enddevice-ip`);
    return response.data;
  } catch (error) {
    console.error('Error fetching end device IP addresses:', error);
    throw error;
  }
};

export const fetchEndDeviceData = async (ipAddress) => {
  try {
    const response = await axios.get(`${API_URL}/get-enddevice-data?ip_address=${ipAddress}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching end device data for IP:', ipAddress, error);
    throw error;
  }
};
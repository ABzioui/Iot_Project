import axios from 'axios';

const API_BASE_URL = 'http://localhost:5001';

export const deviceApi = {
  listDevices: () => axios.get(`${API_BASE_URL}/devices`, {
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('token')}`
    }
  }),
  getDevice: (id) => axios.get(`${API_BASE_URL}/devices/${id}`, {
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('token')}`
    }
  }),
  createDevice: (data) => axios.post(`${API_BASE_URL}/devices`, data, {
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('token')}`
    }
  }),
  updateDevice: (id, data) => axios.put(`${API_BASE_URL}/devices/${id}`, data, {
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('token')}`
    }
  }),
  deleteDevice: (id) => axios.delete(`${API_BASE_URL}/devices/${id}`, {
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('token')}`
    }
  })
};
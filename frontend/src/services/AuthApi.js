import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000';

export const authApi = {
  signIn: (credentials) => axios.post(`${API_BASE_URL}/signin`, credentials),
  register: (userData) => axios.post(`${API_BASE_URL}/register`, userData),
  getProfile: () => axios.get(`${API_BASE_URL}/profile`, {
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('token')}`
    }
  }),
  logout: () => axios.post(`${API_BASE_URL}/logout`, {}, {
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('token')}`
    }
  })
};
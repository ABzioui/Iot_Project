import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { CssBaseline, Container } from '@mui/material';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import PrivateRoute from './components/auth/PrivateRoute';
import SignIn from './components/auth/SignIn';
import Register from './components/auth/Register';
import Profile from './components/auth/Profile';
import DeviceList from './components/devices/DeviceList';
import DeviceForm from './components/devices/DeviceForm';
import DeviceDetail from './components/devices/DeviceDetail';
import HomePage from './views/HomePage';
import MonitoringPage from './views/MonitoringPage';
import IotVisualizationPage from './views/IotVisualizationPage';
import EndDeviceVisualizationPage from './views/EndDeviceVisualizationPage';

const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
});

const App = () => {
  return (
    <ThemeProvider theme={theme}>
      <BrowserRouter>
        <CssBaseline />
        <Container maxWidth="lg">
          <Routes>
            <Route path="/signin" element={<SignIn />} />
            <Route path="/register" element={<Register />} />
            <Route path="/profile" element={<PrivateRoute element={<Profile />} />} />
            <Route path="/devices" element={<PrivateRoute element={<DeviceList />} />} />
            <Route path="/devices/new" element={<PrivateRoute element={<DeviceForm />} />} />
            <Route path="/devices/:id" element={<PrivateRoute element={<DeviceDetail />} />} />
            <Route path="/devices/:id/edit" element={<PrivateRoute element={<DeviceForm />} />} />
            <Route path="/" element={<HomePage />} />
            <Route path="/monitoring" element={<MonitoringPage />} />
            <Route path="/iot-visualization" element={<IotVisualizationPage />} />
            <Route path="/end-device-visualization" element={<EndDeviceVisualizationPage />} />
          </Routes>
        </Container>
      </BrowserRouter>
    </ThemeProvider>
  );
};

export default App;
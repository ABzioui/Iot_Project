import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import DeviceListPage from './pages/DeviceListPage';
import DeviceDetailPage from './pages/DeviceDetailPage';
import DeviceEditPage from './pages/DeviceEditePage';
import DeviceAddPage from './pages/DeviceAddPage';

const AppRoutes = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<DeviceListPage />} />
        <Route path="/device/:id" element={<DeviceDetailPage />} />
        <Route path="/device/edit/:id" element={<DeviceEditPage />} />
        <Route path="/device/add" element={<DeviceAddPage />} />
      </Routes>
    </Router>
  );
};

export default AppRoutes;

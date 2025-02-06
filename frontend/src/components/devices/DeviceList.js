import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Button,
  Typography,
  Box,
  IconButton,
  Chip,
  Tooltip,
  LinearProgress,
  Container,
  Alert,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
} from '@mui/material';
import {
  Add as AddIcon,
  Visibility as ViewIcon,
  Delete as DeleteIcon,
  ArrowBack as ArrowBackIcon,
  Refresh as RefreshIcon,
} from '@mui/icons-material';
import { deviceApi } from '../../services/DeviceApi';

export default function DeviceList() {
  const [devices, setDevices] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [deleteDialog, setDeleteDialog] = useState({ open: false, deviceId: null });
  const navigate = useNavigate();

  useEffect(() => {
    loadDevices();
  }, []);

  const loadDevices = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await deviceApi.listDevices();
      setDevices(response.data);
    } catch (error) {
      setError('Failed to load devices. Please try again later.');
      console.error('Error loading devices:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (deviceId) => {
    try {
      await deviceApi.deleteDevice(deviceId);
      setDeleteDialog({ open: false, deviceId: null });
      loadDevices();
    } catch (error) {
      setError('Failed to delete device. Please try again.');
      console.error('Error deleting device:', error);
    }
  };

  const getStatusChipColor = (status) => {
    const statusMap = {
      'active': 'success',
      'inactive': 'error',
      'maintenance': 'warning',
      'offline': 'default'
    };
    return statusMap[status.toLowerCase()] || 'default';
  };

  return (
    <Container maxWidth="lg">
      <Box sx={{ py: 4 }}>
        {/* Header Section */}
        <Box sx={{ mb: 4 }}>
          <Button
            startIcon={<ArrowBackIcon />}
            onClick={() => navigate('/')}
            sx={{ mb: 2 }}
          >
            Back to Dashboard
          </Button>
          
          <Paper
            elevation={3}
            sx={{
              p: 3,
              background: 'linear-gradient(45deg, #3f51b5 30%, #2196F3 90%)',
              color: 'white',
              mb: 4,
            }}
          >
            <Box display="flex" justifyContent="space-between" alignItems="center">
              <Typography variant="h4" component="h1" sx={{ fontWeight: 'bold' }}>
                Device Management
              </Typography>
              <Box>
                <Tooltip title="Refresh list">
                  <IconButton 
                    onClick={loadDevices} 
                    sx={{ color: 'white', mr: 1 }}
                  >
                    <RefreshIcon />
                  </IconButton>
                </Tooltip>
                <Button
                  variant="contained"
                  startIcon={<AddIcon />}
                  onClick={() => navigate('/devices/new')}
                  sx={{
                    backgroundColor: 'white',
                    color: '#3f51b5',
                    '&:hover': {
                      backgroundColor: 'rgba(255, 255, 255, 0.9)',
                    },
                  }}
                >
                  Add New Device
                </Button>
              </Box>
            </Box>
          </Paper>
        </Box>

        {/* Error Alert */}
        {error && (
          <Alert severity="error" sx={{ mb: 3 }}>
            {error}
          </Alert>
        )}

        {/* Loading State */}
        {loading && <LinearProgress sx={{ mb: 3 }} />}

        {/* Table Section */}
        <TableContainer 
          component={Paper} 
          sx={{ 
            boxShadow: 3,
            '& .MuiTableCell-head': {
              backgroundColor: '#f5f5f5',
              fontWeight: 'bold',
            },
          }}
        >
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Device ID</TableCell>
                <TableCell>Type</TableCell>
                <TableCell>Status</TableCell>
                <TableCell>Created At</TableCell>
                <TableCell align="center">Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {devices.map((device) => (
                <TableRow 
                  key={device.device_id}
                  sx={{ '&:hover': { backgroundColor: '#f5f5f5' } }}
                >
                  <TableCell>{device.device_id}</TableCell>
                  <TableCell>
                    <Typography variant="body2" color="textSecondary">
                      {device.type}
                    </Typography>
                  </TableCell>
                  <TableCell>
                    <Chip
                      label={device.status}
                      color={getStatusChipColor(device.status)}
                      size="small"
                    />
                  </TableCell>
                  <TableCell>
                    <Typography variant="body2" color="textSecondary">
                      {new Date(device.created_at).toLocaleDateString(undefined, {
                        year: 'numeric',
                        month: 'long',
                        day: 'numeric'
                      })}
                    </Typography>
                  </TableCell>
                  <TableCell align="center">
                    <Tooltip title="View details">
                      <IconButton
                        color="primary"
                        onClick={() => navigate(`/devices/${device.device_id}`)}
                        size="small"
                      >
                        <ViewIcon />
                      </IconButton>
                    </Tooltip>
                    <Tooltip title="Delete device">
                      <IconButton
                        color="error"
                        onClick={() => setDeleteDialog({ 
                          open: true, 
                          deviceId: device.device_id 
                        })}
                        size="small"
                      >
                        <DeleteIcon />
                      </IconButton>
                    </Tooltip>
                  </TableCell>
                </TableRow>
              ))}
              {devices.length === 0 && !loading && (
                <TableRow>
                  <TableCell colSpan={5} align="center" sx={{ py: 3 }}>
                    <Typography variant="body1" color="textSecondary">
                      No devices found. Click "Add New Device" to get started.
                    </Typography>
                  </TableCell>
                </TableRow>
              )}
            </TableBody>
          </Table>
        </TableContainer>

        {/* Delete Confirmation Dialog */}
        <Dialog
          open={deleteDialog.open}
          onClose={() => setDeleteDialog({ open: false, deviceId: null })}
        >
          <DialogTitle>Confirm Device Deletion</DialogTitle>
          <DialogContent>
            Are you sure you want to delete this device? This action cannot be undone.
          </DialogContent>
          <DialogActions>
            <Button 
              onClick={() => setDeleteDialog({ open: false, deviceId: null })}
            >
              Cancel
            </Button>
            <Button 
              color="error" 
              variant="contained"
              onClick={() => handleDelete(deleteDialog.deviceId)}
            >
              Delete
            </Button>
          </DialogActions>
        </Dialog>
      </Box>
    </Container>
  );
}
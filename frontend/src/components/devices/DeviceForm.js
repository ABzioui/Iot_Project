import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import {
  TextField,
  Button,
  Box,
  Typography,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Grid,
  Paper,
  Container,
  Alert,
  CircularProgress,
  IconButton,
  Tooltip,
  Divider,
} from '@mui/material';
import {
  ArrowBack as ArrowBackIcon,
  Save as SaveIcon,
  Cancel as CancelIcon,
  LocationOn as LocationIcon,
} from '@mui/icons-material';
import { deviceApi } from '../../services/DeviceApi';

export default function DeviceForm() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [formData, setFormData] = useState({
    device_id: '',
    type: '',
    status: 'active',
    location_lat: '',
    location_lon: '',
    monitored_params: []
  });

  useEffect(() => {
    if (id) {
      loadDevice();
    }
  }, [id]);

  const loadDevice = async () => {
    setLoading(true);
    try {
      const response = await deviceApi.getDevice(id);
      setFormData(response.data);
    } catch (error) {
      setError('Failed to load device details. Please try again.');
      console.error('Error loading device:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      if (id) {
        await deviceApi.updateDevice(id, formData);
      } else {
        await deviceApi.createDevice(formData);
      }
      navigate('/devices');
    } catch (error) {
      setError('Failed to save device. Please check your inputs and try again.');
      console.error('Error saving device:', error);
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  if (loading && id) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Container maxWidth="lg">
      <Box sx={{ py: 4 }}>
        {/* Header Section */}
        <Button
          startIcon={<ArrowBackIcon />}
          onClick={() => navigate('/devices')}
          sx={{ mb: 3 }}
        >
          Back to Devices
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
          <Typography variant="h4" component="h1" sx={{ fontWeight: 'bold' }}>
            {id ? 'Edit Device' : 'Add New Device'}
          </Typography>
          <Typography variant="subtitle1" sx={{ mt: 1, opacity: 0.9 }}>
            {id ? 'Modify the device details below' : 'Fill in the device details below'}
          </Typography>
        </Paper>

        {error && (
          <Alert severity="error" sx={{ mb: 3 }}>
            {error}
          </Alert>
        )}

        <Paper elevation={2} sx={{ p: 4 }}>
          <form onSubmit={handleSubmit}>
            <Grid container spacing={3}>
              <Grid item xs={12} md={6}>
                <TextField
                  fullWidth
                  label="Device ID"
                  name="device_id"
                  value={formData.device_id}
                  onChange={handleChange}
                  disabled={!!id}
                  required
                  variant="outlined"
                  helperText={!!id ? "Device ID cannot be modified" : "Enter a unique device identifier"}
                />
              </Grid>
              <Grid item xs={12} md={6}>
                <FormControl fullWidth required>
                  <InputLabel>Type</InputLabel>
                  <Select
                    name="type"
                    value={formData.type}
                    onChange={handleChange}
                    disabled={!!id}
                    variant="outlined"
                  >
                    <MenuItem value="iot">IoT Device</MenuItem>
                    <MenuItem value="end_device">End Device</MenuItem>
                    <MenuItem value="api">API Device</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={12} md={6}>
                <FormControl fullWidth>
                  <InputLabel>Status</InputLabel>
                  <Select
                    name="status"
                    value={formData.status}
                    onChange={handleChange}
                    variant="outlined"
                  >
                    <MenuItem value="active">Active</MenuItem>
                    <MenuItem value="inactive">Inactive</MenuItem>
                  </Select>
                </FormControl>
              </Grid>

              {formData.type === 'api' && (
                <>
                  <Grid item xs={12}>
                    <Divider>
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        <LocationIcon color="primary" />
                        <Typography color="primary">Location Details</Typography>
                      </Box>
                    </Divider>
                  </Grid>
                  <Grid item xs={12} md={6}>
                    <TextField
                      fullWidth
                      label="Latitude"
                      name="location_lat"
                      type="number"
                      value={formData.location_lat}
                      onChange={handleChange}
                      variant="outlined"
                      InputProps={{
                        inputProps: { 
                          min: -90, 
                          max: 90,
                          step: "any"
                        }
                      }}
                      helperText="Enter latitude between -90 and 90"
                    />
                  </Grid>
                  <Grid item xs={12} md={6}>
                    <TextField
                      fullWidth
                      label="Longitude"
                      name="location_lon"
                      type="number"
                      value={formData.location_lon}
                      onChange={handleChange}
                      variant="outlined"
                      InputProps={{
                        inputProps: { 
                          min: -180, 
                          max: 180,
                          step: "any"
                        }
                      }}
                      helperText="Enter longitude between -180 and 180"
                    />
                  </Grid>
                </>
              )}
            </Grid>

            <Box sx={{ mt: 4, display: 'flex', gap: 2 }}>
              <Button
                type="submit"
                variant="contained"
                color="primary"
                disabled={loading}
                startIcon={loading ? <CircularProgress size={20} /> : <SaveIcon />}
                sx={{ minWidth: 120 }}
              >
                {loading ? 'Saving...' : id ? 'Update Device' : 'Create Device'}
              </Button>
              <Button
                variant="outlined"
                onClick={() => navigate('/devices')}
                startIcon={<CancelIcon />}
                sx={{ minWidth: 120 }}
              >
                Cancel
              </Button>
            </Box>
          </form>
        </Paper>
      </Box>
    </Container>
  );
}
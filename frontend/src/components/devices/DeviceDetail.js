import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Card, CardContent, Typography, Button, Box,
  Grid, Divider
} from '@mui/material';
import { deviceApi } from '../../services/DeviceApi';

export default function DeviceDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [device, setDevice] = useState(null);

  useEffect(() => {
    loadDevice();
  }, [id]);

  const loadDevice = async () => {
    try {
      const response = await deviceApi.getDevice(id);
      setDevice(response.data);
    } catch (error) {
      console.error('Error loading device:', error);
    }
  };

  if (!device) return <Typography>Loading...</Typography>;

  return (
    <Box p={3}>
      <Card>
        <CardContent>
          <Box display="flex" justifyContent="space-between" alignItems="center">
            <Typography variant="h4">Device Details</Typography>
            <Box>
              <Button 
                variant="contained" 
                color="primary"
                onClick={() => navigate(`/devices/${id}/edit`)}
              >
                Edit
              </Button>
              <Button 
                variant="outlined"
                onClick={() => navigate('/devices')}
                sx={{ ml: 2 }}
              >
                Back
              </Button>
            </Box>
          </Box>
          <Divider sx={{ my: 2 }} />
          <Grid container spacing={2}>
            <Grid item xs={12} md={6}>
              <Typography variant="subtitle1">Device ID:</Typography>
              <Typography variant="body1">{device.device_id}</Typography>
            </Grid>
            <Grid item xs={12} md={6}>
              <Typography variant="subtitle1">Type:</Typography>
              <Typography variant="body1">{device.type}</Typography>
            </Grid>
            <Grid item xs={12} md={6}>
              <Typography variant="subtitle1">Status:</Typography>
              <Typography variant="body1">{device.status}</Typography>
            </Grid>
            {device.type === 'api' && (
              <>
                <Grid item xs={12} md={6}>
                  <Typography variant="subtitle1">Location:</Typography>
                  <Typography variant="body1">
                    {device.location_lat}, {device.location_lon}
                  </Typography>
                </Grid>
              </>
            )}
            {device.latest_data && (
              <Grid item xs={12}>
                <Typography variant="h6" sx={{ mt: 2 }}>Latest Data</Typography>
                <pre>{JSON.stringify(device.latest_data, null, 2)}</pre>
              </Grid>
            )}
          </Grid>
        </CardContent>
      </Card>
    </Box>
  );
}
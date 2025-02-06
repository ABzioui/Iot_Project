import React from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Container,
  Typography,
  Paper,
  Grid,
  Card,
  CardContent,
  CardActions,
  Button,
  IconButton,
  useTheme,
} from '@mui/material';
import {
  ShowChart as ChartIcon,
  Router as RouterIcon,
  Cloud as CloudIcon,
  ArrowBack as ArrowBackIcon,
} from '@mui/icons-material';

const MonitoringPage = () => {
  const navigate = useNavigate();
  const theme = useTheme();

  const monitoringFeatures = [
    {
      title: 'IoT Visualization',
      icon: <ChartIcon sx={{ fontSize: 40 }} />,
      description: 'View real-time data visualization of your IoT network performance and metrics.',
      path: '/iot-visualization',
      color: '#2196f3', // blue
    },
    {
      title: 'End Device Visualization',
      icon: <RouterIcon sx={{ fontSize: 40 }} />,
      description: 'Monitor and analyze individual end device status and performance metrics.',
      path: '/end-device-visualization',
      color: '#4caf50', // green
    },
    {
      title: 'Meteo Predictions',
      icon: <CloudIcon sx={{ fontSize: 40 }} />,
      description: 'Access weather predictions and environmental data analysis.',
      path: '/meteo-predictions',
      color: '#ff9800', // orange
    },
  ];

  return (
    <Box
      sx={{
        minHeight: '100vh',
        backgroundColor: 'background.default',
        pt: 4,
        pb: 6,
      }}
    >
      <Container maxWidth="lg">
        <Button
          startIcon={<ArrowBackIcon />}
          onClick={() => navigate('/')}
          sx={{ mb: 3 }}
        >
          Back to Dashboard
        </Button>

        <Paper
          elevation={3}
          sx={{
            borderRadius: 2,
            p: 4,
            mb: 4,
            background: 'linear-gradient(45deg, #3f51b5 30%, #2196F3 90%)',
            color: 'white',
          }}
        >
          <Typography
            component="h1"
            variant="h3"
            align="center"
            gutterBottom
            sx={{
              fontWeight: 'bold',
              textShadow: '2px 2px 4px rgba(0,0,0,0.2)',
            }}
          >
            Monitoring Dashboard
          </Typography>
          <Typography variant="h6" align="center">
            Monitor and analyze your IoT network performance
          </Typography>
        </Paper>

        <Grid container spacing={4}>
          {monitoringFeatures.map((feature) => (
            <Grid item xs={12} md={4} key={feature.title}>
              <Card
                sx={{
                  height: '100%',
                  display: 'flex',
                  flexDirection: 'column',
                  transition: 'transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out',
                  '&:hover': {
                    transform: 'translateY(-5px)',
                    boxShadow: 6,
                  },
                }}
              >
                <CardContent sx={{ flexGrow: 1 }}>
                  <Box
                    sx={{
                      display: 'flex',
                      justifyContent: 'center',
                      mb: 2,
                    }}
                  >
                    <IconButton
                      sx={{
                        backgroundColor: `${feature.color}15`,
                        color: feature.color,
                        '&:hover': {
                          backgroundColor: `${feature.color}25`,
                        },
                      }}
                    >
                      {feature.icon}
                    </IconButton>
                  </Box>
                  <Typography 
                    gutterBottom 
                    variant="h5" 
                    component="h2" 
                    align="center"
                    sx={{ color: feature.color, fontWeight: 'medium' }}
                  >
                    {feature.title}
                  </Typography>
                  <Typography variant="body1" align="center" color="text.secondary">
                    {feature.description}
                  </Typography>
                </CardContent>
                <CardActions sx={{ justifyContent: 'center', pb: 3 }}>
                  <Button
                    variant="contained"
                    size="large"
                    onClick={() => navigate(feature.path)}
                    sx={{
                      backgroundColor: feature.color,
                      '&:hover': {
                        backgroundColor: feature.color,
                        opacity: 0.9,
                      },
                    }}
                  >
                    View Details
                  </Button>
                </CardActions>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Container>
    </Box>
  );
};

export default MonitoringPage;
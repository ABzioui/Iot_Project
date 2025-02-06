import React from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Container,
  Typography,
  Button,
  Paper,
  Grid,
  Card,
  CardContent,
  CardActions,
  IconButton,
  useTheme,
} from '@mui/material';
import {
  Speed as SpeedIcon,
  DevicesOther as DevicesIcon,
  Settings as SettingsIcon,
} from '@mui/icons-material';

const HomePage = () => {
  const navigate = useNavigate();
  const theme = useTheme();

  const features = [
    {
      title: 'Real-time Monitoring',
      icon: <SpeedIcon sx={{ fontSize: 40 }} />,
      description: 'Monitor your IoT devices in real-time with advanced analytics and alerts.',
      path: '/monitoring',
      color: theme.palette.primary.main,
    },
    {
      title: 'Device Management',
      icon: <DevicesIcon sx={{ fontSize: 40 }} />,
      description: 'Manage and configure all your IoT devices from a centralized dashboard.',
      path: '/devices',
      color: theme.palette.secondary.main,
    },
  ];

  return (
    <Box
      sx={{
        minHeight: '100vh',
        backgroundColor: 'background.default',
        pt: 8,
        pb: 6,
      }}
    >
      <Container maxWidth="lg">
        <Paper
          elevation={3}
          sx={{
            borderRadius: 2,
            p: 4,
            mb: 4,
            background: 'linear-gradient(45deg, #2196F3 30%, #21CBF3 90%)',
            color: 'white',
          }}
        >
          <Typography
            component="h1"
            variant="h2"
            align="center"
            gutterBottom
            sx={{
              fontWeight: 'bold',
              textShadow: '2px 2px 4px rgba(0,0,0,0.2)',
            }}
          >
            Welcome to IoT Dashboard
          </Typography>
          <Typography variant="h5" align="center" paragraph>
            Monitor, manage, and analyze your IoT devices all in one place
          </Typography>
        </Paper>

        <Grid container spacing={4} justifyContent="center">
          {features.map((feature) => (
            <Grid item xs={12} sm={6} md={6} key={feature.title}>
              <Card
                sx={{
                  height: '100%',
                  display: 'flex',
                  flexDirection: 'column',
                  transition: 'transform 0.2s ease-in-out',
                  '&:hover': {
                    transform: 'translateY(-5px)',
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
                  <Typography gutterBottom variant="h5" component="h2" align="center">
                    {feature.title}
                  </Typography>
                  <Typography align="center" color="text.secondary">
                    {feature.description}
                  </Typography>
                </CardContent>
                <CardActions sx={{ justifyContent: 'center', pb: 2 }}>
                  <Button
                    variant="contained"
                    sx={{
                      backgroundColor: feature.color,
                      '&:hover': {
                        backgroundColor: feature.color,
                        opacity: 0.9,
                      },
                    }}
                    onClick={() => navigate(feature.path)}
                  >
                    Go to {feature.title}
                  </Button>
                </CardActions>
              </Card>
            </Grid>
          ))}
        </Grid>

        <Box sx={{ mt: 4, textAlign: 'center' }}>
          <Button
            variant="outlined"
            startIcon={<SettingsIcon />}
            sx={{ mt: 2 }}
            onClick={() => navigate('/settings')}
          >
            System Settings
          </Button>
        </Box>
      </Container>
    </Box>
  );
};

export default HomePage;
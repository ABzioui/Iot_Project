import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Box, Button, Typography } from "@mui/material";
import { authApi } from '../../services/AuthApi';

const Profile = () => {
  const [userData, setUserData] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchProfile = async () => {
      const token = localStorage.getItem('token');
      if (!token) {
        navigate("/signin");
        return;
      }

      try {
        const response = await authApi.getProfile();
        setUserData(response);
      } catch (error) {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        navigate("/signin");
      }
    };

    fetchProfile();
  }, [navigate]);

  const handleSignOut = async () => {
    try {
      await authApi.logout();
    } catch (error) {
      console.error('Logout failed', error);
    } finally {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      navigate("/signin");
    }
  };

  return (
    <Box sx={{/* existing styles */}}>
      {userData ? (
        <>
          <Typography variant="h5" mb={2}>
            Welcome, {userData.username}!
          </Typography>
          <Button
            variant="contained"
            color="secondary"
            onClick={handleSignOut}
            fullWidth
            sx={{ mt: 2 }}
          >
            Sign Out
          </Button>
        </>
      ) : (
        <Typography variant="body1">Loading...</Typography>
      )}
    </Box>
  );
};

export default Profile;
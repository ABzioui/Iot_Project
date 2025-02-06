import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { 
  Box, 
  TextField, 
  Button, 
  Typography, 
  Alert, 
  Link, 
  InputAdornment, 
  IconButton 
} from "@mui/material";
import { Visibility, VisibilityOff } from "@mui/icons-material";
import { authApi } from '../../services/AuthApi';

const SignIn = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      navigate("/devices");
    }
  }, [navigate]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    if (!username || !password) {
      setError("Please enter both username and password");
      setLoading(false);
      return;
    }

    try {
      const response = await authApi.signIn({ username, password });
      localStorage.setItem('token', response.token);
      localStorage.setItem('user', JSON.stringify({ username: response.user }));
      navigate("/");
    } catch (err) {
      setError("Sign-In failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleClickShowPassword = () => {
    setShowPassword(!showPassword);
  };

  const handleMouseDownPassword = (event) => {
    event.preventDefault();
  };

  return (
    <Box
      sx={{
        maxWidth: 400,
        mx: "auto",
        mt: 8,
        p: 3,
        boxShadow: 3,
        borderRadius: 2,
        textAlign: "center",
      }}
    >
      <Typography variant="h4" mb={3} fontWeight="bold">
        Sign In
      </Typography>

      {error && (
        <Alert 
          severity="error" 
          sx={{ mb: 2, width: '100%' }}
        >
          {error}
        </Alert>
      )}

      <Box component="form" onSubmit={handleSubmit} noValidate>
        <TextField
          label="Username"
          variant="outlined"
          fullWidth
          margin="normal"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
          error={!!error}
        />

        <TextField
          label="Password"
          type={showPassword ? "text" : "password"}
          variant="outlined"
          fullWidth
          margin="normal"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          error={!!error}
          InputProps={{
            endAdornment: (
              <InputAdornment position="end">
                <IconButton
                  aria-label="toggle password visibility"
                  onClick={handleClickShowPassword}
                  onMouseDown={handleMouseDownPassword}
                  edge="end"
                >
                  {showPassword ? <VisibilityOff /> : <Visibility />}
                </IconButton>
              </InputAdornment>
            )
          }}
        />

        <Button
          type="submit"
          variant="contained"
          color="primary"
          fullWidth
          sx={{ mt: 2, py: 1.5 }}
          disabled={loading}
        >
          {loading ? "Signing In..." : "Sign In"}
        </Button>
      </Box>

      <Typography variant="body2" mt={2}>
        Don't have an account?{" "}
        <Link 
          href="/register" 
          underline="hover"
          color="primary"
        >
          Register here
        </Link>
      </Typography>
    </Box>
  );
};

export default SignIn;
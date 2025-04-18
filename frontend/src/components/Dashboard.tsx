import { Box, Button, Container, Paper, Typography } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const Dashboard = () => {
  const navigate = useNavigate();
  const { user, logout } = useAuth();

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  return (
    <Container component="main" maxWidth="md">
      <Box
        sx={{
          marginTop: 8,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
        }}
      >
        <Paper
          elevation={3}
          sx={{
            padding: 4,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            width: '100%',
          }}
        >
          <Typography component="h1" variant="h4" sx={{ mb: 3 }}>
            Bem-vindo!
          </Typography>
          {user && (
            <>
              <Typography variant="h6" sx={{ mb: 2 }}>
                {user.name}
              </Typography>
              <Typography variant="body1" sx={{ mb: 3 }}>
                {user.email}
              </Typography>
            </>
          )}
          <Button
            variant="contained"
            color="error"
            onClick={handleLogout}
            sx={{ mt: 2 }}
          >
            Sair
          </Button>
        </Paper>
      </Box>
    </Container>
  );
};

export default Dashboard; 
import { Box, Button, Container, Paper, Typography } from '@mui/material';
import { useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import GoogleIcon from '@mui/icons-material/Google';

const Login = () => {
  const { user } = useAuth();

  const handleGoogleLogin = () => {
    window.location.href = 'http://localhost:8000/login/google';
  };

  // Limpar qualquer sessão existente ao montar o componente
  useEffect(() => {
    document.cookie = 'session=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
  }, []);

  return (
    <Box
      sx={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        padding: 3,
      }}
    >
      <Container maxWidth="sm">
        <Paper
          elevation={6}
          sx={{
            padding: { xs: 3, sm: 6 },
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            borderRadius: 2,
            background: 'rgba(255, 255, 255, 0.95)',
            backdropFilter: 'blur(10px)',
            boxShadow: '0 8px 32px 0 rgba(31, 38, 135, 0.37)',
          }}
        >
          <Typography
            component="h1"
            variant="h4"
            sx={{
              mb: 4,
              fontWeight: 600,
              color: '#1a237e',
              textAlign: 'center',
            }}
          >
            Bem-vindo ao Fruit Checker
          </Typography>
          <Typography
            variant="body1"
            sx={{
              mb: 4,
              color: '#666',
              textAlign: 'center',
              maxWidth: '80%',
            }}
          >
            Faça login para começar a identificar frutas e explorar suas características
          </Typography>
          <Button
            fullWidth
            variant="contained"
            onClick={handleGoogleLogin}
            startIcon={<GoogleIcon />}
            sx={{
              py: 1.5,
              backgroundColor: '#4285f4',
              color: 'white',
              fontSize: '1.1rem',
              textTransform: 'none',
              borderRadius: 2,
              boxShadow: '0 2px 4px rgba(0,0,0,0.2)',
              '&:hover': {
                backgroundColor: '#357abd',
                boxShadow: '0 4px 8px rgba(0,0,0,0.2)',
              },
              transition: 'all 0.3s ease',
            }}
          >
            Entrar com Google
          </Button>
        </Paper>
      </Container>
    </Box>
  );
};

export default Login; 
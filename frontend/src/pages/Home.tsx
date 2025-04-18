import { Box, Typography, Paper } from '@mui/material';
import Sidebar from '../components/Sidebar';
import { useAuth } from '../contexts/AuthContext';

const Home = () => {
  const { user } = useAuth();

  return (
    <Box sx={{ display: 'flex', minHeight: '100vh' }}>
      <Sidebar />
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: 3,
          background: 'linear-gradient(135deg, #f5f7ff 0%, #e8eaff 100%)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
        }}
      >
        <Paper
          elevation={3}
          sx={{
            p: 6,
            maxWidth: 600,
            width: '100%',
            textAlign: 'center',
            background: 'rgba(255, 255, 255, 0.95)',
          }}
        >
          <Typography
            variant="h3"
            sx={{
              mb: 2,
              background: 'linear-gradient(45deg, #667eea 30%, #764ba2 90%)',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
              fontWeight: 'bold',
            }}
          >
            Bem-vindo!
          </Typography>
          <Typography
            variant="h4"
            sx={{
              color: '#1a237e',
              mb: 3,
              fontWeight: 500,
            }}
          >
            {user?.name}
          </Typography>
          <Typography
            variant="body1"
            sx={{
              color: '#666',
              fontSize: '1.1rem',
              maxWidth: '80%',
              margin: '0 auto',
            }}
          >
            Explore o Fruit Checker para identificar frutas e descobrir suas características.
            Use a barra lateral para navegar entre as funcionalidades disponíveis.
          </Typography>
        </Paper>
      </Box>
    </Box>
  );
};

export default Home; 
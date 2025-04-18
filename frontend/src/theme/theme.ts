import { createTheme } from '@mui/material/styles';

export const theme = createTheme({
  palette: {
    primary: {
      main: '#667eea',
      dark: '#4C63CB',
      light: '#869EFF',
    },
    secondary: {
      main: '#764ba2',
      dark: '#5B3A7E',
      light: '#9169C6',
    },
    background: {
      default: '#f5f7ff',
      paper: 'rgba(255, 255, 255, 0.95)',
    },
    text: {
      primary: '#1a237e',
      secondary: '#666666',
    },
  },
  typography: {
    fontFamily: '"Inter", "Roboto", "Helvetica", "Arial", sans-serif',
    h4: {
      fontWeight: 600,
    },
    button: {
      textTransform: 'none',
      fontWeight: 500,
    },
  },
  components: {
    MuiPaper: {
      styleOverrides: {
        root: {
          backdropFilter: 'blur(10px)',
          boxShadow: '0 8px 32px 0 rgba(31, 38, 135, 0.37)',
        },
      },
    },
  },
}); 
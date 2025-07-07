import { useState } from 'react';
import {
  Box,
  Button,
  Container,
  Paper,
  Typography,
  CircularProgress,
  Snackbar,
  Alert
} from '@mui/material';
import Sidebar from '../components/Sidebar';
import axios from 'axios';

const VerificarFruta = () => {
  const [file, setFile] = useState<File | null>(null);
  const [result, setResult] = useState<{ classe: string; probabilidade: number } | null>(null);
  const [loading, setLoading] = useState(false);
  const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'success' as 'success' | 'error' });

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setResult(null);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) {
      setSnackbar({ open: true, message: 'Selecione uma imagem!', severity: 'error' });
      return;
    }
    setLoading(true);
    setResult(null);
    try {
      const formData = new FormData();
      formData.append('file', file);
      const response = await axios.post('http://localhost:8000/classify-fruit', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      setResult(response.data);
    } catch (error: any) {
      setSnackbar({ open: true, message: error.response?.data?.detail || 'Erro ao verificar fruta', severity: 'error' });
    } finally {
      setLoading(false);
    }
  };

  const handleCloseSnackbar = () => {
    setSnackbar(prev => ({ ...prev, open: false }));
  };

  return (
    <Box sx={{ display: 'flex', minHeight: '100vh' }}>
      <Sidebar />
      <Box component="main" sx={{ flexGrow: 1, p: 3, background: 'linear-gradient(135deg, #f5f7ff 0%, #e8eaff 100%)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        <Container maxWidth="sm">
          <Paper elevation={3} sx={{ p: 5, textAlign: 'center', background: 'rgba(255,255,255,0.95)' }}>
            <Typography variant="h4" sx={{ mb: 3, fontWeight: 600, color: '#667eea' }}>
              Verificar Fruta
            </Typography>
            <form onSubmit={handleSubmit}>
              <Button variant="contained" component="label" sx={{ mb: 2 }}>
                Selecionar Imagem
                <input type="file" accept="image/*" hidden onChange={handleFileChange} />
              </Button>
              <Box sx={{ mb: 2 }}>
                <Button type="submit" variant="contained" color="primary" disabled={loading}>
                  {loading ? <CircularProgress size={24} color="inherit" /> : 'Verificar'}
                </Button>
              </Box>
            </form>
            {file && (
              <Box sx={{ mt: 3, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                <img
                  src={URL.createObjectURL(file)}
                  alt="Imagem selecionada"
                  style={{ maxWidth: '100%', maxHeight: 250, borderRadius: 8, marginBottom: 16 }}
                />
                {result && (
                  <>
                    <Typography variant="h6" sx={{ color: result.classe === 'Podre' ? 'red' : 'green', fontWeight: 700 }}>
                      Resultado: {result.classe}
                    </Typography>
                    <Typography variant="body1">
                      Probabilidade: {(result.probabilidade * 100).toFixed(2)}%
                    </Typography>
                  </>
                )}
              </Box>
            )}
          </Paper>
        </Container>
        <Snackbar open={snackbar.open} autoHideDuration={4000} onClose={handleCloseSnackbar}>
          <Alert onClose={handleCloseSnackbar} severity={snackbar.severity} sx={{ width: '100%' }}>
            {snackbar.message}
          </Alert>
        </Snackbar>
      </Box>
    </Box>
  );
};

export default VerificarFruta; 
import { useState, useEffect } from 'react';
import {
  Box,
  Button,
  Container,
  Paper,
  Typography,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  IconButton,
  Snackbar,
  Alert,
  MenuItem,
  Select,
  InputLabel,
  FormControl
} from '@mui/material';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import AddIcon from '@mui/icons-material/Add';
import Sidebar from '../components/Sidebar';
import axios from 'axios';

interface Sale {
  id: number;
  value: number;
  quantity: number;
  fruit: string;
  created_at: string;
  store_id: number;
}

interface Store {
  id: number;
  name: string;
}

const Sales = () => {
  const [sales, setSales] = useState<Sale[]>([]);
  const [stores, setStores] = useState<Store[]>([]);
  const [openDialog, setOpenDialog] = useState(false);
  const [editingSale, setEditingSale] = useState<Sale | null>(null);
  const [formData, setFormData] = useState({
    value: '',
    quantity: '',
    fruit: '',
    store_id: ''
  });
  const [snackbar, setSnackbar] = useState({
    open: false,
    message: '',
    severity: 'success' as 'success' | 'error'
  });

  const fetchSales = async () => {
    try {
      const response = await axios.get('http://localhost:8000/sales/', {
        withCredentials: true
      });
      if (Array.isArray(response.data)) {
        setSales(response.data);
      } else {
        setSales([]);
      }
    } catch (error) {
      setSales([]);
      showSnackbar('Erro ao carregar vendas', 'error');
    }
  };

  const fetchStores = async () => {
    try {
      const response = await axios.get('http://localhost:8000/stores/', {
        withCredentials: true
      });
      if (Array.isArray(response.data)) {
        setStores(response.data);
      }
    } catch (error) {
      setStores([]);
    }
  };

  useEffect(() => {
    fetchSales();
    fetchStores();
  }, []);

  const handleOpenDialog = (sale?: Sale) => {
    if (sale) {
      setEditingSale(sale);
      setFormData({
        value: sale.value.toString(),
        quantity: sale.quantity.toString(),
        fruit: sale.fruit,
        store_id: sale.store_id.toString()
      });
    } else {
      setEditingSale(null);
      setFormData({
        value: '',
        quantity: '',
        fruit: '',
        store_id: ''
      });
    }
    setOpenDialog(true);
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
    setEditingSale(null);
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSelectChange = (e: any) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async () => {
    try {
      const data = {
        value: parseFloat(formData.value),
        quantity: parseInt(formData.quantity),
        fruit: formData.fruit,
        store_id: parseInt(formData.store_id)
      };
      if (editingSale) {
        await axios.put(`http://localhost:8000/sales/${editingSale.id}`, data, {
          withCredentials: true
        });
        showSnackbar('Venda atualizada com sucesso!', 'success');
      } else {
        await axios.post('http://localhost:8000/sales/', data, {
          withCredentials: true
        });
        showSnackbar('Venda criada com sucesso!', 'success');
      }
      handleCloseDialog();
      setTimeout(() => {
        fetchSales();
      }, 500);
    } catch (error) {
      showSnackbar('Erro ao salvar venda', 'error');
    }
  };

  const handleDelete = async (id: number) => {
    if (window.confirm('Tem certeza que deseja excluir esta venda?')) {
      try {
        await axios.delete(`http://localhost:8000/sales/${id}`, {
          withCredentials: true
        });
        showSnackbar('Venda excluída com sucesso!', 'success');
        setTimeout(() => {
          fetchSales();
        }, 500);
      } catch (error) {
        showSnackbar('Erro ao excluir venda', 'error');
      }
    }
  };

  const showSnackbar = (message: string, severity: 'success' | 'error') => {
    setSnackbar({ open: true, message, severity });
  };

  const handleCloseSnackbar = () => {
    setSnackbar(prev => ({ ...prev, open: false }));
  };

  return (
    <Box sx={{ display: 'flex', minHeight: '100vh' }}>
      <Sidebar />
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: 3,
          background: 'linear-gradient(135deg, #f5f7ff 0%, #e8eaff 100%)',
        }}
      >
        <Container maxWidth="lg">
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 4 }}>
            <Typography variant="h4" sx={{ color: '#1a237e', fontWeight: 600 }}>
              Vendas
            </Typography>
            <Button
              variant="contained"
              startIcon={<AddIcon />}
              onClick={() => handleOpenDialog()}
              sx={{
                background: 'linear-gradient(45deg, #667eea 30%, #764ba2 90%)',
                color: 'white',
                '&:hover': {
                  background: 'linear-gradient(45deg, #5a6fd6 30%, #6a3d9e 90%)',
                },
              }}
            >
              Nova Venda
            </Button>
          </Box>

          <TableContainer component={Paper} sx={{ boxShadow: 3 }}>
            <Table>
              <TableHead>
                <TableRow sx={{ backgroundColor: '#f5f5f5' }}>
                  <TableCell>Fruta</TableCell>
                  <TableCell>Quantidade</TableCell>
                  <TableCell>Valor</TableCell>
                  <TableCell>Loja</TableCell>
                  <TableCell>Data</TableCell>
                  <TableCell>Ações</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {sales.length === 0 ? (
                  <TableRow>
                    <TableCell colSpan={6} align="center">
                      <Typography variant="body1" sx={{ py: 2, color: 'text.secondary' }}>
                        Nenhuma venda registrada
                      </Typography>
                    </TableCell>
                  </TableRow>
                ) : (
                  sales.map((sale) => (
                    <TableRow key={sale.id}>
                      <TableCell>{sale.fruit}</TableCell>
                      <TableCell>{sale.quantity}</TableCell>
                      <TableCell>R$ {sale.value.toFixed(2)}</TableCell>
                      <TableCell>
                        {stores.find(store => store.id === sale.store_id)?.name}
                      </TableCell>
                      <TableCell>
                        {new Date(sale.created_at).toLocaleDateString()}
                      </TableCell>
                      <TableCell>
                        <IconButton
                          color="primary"
                          onClick={() => handleOpenDialog(sale)}
                          sx={{ mr: 1 }}
                        >
                          <EditIcon />
                        </IconButton>
                        <IconButton
                          color="error"
                          onClick={() => handleDelete(sale.id)}
                        >
                          <DeleteIcon />
                        </IconButton>
                      </TableCell>
                    </TableRow>
                  ))
                )}
              </TableBody>
            </Table>
          </TableContainer>

          <Dialog open={openDialog} onClose={handleCloseDialog} maxWidth="sm" fullWidth>
            <DialogTitle>
              {editingSale ? 'Editar Venda' : 'Nova Venda'}
            </DialogTitle>
            <DialogContent>
              <FormControl fullWidth sx={{ mt: 2, mb: 2 }}>
                <InputLabel>Loja</InputLabel>
                <Select
                  name="store_id"
                  value={formData.store_id}
                  label="Loja"
                  onChange={handleSelectChange}
                  required
                >
                  {stores.map((store) => (
                    <MenuItem key={store.id} value={store.id}>
                      {store.name}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
              <TextField
                fullWidth
                label="Fruta"
                name="fruit"
                value={formData.fruit}
                onChange={handleInputChange}
                required
                sx={{ mb: 2 }}
              />
              <TextField
                fullWidth
                label="Quantidade"
                name="quantity"
                type="number"
                value={formData.quantity}
                onChange={handleInputChange}
                required
                sx={{ mb: 2 }}
              />
              <TextField
                fullWidth
                label="Valor"
                name="value"
                type="number"
                value={formData.value}
                onChange={handleInputChange}
                required
                sx={{ mb: 2 }}
              />
            </DialogContent>
            <DialogActions>
              <Button onClick={handleCloseDialog}>Cancelar</Button>
              <Button onClick={handleSubmit} variant="contained">
                Salvar
              </Button>
            </DialogActions>
          </Dialog>

          <Snackbar
            open={snackbar.open}
            autoHideDuration={6000}
            onClose={handleCloseSnackbar}
            anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
          >
            <Alert
              onClose={handleCloseSnackbar}
              severity={snackbar.severity}
              sx={{ width: '100%' }}
            >
              {snackbar.message}
            </Alert>
          </Snackbar>
        </Container>
      </Box>
    </Box>
  );
};

export default Sales; 
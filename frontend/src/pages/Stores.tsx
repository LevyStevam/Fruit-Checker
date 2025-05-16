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
  Alert
} from '@mui/material';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import AddIcon from '@mui/icons-material/Add';
import Sidebar from '../components/Sidebar';
import axios from 'axios';

interface Store {
  id: number;
  name: string;
  cnpj: string;
  employees: number;
  address: string;
  phone: string;
  email: string;
}

const Stores = () => {
  const [stores, setStores] = useState<Store[]>([]);
  const [openDialog, setOpenDialog] = useState(false);
  const [editingStore, setEditingStore] = useState<Store | null>(null);
  const [formData, setFormData] = useState({
    name: '',
    cnpj: '',
    employees: 0,
    address: '',
    phone: '',
    email: ''
  });
  const [snackbar, setSnackbar] = useState({
    open: false,
    message: '',
    severity: 'success' as 'success' | 'error'
  });

  const fetchStores = async () => {
    try {
      const response = await axios.get('http://localhost:8000/stores/', {
        withCredentials: true
      });
      console.log('Resposta da API:', response.data);
      if (Array.isArray(response.data)) {
        setStores(response.data);
      } else {
        console.error('Dados recebidos não são um array:', response.data);
        setStores([]);
      }
    } catch (error) {
      console.error('Erro ao buscar lojas:', error);
      showSnackbar('Erro ao carregar lojas', 'error');
      setStores([]);
    }
  };

  useEffect(() => {
    fetchStores();
  }, []);

  const handleOpenDialog = (store?: Store) => {
    if (store) {
      setEditingStore(store);
      setFormData({
        name: store.name,
        cnpj: store.cnpj,
        employees: store.employees,
        address: store.address,
        phone: store.phone || '',
        email: store.email || ''
      });
    } else {
      setEditingStore(null);
      setFormData({
        name: '',
        cnpj: '',
        employees: 0,
        address: '',
        phone: '',
        email: ''
      });
    }
    setOpenDialog(true);
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
    setEditingStore(null);
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name === 'employees' ? Number(value) : value
    }));
  };

  const handleSubmit = async () => {
    try {
      if (editingStore) {
        await axios.put(`http://localhost:8000/stores/${editingStore.id}`, formData, {
          withCredentials: true
        });
        showSnackbar('Loja atualizada com sucesso!', 'success');
      } else {
        const response = await axios.post('http://localhost:8000/stores/', formData, {
          withCredentials: true
        });
        console.log('Loja criada:', response.data);
        showSnackbar('Loja criada com sucesso!', 'success');
      }
      handleCloseDialog();
      setTimeout(() => {
        fetchStores();
      }, 500);
    } catch (error) {
      console.error('Erro ao salvar loja:', error);
      showSnackbar('Erro ao salvar loja', 'error');
    }
  };

  const handleDelete = async (id: number) => {
    if (window.confirm('Tem certeza que deseja excluir esta loja?')) {
      try {
        await axios.delete(`http://localhost:8000/stores/${id}`, {
          withCredentials: true
        });
        showSnackbar('Loja excluída com sucesso!', 'success');
        setTimeout(() => {
          fetchStores();
        }, 500);
      } catch (error) {
        console.error('Erro ao excluir loja:', error);
        showSnackbar('Erro ao excluir loja', 'error');
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
              Minhas Lojas
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
              Nova Loja
            </Button>
          </Box>

          <TableContainer component={Paper} sx={{ boxShadow: 3 }}>
            <Table>
              <TableHead>
                <TableRow sx={{ backgroundColor: '#f5f5f5' }}>
                  <TableCell>Nome</TableCell>
                  <TableCell>CNPJ</TableCell>
                  <TableCell>Funcionários</TableCell>
                  <TableCell>Endereço</TableCell>
                  <TableCell>Ações</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {stores.length === 0 ? (
                  <TableRow>
                    <TableCell colSpan={5} align="center">
                      <Typography variant="body1" sx={{ py: 2, color: 'text.secondary' }}>
                        Nenhuma loja cadastrada
                      </Typography>
                    </TableCell>
                  </TableRow>
                ) : (
                  stores.map((store) => (
                    <TableRow key={store.id}>
                      <TableCell>{store.name}</TableCell>
                      <TableCell>{store.cnpj}</TableCell>
                      <TableCell>{store.employees}</TableCell>
                      <TableCell>{store.address}</TableCell>
                      <TableCell>
                        <IconButton
                          color="primary"
                          onClick={() => handleOpenDialog(store)}
                          sx={{ mr: 1 }}
                        >
                          <EditIcon />
                        </IconButton>
                        <IconButton
                          color="error"
                          onClick={() => handleDelete(store.id)}
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
        </Container>

        <Dialog open={openDialog} onClose={handleCloseDialog} maxWidth="sm" fullWidth>
          <DialogTitle>
            {editingStore ? 'Editar Loja' : 'Nova Loja'}
          </DialogTitle>
          <DialogContent>
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, pt: 2 }}>
              <TextField
                name="name"
                label="Nome da Loja"
                value={formData.name}
                onChange={handleInputChange}
                fullWidth
                required
              />
              <TextField
                name="cnpj"
                label="CNPJ"
                value={formData.cnpj}
                onChange={handleInputChange}
                fullWidth
                required
              />
              <TextField
                name="employees"
                label="Número de Funcionários"
                type="number"
                value={formData.employees}
                onChange={handleInputChange}
                fullWidth
                required
              />
              <TextField
                name="address"
                label="Endereço"
                value={formData.address}
                onChange={handleInputChange}
                fullWidth
                required
              />
              <TextField
                name="phone"
                label="Telefone"
                value={formData.phone}
                onChange={handleInputChange}
                fullWidth
              />
              <TextField
                name="email"
                label="Email"
                type="email"
                value={formData.email}
                onChange={handleInputChange}
                fullWidth
              />
            </Box>
          </DialogContent>
          <DialogActions>
            <Button onClick={handleCloseDialog}>Cancelar</Button>
            <Button onClick={handleSubmit} variant="contained" color="primary">
              {editingStore ? 'Atualizar' : 'Criar'}
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
      </Box>
    </Box>
  );
};

export default Stores; 
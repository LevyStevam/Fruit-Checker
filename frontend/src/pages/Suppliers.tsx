import { useState, useEffect } from 'react';
import {
  Box, Button, Container, Paper, Typography, Table, TableBody,
  TableCell, TableContainer, TableHead, TableRow, Dialog, DialogTitle,
  DialogContent, DialogActions, TextField, IconButton, Snackbar, Alert,
  MenuItem, Select, InputLabel, FormControl
} from '@mui/material';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import AddIcon from '@mui/icons-material/Add';
import Sidebar from '../components/Sidebar';
import axios from 'axios';

// Interfaces
interface Supplier {
  id: number;
  name: string;
  cnpj: string;
  address: string;
  fruits: string;
  store_id: number;
}

interface Store {
  id: number;
  name: string;
}

const SuppliersPage = () => {
  const [suppliers, setSuppliers] = useState<Supplier[]>([]);
  const [stores, setStores] = useState<Store[]>([]);
  const [openDialog, setOpenDialog] = useState(false);
  const [editingSupplier, setEditingSupplier] = useState<Supplier | null>(null);
  const [formData, setFormData] = useState({
    name: '',
    cnpj: '',
    address: '',
    fruits: '',
    store_id: ''
  });
  const [snackbar, setSnackbar] = useState({
    open: false,
    message: '',
    severity: 'success' as 'success' | 'error'
  });

  const fetchStores = async () => {
    try {
      const response = await axios.get('http://localhost:8000/stores/', { withCredentials: true });
      if (Array.isArray(response.data)) {
        setStores(response.data);
        return response.data;
      }
      return [];
    } catch (error) {
      setStores([]);
      showSnackbar('Erro ao carregar lojas', 'error');
      return [];
    }
  };

  const fetchSuppliers = async (currentStores: Store[]) => {
    if (currentStores.length === 0) {
      setSuppliers([]);
      return;
    }
    try {
      const supplierPromises = currentStores.map(store =>
        axios.get(`http://localhost:8000/suppliers/store/${store.id}`, { withCredentials: true })
      );
      const responses = await Promise.all(supplierPromises);
      const allSuppliers = responses.flatMap(response => response.data);
      setSuppliers(allSuppliers);
    } catch (error) {
      setSuppliers([]);
      showSnackbar('Erro ao carregar fornecedores', 'error');
    }
  };

  const loadData = async () => {
    const fetchedStores = await fetchStores();
    await fetchSuppliers(fetchedStores);
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleOpenDialog = (supplier?: Supplier) => {
    if (supplier) {
      setEditingSupplier(supplier);
      setFormData({
        name: supplier.name,
        cnpj: supplier.cnpj,
        address: supplier.address,
        fruits: supplier.fruits,
        store_id: supplier.store_id.toString()
      });
    } else {
      setEditingSupplier(null);
      setFormData({ name: '', cnpj: '', address: '', fruits: '', store_id: '' });
    }
    setOpenDialog(true);
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
    setEditingSupplier(null);
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData(prev => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleSelectChange = (e: any) => {
    setFormData(prev => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleSubmit = async () => {
    try {
      const data = {
        ...formData,
        store_id: parseInt(formData.store_id)
      };

      if (editingSupplier) {
        await axios.put(`http://localhost:8000/suppliers/${editingSupplier.id}`, data, { withCredentials: true });
        showSnackbar('Fornecedor atualizado com sucesso!', 'success');
      } else {
        await axios.post('http://localhost:8000/suppliers/', data, { withCredentials: true });
        showSnackbar('Fornecedor criado com sucesso!', 'success');
      }
      handleCloseDialog();
      setTimeout(loadData, 500);
    } catch (error: any) {
      const errorMessage = error.response?.data?.detail || 'Erro ao salvar fornecedor';
      showSnackbar(errorMessage, 'error');
    }
  };

  const handleDelete = async (id: number) => {
    if (window.confirm('Tem certeza que deseja excluir este fornecedor?')) {
      try {
        await axios.delete(`http://localhost:8000/suppliers/${id}`, { withCredentials: true });
        showSnackbar('Fornecedor excluído com sucesso!', 'success');
        setTimeout(loadData, 500);
      } catch (error) {
        showSnackbar('Erro ao excluir fornecedor', 'error');
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
      <Box component="main" sx={{ flexGrow: 1, p: 3, background: 'linear-gradient(135deg, #f5f7ff 0%, #e8eaff 100%)' }}>
        <Container maxWidth="lg">
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 4 }}>
            <Typography variant="h4" sx={{ color: '#1a237e', fontWeight: 600 }}>Fornecedores</Typography>
            <Button
              variant="contained" startIcon={<AddIcon />} onClick={() => handleOpenDialog()}
              sx={{ background: 'linear-gradient(45deg, #667eea 30%, #764ba2 90%)', color: 'white', '&:hover': { background: 'linear-gradient(45deg, #5a6fd6 30%, #6a3d9e 90%)' } }}
            >
              Novo Fornecedor
            </Button>
          </Box>

          <TableContainer component={Paper} sx={{ boxShadow: 3 }}>
            <Table>
              <TableHead><TableRow sx={{ backgroundColor: '#f5f5f5' }}><TableCell>Nome</TableCell><TableCell>CNPJ</TableCell><TableCell>Frutas Fornecidas</TableCell><TableCell>Loja</TableCell><TableCell>Ações</TableCell></TableRow></TableHead>
              <TableBody>
                {suppliers.length === 0 ? (
                  <TableRow><TableCell colSpan={5} align="center"><Typography sx={{ py: 2, color: 'text.secondary' }}>Nenhum fornecedor cadastrado</Typography></TableCell></TableRow>
                ) : (
                  suppliers.map((supplier) => (
                    <TableRow key={supplier.id}>
                      <TableCell>{supplier.name}</TableCell>
                      <TableCell>{supplier.cnpj}</TableCell>
                      <TableCell>{supplier.fruits}</TableCell>
                      <TableCell>{stores.find(store => store.id === supplier.store_id)?.name}</TableCell>
                      <TableCell>
                        <IconButton color="primary" onClick={() => handleOpenDialog(supplier)} sx={{ mr: 1 }}><EditIcon /></IconButton>
                        <IconButton color="error" onClick={() => handleDelete(supplier.id)}><DeleteIcon /></IconButton>
                      </TableCell>
                    </TableRow>
                  ))
                )}
              </TableBody>
            </Table>
          </TableContainer>

          <Dialog open={openDialog} onClose={handleCloseDialog} maxWidth="sm" fullWidth>
            <DialogTitle>{editingSupplier ? 'Editar Fornecedor' : 'Novo Fornecedor'}</DialogTitle>
            <DialogContent>
              <FormControl fullWidth sx={{ mt: 2, mb: 2 }}>
                <InputLabel>Loja</InputLabel>
                <Select name="store_id" value={formData.store_id} label="Loja" onChange={handleSelectChange} required>
                  {stores.map((store) => (<MenuItem key={store.id} value={store.id}>{store.name}</MenuItem>))}
                </Select>
              </FormControl>
              <TextField fullWidth label="Nome" name="name" value={formData.name} onChange={handleInputChange} required sx={{ mb: 2 }} />
              <TextField fullWidth label="CNPJ" name="cnpj" value={formData.cnpj} onChange={handleInputChange} required sx={{ mb: 2 }} />
              <TextField fullWidth label="Endereço" name="address" value={formData.address} onChange={handleInputChange} required sx={{ mb: 2 }} />
              <TextField fullWidth label="Frutas (separadas por vírgula)" name="fruits" value={formData.fruits} onChange={handleInputChange} required sx={{ mb: 2 }} />
            </DialogContent>
            <DialogActions>
              <Button onClick={handleCloseDialog}>Cancelar</Button>
              <Button onClick={handleSubmit} variant="contained">Salvar</Button>
            </DialogActions>
          </Dialog>

          <Snackbar open={snackbar.open} autoHideDuration={6000} onClose={handleCloseSnackbar} anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}>
            <Alert onClose={handleCloseSnackbar} severity={snackbar.severity} sx={{ width: '100%' }}>{snackbar.message}</Alert>
          </Snackbar>
        </Container>
      </Box>
    </Box>
  );
};

export default SuppliersPage; 
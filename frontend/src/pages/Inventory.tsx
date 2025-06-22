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

// Interface for Inventory Item
interface InventoryItem {
  id: number;
  fruit: string;
  quantity: number;
  unit: string;
  store_id: number;
  created_at: string;
  updated_at: string;
}

// Interface for Store
interface Store {
  id: number;
  name: string;
}

const InventoryPage = () => {
  const [inventoryItems, setInventoryItems] = useState<InventoryItem[]>([]);
  const [stores, setStores] = useState<Store[]>([]);
  const [openDialog, setOpenDialog] = useState(false);
  const [editingItem, setEditingItem] = useState<InventoryItem | null>(null);
  const [formData, setFormData] = useState({
    fruit: '',
    quantity: '',
    unit: '',
    store_id: ''
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

  const fetchInventory = async (currentStores: Store[]) => {
    if (currentStores.length === 0) {
        setInventoryItems([]);
        return;
    }
    try {
        const inventoryPromises = currentStores.map(store =>
            axios.get(`http://localhost:8000/inventory/store/${store.id}`, {
              withCredentials: true
            })
        );
        const responses = await Promise.all(inventoryPromises);
        const allInventory = responses.flatMap(response => response.data);
        setInventoryItems(allInventory);
    } catch (error) {
      setInventoryItems([]);
      showSnackbar('Erro ao carregar estoque', 'error');
    }
  };

  const loadData = async () => {
    const fetchedStores = await fetchStores();
    await fetchInventory(fetchedStores);
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleOpenDialog = (item?: InventoryItem) => {
    if (item) {
      setEditingItem(item);
      setFormData({
        fruit: item.fruit,
        quantity: item.quantity.toString(),
        unit: item.unit,
        store_id: item.store_id.toString()
      });
    } else {
      setEditingItem(null);
      setFormData({
        fruit: '',
        quantity: '',
        unit: '',
        store_id: ''
      });
    }
    setOpenDialog(true);
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
    setEditingItem(null);
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
      if (editingItem) {
        // Update
        const data = {
            quantity: parseInt(formData.quantity),
            unit: formData.unit,
        };
        await axios.put(`http://localhost:8000/inventory/${editingItem.id}`, data, {
          withCredentials: true
        });
        showSnackbar('Item atualizado com sucesso!', 'success');
      } else {
        // Create
        const data = {
            fruit: formData.fruit,
            quantity: parseInt(formData.quantity),
            unit: formData.unit,
            store_id: parseInt(formData.store_id)
        };
        await axios.post('http://localhost:8000/inventory/', data, {
          withCredentials: true
        });
        showSnackbar('Item criado com sucesso!', 'success');
      }
      handleCloseDialog();
      setTimeout(loadData, 500);
    } catch (error: any) {
      const errorMessage = error.response?.data?.detail || 'Erro ao salvar item';
      showSnackbar(errorMessage, 'error');
    }
  };

  const handleDelete = async (id: number) => {
    if (window.confirm('Tem certeza que deseja excluir este item do estoque?')) {
      try {
        await axios.delete(`http://localhost:8000/inventory/${id}`, {
          withCredentials: true
        });
        showSnackbar('Item excluído com sucesso!', 'success');
        setTimeout(loadData, 500);
      } catch (error) {
        showSnackbar('Erro ao excluir item', 'error');
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
              Estoque
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
              Novo Item
            </Button>
          </Box>

          <TableContainer component={Paper} sx={{ boxShadow: 3 }}>
            <Table>
              <TableHead>
                <TableRow sx={{ backgroundColor: '#f5f5f5' }}>
                  <TableCell>Fruta</TableCell>
                  <TableCell>Quantidade</TableCell>
                  <TableCell>Unidade</TableCell>
                  <TableCell>Loja</TableCell>
                  <TableCell>Última Atualização</TableCell>
                  <TableCell>Ações</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {inventoryItems.length === 0 ? (
                  <TableRow>
                    <TableCell colSpan={6} align="center">
                      <Typography variant="body1" sx={{ py: 2, color: 'text.secondary' }}>
                        Nenhum item no estoque
                      </Typography>
                    </TableCell>
                  </TableRow>
                ) : (
                  inventoryItems.map((item) => (
                    <TableRow key={item.id}>
                      <TableCell>{item.fruit}</TableCell>
                      <TableCell>{item.quantity}</TableCell>
                      <TableCell>{item.unit}</TableCell>
                      <TableCell>
                        {stores.find(store => store.id === item.store_id)?.name}
                      </TableCell>
                      <TableCell>
                        {new Date(item.updated_at).toLocaleString()}
                      </TableCell>
                      <TableCell>
                        <IconButton
                          color="primary"
                          onClick={() => handleOpenDialog(item)}
                          sx={{ mr: 1 }}
                        >
                          <EditIcon />
                        </IconButton>
                        <IconButton
                          color="error"
                          onClick={() => handleDelete(item.id)}
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
              {editingItem ? 'Editar Item do Estoque' : 'Novo Item no Estoque'}
            </DialogTitle>
            <DialogContent>
              <FormControl fullWidth sx={{ mt: 2, mb: 2 }} disabled={!!editingItem}>
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
                disabled={!!editingItem}
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
                label="Unidade (ex: kg, un)"
                name="unit"
                value={formData.unit}
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

export default InventoryPage; 
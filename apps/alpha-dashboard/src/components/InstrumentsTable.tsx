import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Pagination,
  CircularProgress,
  Alert,
  TextField,
  InputAdornment,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Chip,
  Grid,
  Button,
} from '@mui/material';
import { Search as SearchIcon, Clear as ClearIcon } from '@mui/icons-material';
import { instrumentsApi } from '../services/api';
import type { Instrument, InstrumentsResponse } from '../types';

interface SearchFilters {
  search: string;
  exchange: string;
  instrumentType: string;
}

const InstrumentsTable: React.FC = () => {
  const [instruments, setInstruments] = useState<Instrument[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [page, setPage] = useState<number>(1);
  const [totalPages, setTotalPages] = useState<number>(1);
  const [totalItems, setTotalItems] = useState<number>(0);
  const [filters, setFilters] = useState<SearchFilters>({
    search: '',
    exchange: '',
    instrumentType: '',
  });
  const pageSize = 50;

  // Common exchange and instrument type options
  const exchangeOptions = ['NSE', 'BSE', 'NFO', 'BFO', 'CDS', 'MCX'];
  const instrumentTypeOptions = [
    'EQ',
    'FUT',
    'OPT',
    'CE',
    'PE',
    'FUTCOM',
    'OPTCOM',
  ];

  const fetchInstruments = async (
    currentPage: number,
    filters: SearchFilters
  ) => {
    setLoading(true);
    setError(null);

    try {
      const response = await instrumentsApi.searchInstruments(
        currentPage,
        pageSize,
        filters.search || undefined,
        filters.exchange || undefined,
        filters.instrumentType || undefined
      );
      setInstruments(response.data.instruments);
      setTotalPages(response.data.pagination.total_pages);
      setTotalItems(response.data.pagination.total_items);
    } catch (err) {
      setError('Failed to fetch instruments. Please try again.');
      console.error('Error fetching instruments:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchInstruments(page, filters);
  }, [page, filters]);

  const handlePageChange = (_: React.ChangeEvent<unknown>, value: number) => {
    setPage(value);
  };

  const handleFilterChange = (
    filterName: keyof SearchFilters,
    value: string
  ) => {
    setFilters((prev) => ({
      ...prev,
      [filterName]: value,
    }));
    setPage(1); // Reset to first page when filtering
  };

  const handleClearFilters = () => {
    setFilters({
      search: '',
      exchange: '',
      instrumentType: '',
    });
    setPage(1);
  };

  const hasActiveFilters =
    filters.search || filters.exchange || filters.instrumentType;

  const getColumns = () => {
    if (instruments.length === 0) return [];

    const sampleInstrument = instruments[0];
    const commonColumns = [
      'symbol',
      'name',
      'token',
      'instrumenttype',
      'exch_seg',
      'lotsize',
      'tick_size',
    ];

    return commonColumns.filter((col) => sampleInstrument.hasOwnProperty(col));
  };

  const formatCellValue = (value: any) => {
    if (value === null || value === undefined) return '-';
    if (typeof value === 'number') {
      return value.toLocaleString();
    }
    return String(value);
  };

  return (
    <Box sx={{ width: '100%' }}>
      <Typography variant="h5" fontWeight="bold" sx={{ mb: 3 }}>
        Instruments
      </Typography>

      {/* Filters Section */}
      <Box sx={{ mb: 3 }}>
        <Grid container spacing={2} alignItems="center">
          <Grid item xs={12} md={4}>
            <TextField
              fullWidth
              placeholder="Search instruments..."
              value={filters.search}
              onChange={(e) => handleFilterChange('search', e.target.value)}
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <SearchIcon />
                  </InputAdornment>
                ),
              }}
            />
          </Grid>

          <Grid item xs={12} md={3}>
            <FormControl fullWidth>
              <InputLabel>Exchange</InputLabel>
              <Select
                value={filters.exchange}
                label="Exchange"
                onChange={(e) => handleFilterChange('exchange', e.target.value)}
              >
                <MenuItem value="">All Exchanges</MenuItem>
                {exchangeOptions.map((exchange) => (
                  <MenuItem key={exchange} value={exchange}>
                    {exchange}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>

          <Grid item xs={12} md={3}>
            <FormControl fullWidth>
              <InputLabel>Instrument Type</InputLabel>
              <Select
                value={filters.instrumentType}
                label="Instrument Type"
                onChange={(e) =>
                  handleFilterChange('instrumentType', e.target.value)
                }
              >
                <MenuItem value="">All Types</MenuItem>
                {instrumentTypeOptions.map((type) => (
                  <MenuItem key={type} value={type}>
                    {type}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>

          <Grid item xs={12} md={2}>
            <Button
              variant="outlined"
              startIcon={<ClearIcon />}
              onClick={handleClearFilters}
              disabled={!hasActiveFilters}
              fullWidth
            >
              Clear
            </Button>
          </Grid>
        </Grid>

        {/* Active Filters Display */}
        {hasActiveFilters && (
          <Box sx={{ mt: 2, display: 'flex', gap: 1, flexWrap: 'wrap' }}>
            {filters.search && (
              <Chip
                label={`Search: ${filters.search}`}
                onDelete={() => handleFilterChange('search', '')}
                size="small"
              />
            )}
            {filters.exchange && (
              <Chip
                label={`Exchange: ${filters.exchange}`}
                onDelete={() => handleFilterChange('exchange', '')}
                size="small"
              />
            )}
            {filters.instrumentType && (
              <Chip
                label={`Type: ${filters.instrumentType}`}
                onDelete={() => handleFilterChange('instrumentType', '')}
                size="small"
              />
            )}
          </Box>
        )}
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      {loading ? (
        <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}>
          <CircularProgress />
        </Box>
      ) : (
        <>
          <TableContainer
            component={Paper}
            sx={{
              bgcolor: 'background.paper',
              maxHeight: 600,
              overflow: 'auto',
            }}
          >
            <Table stickyHeader>
              <TableHead>
                <TableRow>
                  {getColumns().map((column) => (
                    <TableCell key={column} sx={{ fontWeight: 'bold' }}>
                      {column.replace('_', ' ').toUpperCase()}
                    </TableCell>
                  ))}
                </TableRow>
              </TableHead>
              <TableBody>
                {instruments.map((instrument, index) => (
                  <TableRow key={index}>
                    {getColumns().map((column) => (
                      <TableCell key={column}>
                        {formatCellValue(instrument[column])}
                      </TableCell>
                    ))}
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>

          {totalPages > 1 && (
            <Box sx={{ display: 'flex', justifyContent: 'center', mt: 3 }}>
              <Pagination
                count={totalPages}
                page={page}
                onChange={handlePageChange}
                color="primary"
                showFirstButton
                showLastButton
              />
            </Box>
          )}

          <Typography variant="body2" color="text.secondary" sx={{ mt: 2 }}>
            Showing {instruments.length} of {totalItems} instruments
            {hasActiveFilters && ' (filtered)'}
          </Typography>
        </>
      )}
    </Box>
  );
};

export default InstrumentsTable;

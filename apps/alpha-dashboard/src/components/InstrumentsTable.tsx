import React, { useState, useEffect } from 'react'
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
  InputAdornment
} from '@mui/material'
import { Search as SearchIcon } from '@mui/icons-material'
import { instrumentsApi } from '../services/api'
import type { Instrument, InstrumentsResponse } from '../types'

const InstrumentsTable: React.FC = () => {
  const [instruments, setInstruments] = useState<Instrument[]>([])
  const [loading, setLoading] = useState<boolean>(false)
  const [error, setError] = useState<string | null>(null)
  const [page, setPage] = useState<number>(1)
  const [totalPages, setTotalPages] = useState<number>(1)
  const [searchTerm, setSearchTerm] = useState<string>('')
  const pageSize = 50

  const fetchInstruments = async (currentPage: number, search?: string) => {
    setLoading(true)
    setError(null)
    
    try {
      const response = await instrumentsApi.getInstruments(currentPage, pageSize, search)
      setInstruments(response.data.instruments)
      setTotalPages(response.data.pagination.total_pages)
    } catch (err) {
      setError('Failed to fetch instruments. Please try again.')
      console.error('Error fetching instruments:', err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchInstruments(page, searchTerm)
  }, [page, searchTerm])

  const handlePageChange = (_: React.ChangeEvent<unknown>, value: number) => {
    setPage(value)
  }

  const handleSearchChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(event.target.value)
    setPage(1) // Reset to first page when searching
  }

  const getColumns = () => {
    if (instruments.length === 0) return []
    
    const sampleInstrument = instruments[0]
    const commonColumns = ['symbol', 'name', 'token', 'instrumenttype', 'exch_seg', 'lotsize', 'tick_size']
    
    return commonColumns.filter(col => sampleInstrument.hasOwnProperty(col))
  }

  const formatCellValue = (value: any) => {
    if (value === null || value === undefined) return '-'
    if (typeof value === 'number') {
      return value.toLocaleString()
    }
    return String(value)
  }

  return (
    <Box sx={{ width: '100%' }}>
      <Typography variant="h5" fontWeight="bold" sx={{ mb: 3 }}>
        Instruments
      </Typography>
      
      <Box sx={{ mb: 3 }}>
        <TextField
          fullWidth
          placeholder="Search instruments..."
          value={searchTerm}
          onChange={handleSearchChange}
          InputProps={{
            startAdornment: (
              <InputAdornment position="start">
                <SearchIcon />
              </InputAdornment>
            ),
          }}
          sx={{ maxWidth: 400 }}
        />
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
              overflow: 'auto'
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
            Showing {instruments.length} instruments
          </Typography>
        </>
      )}
    </Box>
  )
}

export default InstrumentsTable

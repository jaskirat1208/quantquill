import React, { useState, useEffect, useCallback } from 'react'
import {
  Box,
  Typography,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  TextField,
  Button,
  Paper,
  CircularProgress,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Chip,
  IconButton,
  InputAdornment,
  FormControlLabel,
  Switch
} from '@mui/material'
import { Clear } from '@mui/icons-material'
import { useTheme } from '@mui/material/styles'
import { AgGridReact } from 'ag-grid-react'
import 'ag-grid-community/styles/ag-grid.css'
import 'ag-grid-community/styles/ag-theme-quartz.css'
import { oiMonitorApi, instrumentsApi } from '../services/api'

const OIMonitorPage: React.FC = () => {
  const theme = useTheme()
  const [underlying, setUnderlying] = useState<string>('NIFTY')
  const [selectedStrikes, setSelectedStrikes] = useState<number[]>([])
  const [expiry, setExpiry] = useState<string>('')
  const [availableExpiries, setAvailableExpiries] = useState<string[]>([])
  const [availableStrikes, setAvailableStrikes] = useState<number[]>([])
  const [strikeDialogOpen, setStrikeDialogOpen] = useState<boolean>(false)
  const [liveMode, setLiveMode] = useState<boolean>(false)
  const [interval, setInterval] = useState<string>('FIVE_MINUTE')
  const [date, setDate] = useState<string>(new Date().toISOString().split('T')[0])
  const [data, setData] = useState<any[]>([])
  const [loading, setLoading] = useState<boolean>(false)
  const [loadingExpiries, setLoadingExpiries] = useState<boolean>(false)
  const [loadingStrikes, setLoadingStrikes] = useState<boolean>(false)
  const [error, setError] = useState<string>('')

  const intervalOptions = [
    { value: 'ONE_MINUTE', label: '1m' },
    { value: 'THREE_MINUTE', label: '3m' },
    { value: 'FIVE_MINUTE', label: '5m' },
    { value: 'FIFTEEN_MINUTE', label: '15m' },
    { value: 'ONE_HOUR', label: '1h' },
  ]

  useEffect(() => {
    const fetchExpiries = async () => {
      if (!underlying) return
      setLoadingExpiries(true)
      try {
        const response = await instrumentsApi.getAvailableExpiries(underlying)
        setAvailableExpiries(response.data)
        if (response.data.length > 0 && !expiry) {
          setExpiry(response.data[0])
        }
      } catch (err) {
        console.error('Failed to fetch expiries:', err)
      } finally {
        setLoadingExpiries(false)
      }
    }

    fetchExpiries()
  }, [underlying])

  useEffect(() => {
    const fetchStrikes = async () => {
      if (!underlying || !expiry) return
      setLoadingStrikes(true)
      try {
        const response = await instrumentsApi.getAvailableStrikes(underlying, expiry)
        setAvailableStrikes(response.data)
        if (response.data.length > 0 && selectedStrikes.length === 0) {
          setSelectedStrikes([response.data[0]])
        }
      } catch (err) {
        console.error('Failed to fetch strikes:', err)
      } finally {
        setLoadingStrikes(false)
      }
    }

    fetchStrikes()
  }, [underlying, expiry])

  const columnDefs = [
    {
      headerName: 'Date',
      field: 'timestamp',
      width: 150,
      sortable: true,
      filter: true,
      headerClass: 'blue-header',
      cellStyle: { backgroundColor: 'rgba(59, 130, 246, 0.1)', fontWeight: 'bold' },
      valueFormatter: (params: { value: string }) => {
        if (!params.value) return '-'
        return new Date(params.value).toLocaleDateString('en-IN', {
          day: '2-digit',
          month: 'short',
          year: 'numeric',
          timeZone: 'Asia/Kolkata'
        })
      }
    },
    {
      headerName: 'Time',
      field: 'timestamp',
      width: 120,
      sortable: true,
      filter: true,
      headerClass: 'blue-header',
      cellStyle: { backgroundColor: 'rgba(59, 130, 246, 0.1)', fontWeight: 'bold' },
      valueFormatter: (params: { value: string }) => {
        if (!params.value) return '-'
        return new Date(params.value).toLocaleTimeString('en-IN', {
          hour: '2-digit',
          minute: '2-digit',
          hour12: true,
          timeZone: 'Asia/Kolkata'
        })
      }
    },
    {
      headerName: 'Put OI',
      headerClass: 'blue-header center-header',
      children: [
        {
          headerName: 'Total',
          field: 'put_oi',
          width: 150,
          sortable: true,
          filter: true,
          headerClass: 'blue-header',
          valueFormatter: (params: { value: number }) => {
            if (params.value === null || params.value === undefined) return '-'
            return new Intl.NumberFormat('en-IN').format(params.value)
          },
          cellStyle: (params: any) => {
            const change = params.data?.put_oi_change
            if (change > 0) {
              return { backgroundColor: 'rgba(16, 185, 129, 0.2)', color: '#10b981' }
            } else if (change < 0) {
              return { backgroundColor: 'rgba(239, 68, 68, 0.2)', color: '#ef4444' }
            }
            return { color: theme.palette.text.primary }
          }
        },
        {
          headerName: 'Change',
          field: 'put_oi_change',
          width: 150,
          sortable: true,
          filter: true,
          headerClass: 'blue-header',
          valueFormatter: (params: { value: number }) => {
            if (params.value === null || params.value === undefined) return '-'
            return new Intl.NumberFormat('en-IN').format(params.value)
          },
          cellStyle: (params: any) => ({
            color: params.value > 0 ? '#10b981' : params.value < 0 ? '#ef4444' : theme.palette.text.primary,
            fontWeight: 'bold'
          })
        },
      ],

    },
    {
      headerName: 'Call OI',
      headerClass: 'blue-header center-header',
      children: [
        {
          headerName: 'Total',
          field: 'call_oi',
          width: 150,
          sortable: true,
          filter: true,
          headerClass: 'blue-header',
          valueFormatter: (params: { value: number }) => {
            if (params.value === null || params.value === undefined) return '-'
            return new Intl.NumberFormat('en-IN').format(params.value)
          },
          cellStyle: (params: any) => {
            const change = params.data?.call_oi_change
            if (change > 0) {
              return { backgroundColor: 'rgba(16, 185, 129, 0.2)', color: '#10b981' }
            } else if (change < 0) {
              return { backgroundColor: 'rgba(239, 68, 68, 0.2)', color: '#ef4444' }
            }
            return { color: theme.palette.text.primary }
          }
        },
        {
          headerName: 'Change',
          field: 'call_oi_change',
          width: 150,
          sortable: true,
          filter: true,
          headerClass: 'blue-header',
          valueFormatter: (params: { value: number }) => {
            if (params.value === null || params.value === undefined) return '-'
            return new Intl.NumberFormat('en-IN').format(params.value)
          },
          cellStyle: (params: any) => ({
            color: params.value > 0 ? '#10b981' : params.value < 0 ? '#ef4444' : theme.palette.text.primary,
            fontWeight: 'bold'
          })
        },
      ],

    },
    {
      headerName: 'PCR',
      headerClass: 'blue-header',
      children: [
        {
          headerName: 'Total',
          field: 'put_call_ratio',
          width: 150,
          sortable: true,
          filter: true,
          headerClass: 'blue-header',
          valueFormatter: (params: { value: number }) => {
            if (params.value === null || params.value === undefined) return '-'
            return new Intl.NumberFormat('en-IN').format(params.value)
          },
          cellStyle: (params: any) => {
            const change = params.data?.call_oi_change
            if (change > 0) {
              return { backgroundColor: 'rgba(16, 185, 129, 0.2)', color: '#10b981' }
            } else if (change < 0) {
              return { backgroundColor: 'rgba(239, 68, 68, 0.2)', color: '#ef4444' }
            }
            return { color: theme.palette.text.primary }
          }
        },
        {
          headerName: 'Change',
          field: 'put_call_ratio_change',
          width: 150,
          sortable: true,
          filter: true,
          headerClass: 'blue-header',
          valueFormatter: (params: { value: number }) => {
            if (params.value === null || params.value === undefined) return '-'
            return new Intl.NumberFormat('en-IN').format(params.value)
          },
          cellStyle: (params: any) => ({
            color: params.value > 0 ? '#10b981' : params.value < 0 ? '#ef4444' : theme.palette.text.primary,
            fontWeight: 'bold'
          })
        },
      ]
    },
    {
      headerName: 'PE - CE OI',
      headerClass: 'blue-header',
      children: [
        {
          headerName: 'Total',
          field: 'put_call_difference',
          width: 150,
          sortable: true,
          filter: true,
          headerClass: 'blue-header',
          valueFormatter: (params: { value: number }) => {
            if (params.value === null || params.value === undefined) return '-'
            return new Intl.NumberFormat('en-IN').format(params.value)
          },
          cellStyle: (params: any) => {
            const change = params.data?.put_call_diff_change
            if (change > 0) {
              return { backgroundColor: 'rgba(16, 185, 129, 0.2)', color: '#10b981' }
            } else if (change < 0) {
              return { backgroundColor: 'rgba(239, 68, 68, 0.2)', color: '#ef4444' }
            }
            return { color: theme.palette.text.primary }
          }
        },
        {
          headerName: 'Change',
          field: 'put_call_diff_change',
          width: 150,
          sortable: true,
          filter: true,
          headerClass: 'blue-header',
          valueFormatter: (params: { value: number }) => {
            if (params.value === null || params.value === undefined) return '-'
            return new Intl.NumberFormat('en-IN').format(params.value)
          },
          cellStyle: (params: any) => ({
            color: params.value > 0 ? '#10b981' : params.value < 0 ? '#ef4444' : theme.palette.text.primary,
            fontWeight: 'bold'
          })
        },
      ],
    },
  ]

  const handleFetch = useCallback(async () => {
    setLoading(true)
    setError('')
    try {
      if (selectedStrikes.length === 0) {
        setError('Please select at least one strike.')
        setLoading(false)
        return
      }
      const response = await oiMonitorApi.getOIData(
        underlying,
        selectedStrikes,
        expiry,
        interval,
        date
      )
      setData(response.data)
    } catch (err) {
      setError('Failed to fetch OI data. Please check your parameters.')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }, [underlying, selectedStrikes, expiry, interval, date])

  useEffect(() => {
    if (liveMode && selectedStrikes.length > 0 && expiry) {
      const intervalId = window.setInterval(() => {
        handleFetch()
      }, 60000) // Fetch every minute

      return () => window.clearInterval(intervalId)
    }
  }, [liveMode, selectedStrikes, expiry, interval, date, handleFetch])

  const handleStrikeClick = (strikeValue: number, event: React.MouseEvent) => {
    if (event.shiftKey && selectedStrikes.length > 0) {
      const lastSelected = selectedStrikes[selectedStrikes.length - 1]
      const startIndex = availableStrikes.indexOf(lastSelected)
      const endIndex = availableStrikes.indexOf(strikeValue)
      if (startIndex !== -1 && endIndex !== -1) {
        const range = availableStrikes.slice(
          Math.min(startIndex, endIndex),
          Math.max(startIndex, endIndex) + 1
        )
        setSelectedStrikes(range)
      }
    } else {
      setSelectedStrikes(prev =>
        prev.includes(strikeValue)
          ? prev.filter(s => s !== strikeValue)
          : [...prev, strikeValue]
      )
    }
  }

  return (
    <Box sx={{ width: '100%' }}>
      <style>{`
        .blue-header {
          background-color: rgba(59, 130, 246, 0.2) !important;
          color: ${theme.palette.text.primary} !important;
          font-weight: bold !important;
        }
        .center-header {
          text-align: center !important;
        }
      `}</style>
      <Typography variant="h4" fontWeight="bold" sx={{ mb: 3 }}>
        OI Monitor
      </Typography>

      <Typography variant="body1" color="text.secondary" sx={{ mb: 4 }}>
        Monitor Open Interest data for options to analyze market sentiment.
      </Typography>

      <Paper sx={{ p: 3, mb: 4, bgcolor: 'background.paper' }}>
        <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap', alignItems: 'flex-end' }}>
          <FormControl sx={{ minWidth: 150 }}>
            <InputLabel>Underlying</InputLabel>
            <Select
              value={underlying}
              label="Underlying"
              onChange={(e) => setUnderlying(e.target.value)}
            >
              <MenuItem value="NIFTY">NIFTY</MenuItem>
              <MenuItem value="BANKNIFTY">BANKNIFTY</MenuItem>
            </Select>
          </FormControl>

          <FormControl sx={{ minWidth: 150 }}>
            <InputLabel>Expiry</InputLabel>
            <Select
              value={expiry}
              label="Expiry"
              onChange={(e) => setExpiry(e.target.value)}
              disabled={loadingExpiries || availableExpiries.length === 0}
            >
              {loadingExpiries ? (
                <MenuItem disabled>Loading...</MenuItem>
              ) : availableExpiries.length === 0 ? (
                <MenuItem disabled>No expiries available</MenuItem>
              ) : (
                availableExpiries.map((exp) => (
                  <MenuItem key={exp} value={exp}>
                    {exp}
                  </MenuItem>
                ))
              )}
            </Select>
          </FormControl>

          <Box sx={{ minWidth: 200 }}>
            <TextField
              label="Strikes"
              value={selectedStrikes.length > 0 ? `${selectedStrikes.length} selected` : ''}
              onClick={() => setStrikeDialogOpen(true)}
              disabled={loadingStrikes || availableStrikes.length === 0}
              InputProps={{
                readOnly: true,
                endAdornment: (
                  <InputAdornment position="end">
                    {selectedStrikes.length > 0 && (
                      <IconButton
                        onClick={(e) => {
                          e.stopPropagation()
                          setSelectedStrikes([])
                        }}
                        edge="end"
                        size="small"
                      >
                        <Clear fontSize="small" />
                      </IconButton>
                    )}
                  </InputAdornment>
                )
              }}
              placeholder="Select strikes"
              fullWidth
            />
            <Dialog
              open={strikeDialogOpen}
              onClose={() => setStrikeDialogOpen(false)}
              maxWidth="md"
              fullWidth
            >
              <DialogTitle>Select Strikes</DialogTitle>
              <DialogContent>
                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, my: 2 }}>
                  {loadingStrikes ? (
                    <CircularProgress />
                  ) : availableStrikes.length === 0 ? (
                    <Typography>No strikes available</Typography>
                  ) : (
                    availableStrikes.map((str) => (
                      <Chip
                        key={str}
                        label={str}
                        onClick={(e) => handleStrikeClick(str, e)}
                        color={selectedStrikes.includes(str) ? 'primary' : 'default'}
                        variant={selectedStrikes.includes(str) ? 'filled' : 'outlined'}
                        sx={{ cursor: 'pointer' }}
                      />
                    ))
                  )}
                </Box>
                {selectedStrikes.length > 0 && (
                  <Typography variant="body2" color="text.secondary">
                    Selected: {[...selectedStrikes].sort((a, b) => a - b).join(', ')}
                  </Typography>
                )}
              </DialogContent>
              <DialogActions>
                <Button onClick={() => setSelectedStrikes([])}>Clear All</Button>
                <Button onClick={() => setSelectedStrikes(availableStrikes)}>Select All</Button>
                <Button onClick={() => setStrikeDialogOpen(false)} variant="contained">
                  Done
                </Button>
              </DialogActions>
            </Dialog>
          </Box>

          <FormControl sx={{ minWidth: 120 }}>
            <InputLabel>Interval</InputLabel>
            <Select
              value={interval}
              label="Interval"
              onChange={(e) => setInterval(e.target.value)}
            >
              {intervalOptions.map((option) => (
                <MenuItem key={option.value} value={option.value}>
                  {option.label}
                </MenuItem>
              ))}
            </Select>
          </FormControl>

          <FormControl sx={{ minWidth: 180 }}>
            <TextField
              label="Date"
              type="date"
              value={date}
              onChange={(e) => setDate(e.target.value)}
              InputLabelProps={{
                shrink: true,
              }}
            />
          </FormControl>

          <Button
            variant="contained"
            onClick={handleFetch}
            disabled={loading}
            sx={{ minWidth: 120 }}
          >
            {loading ? <CircularProgress size={24} /> : 'Fetch Data'}
          </Button>

          <FormControlLabel
            control={
              <Switch
                checked={liveMode}
                onChange={(e) => setLiveMode(e.target.checked)}
                color="primary"
              />
            }
            label="Live Mode"
          />
        </Box>

        {error && (
          <Typography color="error" sx={{ mt: 2 }}>
            {error}
          </Typography>
        )}
      </Paper>

      {data.length > 0 && (
        <Paper sx={{ p: 2, bgcolor: 'background.paper' }}>
          <Box sx={{ height: 500, width: '100%' }}>
            <div
              className="ag-theme-quartz"
              style={{
                height: '100%',
                width: '100%',
                '--ag-background-color': theme.palette.background.default,
                '--ag-foreground-color': theme.palette.text.primary,
                '--ag-header-background-color': theme.palette.background.paper,
                '--ag-header-foreground-color': theme.palette.text.primary,
                '--ag-odd-row-background-color': theme.palette.background.default,
                '--ag-row-hover-color': theme.palette.action.hover,
                '--ag-selected-row-background-color': theme.palette.primary.main,
                '--ag-range-selection-background-color': theme.palette.primary.main + '33',
                '--ag-border-color': theme.palette.divider,
                '--ag-cell-horizontal-border': theme.palette.divider,
                '--ag-header-column-resize-handle-color': theme.palette.primary.main,
              } as React.CSSProperties}
            >
              <AgGridReact
                rowData={data}
                columnDefs={columnDefs}
                defaultColDef={{
                  resizable: true,
                  sortable: true,
                  filter: true,
                }}
                domLayout="autoHeight"
              />
            </div>
          </Box>
        </Paper>
      )}
    </Box>
  )
}

export default OIMonitorPage

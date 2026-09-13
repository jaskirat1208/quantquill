import React, { useState } from 'react'
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
  CircularProgress
} from '@mui/material'
import { useTheme } from '@mui/material/styles'
import { AgGridReact } from 'ag-grid-react'
import 'ag-grid-community/styles/ag-grid.css'
import 'ag-grid-community/styles/ag-theme-quartz.css'
import { oiMonitorApi } from '../services/api'

const OIMonitorPage: React.FC = () => {
  const theme = useTheme()
  const [underlying, setUnderlying] = useState<string>('NIFTY')
  const [strike, setStrike] = useState<string>('23400')
  const [expiry, setExpiry] = useState<string>('15SEP26')
  const [interval, setInterval] = useState<string>('FIVE_MINUTE')
  const [date, setDate] = useState<string>(new Date().toISOString().split('T')[0])
  const [data, setData] = useState<any[]>([])
  const [loading, setLoading] = useState<boolean>(false)
  const [error, setError] = useState<string>('')

  const intervalOptions = [
    { value: 'ONE_MINUTE', label: '1m' },
    { value: 'THREE_MINUTE', label: '3m' },
    { value: 'FIVE_MINUTE', label: '5m' },
    { value: 'FIFTEEN_MINUTE', label: '15m' },
    { value: 'ONE_HOUR', label: '1h' },
  ]

  const columnDefs = [
    {
      headerName: 'Date',
      field: 'timestamp',
      width: 150,
      sortable: true,
      filter: true,
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
      children: [
        {
          headerName: 'Total',
          field: 'put_oi',
          width: 150,
          sortable: true,
          filter: true,
          cellStyle: { color: '#ef4444' }
        },
        {
          headerName: 'Change',
          field: 'put_oi_change',
          width: 150,
          sortable: true,
          filter: true,
          cellStyle: (params: any) => ({
            color: params.value > 0 ? '#10b981' : params.value < 0 ? '#ef4444' : '#ffffff'
          })
        },
      ],
      headerClass: 'center-header' 

    },
    {
      headerName: 'Call OI',
      children: [
        {
          headerName: 'Total',
          field: 'call_oi',
          width: 150,
          sortable: true,
          filter: true,
          cellStyle: { color: '#10b981' }
        },
        {
          headerName: 'Change',
          field: 'call_oi_change',
          width: 150,
          sortable: true,
          filter: true,
          cellStyle: (params: any) => ({
            color: params.value > 0 ? '#10b981' : params.value < 0 ? '#ef4444' : '#ffffff'
          })
        },
      ],
      headerClass: 'center-header' 

    },
    {
      headerName: 'PCR',
      children: [
        {
          headerName: 'Total',
          field: 'put_call_ratio',
          width: 150,
          sortable: true,
          filter: true,
          valueFormatter: (params: { value: number }) => {
            if (params.value === null || params.value === undefined) return '-'
            return params.value.toFixed(2)
          }
        },
      ]
    },
  ]

  const handleFetch = async () => {
    setLoading(true)
    setError('')
    try {
      const response = await oiMonitorApi.getOIData(
        underlying,
        parseInt(strike),
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
  }

  return (
    <Box sx={{ width: '100%' }}>
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

          <FormControl sx={{ minWidth: 120 }}>
            <TextField
              label="Strike"
              value={strike}
              onChange={(e) => setStrike(e.target.value)}
              type="number"
            />
          </FormControl>

          <FormControl sx={{ minWidth: 150 }}>
            <TextField
              label="Expiry (DDMMMYY)"
              value={expiry}
              onChange={(e) => setExpiry(e.target.value)}
              placeholder="15SEP26"
            />
          </FormControl>

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

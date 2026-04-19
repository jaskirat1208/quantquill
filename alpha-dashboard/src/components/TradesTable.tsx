import React, { useMemo } from 'react'
import { Paper, Typography, Button, Box } from '@mui/material'
import { TableChart, Download } from '@mui/icons-material'
import { AgGridReact } from 'ag-grid-react'
import 'ag-grid-community/styles/ag-grid.css'
import 'ag-grid-community/styles/ag-theme-alpine.css'
import type { TradesTableProps, Trade } from '../types'

const TradesTable: React.FC<TradesTableProps> = ({ trades }) => {
  const columnDefs = useMemo(() => [
    {
      field: 'time',
      headerName: 'Time',
      sortable: true,
      filter: true,
      valueFormatter: (params: { value: string }) => {
        if (!params.value) return '-'
        return new Date(params.value).toLocaleString()
      }
    },
    {
      field: 'action',
      headerName: 'Action',
      sortable: true,
      filter: true,
      cellRenderer: (params: { value: string }) => {
        const isBuy = params.value === 'BUY'
        return (
          <span style={{ 
            color: isBuy ? '#10b981' : '#ef4444', 
            fontWeight: 600 
          }}>
            {params.value}
          </span>
        )
      }
    },
    {
      field: 'price',
      headerName: 'Price',
      sortable: true,
      filter: 'agNumberColumnFilter',
      valueFormatter: (params: { value: number }) => {
        if (params.value == null) return '-'
        return `$${params.value.toFixed(2)}`
      }
    },
    {
      field: 'quantity',
      headerName: 'Quantity',
      sortable: true,
      filter: 'agNumberColumnFilter',
      valueFormatter: (params: { value: number }) => {
        if (params.value == null) return '-'
        return params.value.toFixed(4)
      }
    },
    {
      headerName: 'Total Value',
      sortable: true,
      filter: 'agNumberColumnFilter',
      valueGetter: (params: { data: Trade }) => {
        const price = params.data?.price || 0
        const quantity = params.data?.quantity || 0
        return price * quantity
      },
      valueFormatter: (params: { value: number }) => {
        if (params.value == null) return '-'
        return `$${params.value.toFixed(2)}`
      }
    }
  ], [])

  const defaultColDef = useMemo(() => ({
    flex: 1,
    minWidth: 100,
    resizable: true,
  }), [])

  const exportToCSV = () => {
    if (!trades || trades.length === 0) return
    
    const headers = ['Time', 'Action', 'Price', 'Quantity', 'Total Value']
    const rows = trades.map(trade => [
      new Date(trade.time).toLocaleString(),
      trade.action,
      trade.price.toFixed(2),
      trade.quantity.toFixed(4),
      (trade.price * trade.quantity).toFixed(2)
    ])
    
    const csvContent = [
      headers.join(','),
      ...rows.map(row => row.join(','))
    ].join('\n')
    
    const blob = new Blob([csvContent], { type: 'text/csv' })
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `trades_${new Date().toISOString().split('T')[0]}.csv`
    a.click()
    window.URL.revokeObjectURL(url)
  }

  const gridOptions = {
    pagination: true,
    paginationPageSize: 10,
    paginationPageSizeSelector: [10, 25, 50, 100],
    domLayout: 'autoHeight' as const
  }

  return (
    <Paper elevation={2} sx={{ p: 3, borderRadius: 2 }}>
      <Box display="flex" alignItems="center" justifyContent="space-between" mb={3}>
        <Typography variant="h6" fontWeight="bold" display="flex" alignItems="center" gap={1}>
          <TableChart color="primary" />
          Trade History
        </Typography>
        
        {trades && trades.length > 0 && (
          <Button
            variant="outlined"
            size="small"
            startIcon={<Download />}
            onClick={exportToCSV}
          >
            Export CSV
          </Button>
        )}
      </Box>

      {trades && trades.length > 0 ? (
        <div 
          className="ag-theme-alpine-dark"
          style={{ 
            height: 'auto',
            '--ag-background-color': '#1e293b',
            '--ag-foreground-color': '#fff',
            '--ag-header-background-color': '#374151',
            '--ag-header-foreground-color': '#fff',
            '--ag-row-hover-color': '#374151',
            '--ag-border-color': '#4b5563',
          } as React.CSSProperties}
        >
          <AgGridReact
            rowData={trades}
            columnDefs={columnDefs}
            defaultColDef={defaultColDef}
            gridOptions={gridOptions}
            animateRows={true}
          />
        </div>
      ) : (
        <Box display="flex" flexDirection="column" alignItems="center" justifyContent="center" py={6}>
          <TableChart sx={{ fontSize: 48, color: 'text.disabled', mb: 2 }} />
          <Typography variant="body1" color="text.secondary">
            No trades executed yet
          </Typography>
          <Typography variant="body2" color="text.disabled" sx={{ mt: 1 }}>
            Run a strategy to see trade history
          </Typography>
        </Box>
      )}
    </Paper>
  )
}

export default TradesTable

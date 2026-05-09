import React from 'react'
import { Paper, Typography, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Box } from '@mui/material'
import { Assessment } from '@mui/icons-material'
import type { StrategyResult } from '../types'

interface MetricsTableProps {
  strategyResults: StrategyResult | null
}

const MetricsTable: React.FC<MetricsTableProps> = ({ strategyResults }) => {
  if (!strategyResults) {
    return (
      <Paper elevation={2} sx={{ p: 3, borderRadius: 2 }}>
        <Box display="flex" alignItems="center" justifyContent="center" py={6}>
          <Assessment sx={{ fontSize: 48, color: 'text.disabled', mb: 2 }} />
          <Typography variant="body1" color="text.secondary">
            No metrics available yet
          </Typography>
          <Typography variant="body2" color="text.disabled" sx={{ mt: 1 }}>
            Execute a strategy to see performance metrics
          </Typography>
        </Box>
      </Paper>
    )
  }

  const metricsData = [
    { label: 'Strategy Name', value: strategyResults.strategy_name, format: 'text' },
    { label: 'Symbol', value: strategyResults.symbol, format: 'text' },
    { label: 'Total Trades', value: strategyResults.trades?.length || 0, format: 'number' },
    { label: 'Profit/Loss', value: strategyResults.profit_loss, format: 'currency' },
    { label: 'Win Rate', value: (strategyResults as any).win_rate, format: 'percentage' },
    { label: 'Total Return', value: (strategyResults as any).total_return, format: 'percentage' },
    { label: 'Max Drawdown', value: (strategyResults as any).max_drawdown, format: 'percentage' },
    { label: 'Volatility', value: (strategyResults as any).volatility, format: 'percentage' },
    { label: 'Sharpe Ratio', value: (strategyResults as any).sharpe_ratio, format: 'decimal' },
    { label: 'Executed At', value: strategyResults.executed_at, format: 'datetime' },
    { label: 'Success', value: strategyResults.success, format: 'boolean' },
  ]

  const formatValue = (value: any, format: string) => {
    if (value === undefined || value === null) {
      return '-'
    }
    
    switch (format) {
      case 'currency':
        return `₹${value.toFixed(2)}`
      case 'percentage':
        return `${value.toFixed(2)}%`
      case 'decimal':
        return value.toFixed(3)
      case 'datetime':
        return new Date(value).toLocaleString()
      case 'boolean':
        return value ? '✅ Yes' : '❌ No'
      case 'number':
        return value.toLocaleString()
      default:
        return value
    }
  }

  return (
    <Paper elevation={2} sx={{ p: 3, borderRadius: 2 }}>
      <Typography variant="h6" fontWeight="bold" gutterBottom display="flex" alignItems="center" gap={1}>
        <Assessment color="primary" />
        Performance Metrics
      </Typography>

      <TableContainer>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell sx={{ fontWeight: 'bold', color: 'primary.main' }}>Metric</TableCell>
              <TableCell align="right" sx={{ fontWeight: 'bold', color: 'primary.main' }}>Value</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {metricsData.map((metric, index) => (
              <TableRow key={index} sx={{ '&:hover': { bgcolor: 'action.hover' } }}>
                <TableCell sx={{ fontWeight: 500 }}>
                  {metric.label}
                </TableCell>
                <TableCell align="right" sx={{ fontFamily: 'monospace' }}>
                  {formatValue(metric.value, metric.format)}
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Paper>
  )
}

export default MetricsTable

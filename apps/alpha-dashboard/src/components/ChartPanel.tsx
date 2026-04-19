import React from 'react'
import { Paper, Typography, Grid, Box } from '@mui/material'
import { TrendingUp } from '@mui/icons-material'
import Highcharts from 'highcharts'
import HighchartsReact from 'highcharts-react-official'
import type { ChartPanelProps } from '../types'

const ChartPanel: React.FC<ChartPanelProps> = ({ strategyResults }) => {
  if (!strategyResults) {
    return (
      <Paper elevation={2} sx={{ p: 3, borderRadius: 2, height: '100%', minHeight: 400 }}>
        <Box display="flex" flexDirection="column" alignItems="center" justifyContent="center" height="100%">
          <TrendingUp sx={{ fontSize: 64, color: 'text.disabled', mb: 2 }} />
          <Typography variant="h6" color="text.secondary">
            No Data Available
          </Typography>
          <Typography variant="body2" color="text.disabled" sx={{ mt: 1 }}>
            Execute a strategy to see performance charts
          </Typography>
        </Box>
      </Paper>
    )
  }

  const { trades, strategy_name, profit_loss } = strategyResults

  const tradeData = trades?.map((trade) => trade.price) || []
  
  const pnlData = trades?.map((_, index) => {
    const runningTrades = trades.slice(0, index + 1)
    const runningPnL = runningTrades.reduce((sum, trade) => {
      return sum + (trade.action === 'SELL' ? trade.price * trade.quantity : -trade.price * trade.quantity)
    }, 0)
    return [index, runningPnL]
  }) || []

  const chartOptions: Highcharts.Options = {
    chart: {
      type: 'line',
      backgroundColor: 'transparent',
      style: {
        fontFamily: 'Inter, sans-serif'
      }
    },
    title: {
      text: `${strategy_name.replace('_', ' ').toUpperCase()} Performance`,
      style: {
        color: '#fff',
        fontSize: '16px',
        fontWeight: 'bold'
      }
    },
    xAxis: {
      title: { text: 'Trade Number', style: { color: '#9ca3af' } },
      labels: { style: { color: '#9ca3af' } },
      lineColor: '#4b5563',
      tickColor: '#4b5563'
    },
    yAxis: {
      title: { text: 'Price ($)', style: { color: '#9ca3af' } },
      labels: { style: { color: '#9ca3af' } },
      lineColor: '#4b5563',
      tickColor: '#4b5563',
      gridLineColor: '#374151'
    },
    legend: {
      itemStyle: { color: '#9ca3af' },
      itemHoverStyle: { color: '#fff' }
    },
    series: [
      {
        name: 'Trade Price',
        data: tradeData,
        color: '#0ea5e9',
        marker: {
          enabled: true,
          radius: 4
        },
        type: 'line'
      },
      {
        name: 'Running P&L',
        data: pnlData,
        color: (profit_loss || 0) >= 0 ? '#10b981' : '#ef4444',
        dashStyle: 'Dash',
        type: 'line'
      }
    ],
    plotOptions: {
      line: {
        lineWidth: 2
      }
    },
    tooltip: {
      backgroundColor: '#1e293b',
      borderColor: '#4b5563',
      style: { color: '#fff' }
    }
  }

  const pnlChartOptions: Highcharts.Options = {
    chart: {
      type: 'column',
      backgroundColor: 'transparent'
    },
    title: {
      text: 'Profit & Loss Distribution',
      style: { color: '#fff', fontSize: '14px' }
    },
    xAxis: {
      categories: trades?.map((_, i) => `Trade ${i + 1}`) || [],
      labels: { style: { color: '#9ca3af' } }
    },
    yAxis: {
      title: { text: 'P&L ($)', style: { color: '#9ca3af' } },
      labels: { style: { color: '#9ca3af' } },
      gridLineColor: '#374151'
    },
    plotOptions: {
      column: {
        colorByPoint: true
      }
    },
    series: [{
      name: 'P&L',
      data: pnlData.map(d => d[1]),
      showInLegend: false,
      type: 'column'
    }],
    tooltip: {
      backgroundColor: '#1e293b',
      borderColor: '#4b5563',
      style: { color: '#fff' }
    }
  }

  return (
    <Paper elevation={2} sx={{ p: 3, borderRadius: 2, height: '100%' }}>
      <Typography variant="h6" fontWeight="bold" gutterBottom display="flex" alignItems="center" gap={1}>
        <TrendingUp color="primary" />
        Strategy Performance
      </Typography>

      <Grid container spacing={2} sx={{ mb: 3 }}>
        <Grid item xs={4}>
          <Paper sx={{ p: 2, textAlign: 'center', bgcolor: 'background.default' }}>
            <Typography variant="body2" color="text.secondary">Total Trades</Typography>
            <Typography variant="h5" fontWeight="bold">{trades?.length || 0}</Typography>
          </Paper>
        </Grid>
        <Grid item xs={4}>
          <Paper sx={{ p: 2, textAlign: 'center', bgcolor: 'background.default' }}>
            <Typography variant="body2" color="text.secondary">Net P&L</Typography>
            <Typography variant="h5" fontWeight="bold" color={(profit_loss || 0) >= 0 ? 'success.main' : 'error.main'}>
              ${profit_loss?.toFixed(2) || '0.00'}
            </Typography>
          </Paper>
        </Grid>
        <Grid item xs={4}>
          <Paper sx={{ p: 2, textAlign: 'center', bgcolor: 'background.default' }}>
            <Typography variant="body2" color="text.secondary">Avg per Trade</Typography>
            <Typography variant="h5" fontWeight="bold">
              ${trades?.length ? ((profit_loss || 0) / trades.length).toFixed(2) : '0.00'}
            </Typography>
          </Paper>
        </Grid>
      </Grid>

      <HighchartsReact highcharts={Highcharts} options={chartOptions} />
      <Box sx={{ mt: 2 }}>
        <HighchartsReact highcharts={Highcharts} options={pnlChartOptions} />
      </Box>
    </Paper>
  )
}

export default ChartPanel

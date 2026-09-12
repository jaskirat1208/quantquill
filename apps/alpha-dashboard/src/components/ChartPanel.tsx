import React from 'react'
import { Paper, Typography, Grid, Box } from '@mui/material'
import { TrendingUp } from '@mui/icons-material'
import Highcharts from 'highcharts'
import HighchartsReact from 'highcharts-react-official'
import type { ChartPanelProps, PortfolioSnapshot, MarketSnapshot } from '../types'
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

  const { trades, strategy_name, market_snapshots, profit_loss, portfolio_snapshots, indicators } = strategyResults
  
  // Date formatter for IST timezone
  const dateFormatter = (date: Date): string => {
    const istOffset = 5.5 * 60 * 60 * 1000; // 5.5 hours in milliseconds
    const istDate = new Date(date.getTime() + istOffset + (date.getTimezoneOffset() * 60 * 1000));
    
    const year = istDate.getFullYear();
    const month = (istDate.getMonth() + 1).toString().padStart(2, '0');
    const day = istDate.getDate().toString().padStart(2, '0');
    const hours = istDate.getHours().toString().padStart(2, '0');
    const minutes = istDate.getMinutes().toString().padStart(2, '0');
    
    const currentYear = new Date().getFullYear();
    const showYear = year !== currentYear || (month === '01' && day === '01');
    
    if (showYear) {
      return `${year}/${month}/${day}<br/>${hours}:${minutes}`;
    } else {
      return `${month}/${day}<br/>${hours}:${minutes}`;
    }
  }
  
  // Use portfolio snapshots from backend for P&L data
  const pnlDataWithTime = portfolio_snapshots?.map((snapshot: PortfolioSnapshot) => [
    new Date(snapshot.timestamp).getTime(),
    snapshot.pnl
  ]) || []

  // Prepare indicator data for chart
  const shortEwmaData = market_snapshots?.map((snapshot: MarketSnapshot) => [
    new Date(snapshot.timestamp).getTime(),
    snapshot.short_ewma
  ]) || []

  const longEwmaData = market_snapshots?.map((snapshot: MarketSnapshot) => [
    new Date(snapshot.timestamp).getTime(),
    snapshot.long_ewma
  ]) || []

  // For backward compatibility - trade number based P&L from backend data
  const pnlData = portfolio_snapshots?.map((snapshot: PortfolioSnapshot, index: number) => [
    index,
    snapshot.pnl
  ]) || []

  // Indicator values chart (replaces running P&L chart)
  const indicatorChartOptions: Highcharts.Options = {
    chart: {
      type: 'line',
      backgroundColor: 'transparent',
      style: {
        fontFamily: 'Inter, sans-serif'
      }
    },
    title: {
      text: `${strategy_name.replace('_', ' ').toUpperCase()} - Moving Averages`,
      style: {
        color: '#fff',
        fontSize: '16px',
        fontWeight: 'bold'
      }
    },
    xAxis: {
      type: 'datetime',
      title: { text: 'Date & Time', style: { color: '#9ca3af' } },
      labels: { 
        style: { color: '#9ca3af' },
        formatter: function() {
          return dateFormatter(new Date(this.value));
        },
        useHTML: true
      },
      lineColor: '#4b5563',
      tickColor: '#4b5563'
    },
    yAxis: {
      title: { text: 'Indicator Value', style: { color: '#9ca3af' } },
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
        name: 'Short EWMA',
        data: shortEwmaData,
        color: '#3b82f6',
        lineWidth: 2,
        marker: {
          enabled: false
        },
        type: 'line'
      },
      {
        name: 'Long EWMA',
        data: longEwmaData,
        color: '#f59e0b',
        lineWidth: 2,
        marker: {
          enabled: false
        },
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
      style: { color: '#fff' },
      pointFormatter: function() {
        const date = new Date((this as any).x);
        const istOffset = 5.5 * 60 * 60 * 1000;
        const istDate = new Date(date.getTime() + istOffset + (date.getTimezoneOffset() * 60 * 1000));
        
        const year = istDate.getFullYear();
        const month = (istDate.getMonth() + 1).toString().padStart(2, '0');
        const day = istDate.getDate().toString().padStart(2, '0');
        const hours = istDate.getHours().toString().padStart(2, '0');
        const minutes = istDate.getMinutes().toString().padStart(2, '0');
        
        return `<span style="color: ${(this as any).color}">●</span> ${this.series.name}: <b>${(this as any).y.toFixed(2)}</b><br/>
                <span style="color: #9ca3af">Time: ${year}-${month}-${day} ${hours}:${minutes} IST</span>`
      }
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
      title: { text: 'P&L (₹)', style: { color: '#9ca3af' } },
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
      data: pnlData.map((d: number[]) => d[1]),
      showInLegend: false,
      type: 'column'
    }],
    tooltip: {
      backgroundColor: '#1e293b',
      borderColor: '#4b5563',
      style: { color: '#fff' }
    }
  }

  // P&L vs Time Chart
  const pnlTimeChartOptions: Highcharts.Options = {
    chart: {
      type: 'line',
      backgroundColor: 'transparent'
    },
    title: {
      text: 'P&L Over Time',
      style: { color: '#fff', fontSize: '14px' }
    },
    xAxis: {
      type: 'datetime',
      title: { text: 'Date & Time', style: { color: '#9ca3af' } },
      labels: { 
        style: { color: '#9ca3af' },
        formatter: function() {
          return dateFormatter(new Date(this.value));
        },
        useHTML: true
      },
      lineColor: '#4b5563',
      tickColor: '#4b5563'
    },
    yAxis: {
      title: { text: 'Cumulative P&L (₹)', style: { color: '#9ca3af' } },
      labels: { style: { color: '#9ca3af' } },
      lineColor: '#4b5563',
      tickColor: '#4b5563',
      gridLineColor: '#374151'
    },
    legend: {
      itemStyle: { color: '#9ca3af' },
      itemHoverStyle: { color: '#fff' }
    },
    series: [{
      name: 'Cumulative P&L',
      data: pnlDataWithTime,
      color: (profit_loss || 0) >= 0 ? '#10b981' : '#ef4444',
      lineWidth: 3,
      marker: {
        enabled: true,
        radius: 4
      },
      type: 'line'
    }],
    plotOptions: {
      line: {
        lineWidth: 2
      }
    },
    tooltip: {
      backgroundColor: '#1e293b',
      borderColor: '#4b5563',
      style: { color: '#fff' },
      pointFormatter: function() {
        const date = new Date((this as any).x);
        // Convert to IST (UTC+5:30)
        const istOffset = 5.5 * 60 * 60 * 1000; // 5.5 hours in milliseconds
        const istDate = new Date(date.getTime() + istOffset + (date.getTimezoneOffset() * 60 * 1000));
        
        const year = istDate.getFullYear();
        const month = (istDate.getMonth() + 1).toString().padStart(2, '0');
        const day = istDate.getDate().toString().padStart(2, '0');
        const hours = istDate.getHours().toString().padStart(2, '0');
        const minutes = istDate.getMinutes().toString().padStart(2, '0');
        const seconds = istDate.getSeconds().toString().padStart(2, '0');
        
        return `<span style="color: ${(this as any).color}">●</span> ${this.series.name}: <b>₹${(this as any).y.toFixed(2)}</b><br/>
                <span style="color: #9ca3af">Time: ${year}-${month}-${day} ${hours}:${minutes}:${seconds} IST</span>`
      }
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
              ₹{profit_loss?.toFixed(2) || '0.00'}
            </Typography>
          </Paper>
        </Grid>
        <Grid item xs={4}>
          <Paper sx={{ p: 2, textAlign: 'center', bgcolor: 'background.default' }}>
            <Typography variant="body2" color="text.secondary">Current Trend</Typography>
            <Typography variant="h5" fontWeight="bold" color={indicators?.trend === 'UP' ? 'success.main' : indicators?.trend === 'DOWN' ? 'error.main' : 'warning.main'}>
              {indicators?.trend || 'N/A'}
            </Typography>
          </Paper>
        </Grid>
      </Grid>

      <HighchartsReact highcharts={Highcharts} options={indicatorChartOptions} />
      <Box sx={{ mt: 2 }}>
        <HighchartsReact highcharts={Highcharts} options={pnlChartOptions} />
      </Box>
      <Box sx={{ mt: 2 }}>
        <HighchartsReact highcharts={Highcharts} options={pnlTimeChartOptions} />
      </Box>
    </Paper>
  )
}

export default ChartPanel

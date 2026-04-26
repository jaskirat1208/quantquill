import React, { useState } from 'react'
import { 
  Box, 
  Typography, 
  Grid
} from '@mui/material'
import StrategyPanel from '../components/StrategyPanel'
import ChartPanel from '../components/ChartPanel'
import TradesTable from '../components/TradesTable'
import MetricsTable from '../components/MetricsTable'
import StatCard from '../components/StatCard'
import type { StrategyResult } from '../types'

const DashboardPage: React.FC = () => {
  const [strategyResults, setStrategyResults] = useState<StrategyResult | null>(null)

  const handleStrategyResults = (results: StrategyResult) => {
    setStrategyResults(results)
  }

  return (
    <Box sx={{ width: '100%' }}>
      <Typography variant="h4" fontWeight="bold" sx={{ mb: 3 }}>
        Dashboard
      </Typography>
      
      <Typography variant="body1" color="text.secondary" sx={{ mb: 4 }}>
        Execute and monitor trading strategies with real-time performance metrics.
      </Typography>

      {/* Stats Cards */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard 
            title="Active Strategies" 
            value="3" 
            color="#0ea5e9"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard 
            title="Total Trades" 
            value={strategyResults?.trades?.length || 0} 
            color="#10b981"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard 
            title="Profit/Loss" 
            value={strategyResults?.profit_loss ? `₹${strategyResults.profit_loss.toFixed(2)}` : '₹0.00'} 
            color={strategyResults?.profit_loss && strategyResults.profit_loss >= 0 ? '#10b981' : '#ef4444'}
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard 
            title="Position Size" 
            value="₹1,000" 
            color="#3b82f6"
          />
        </Grid>
      </Grid>

      {/* Main Content */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} lg={6}>
          <StrategyPanel onResults={handleStrategyResults} />
        </Grid>
        <Grid item xs={12} lg={6}>
          <ChartPanel strategyResults={strategyResults} />
        </Grid>
      </Grid>

      {/* Metrics Table */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12}>
          <MetricsTable strategyResults={strategyResults} />
        </Grid>
      </Grid>

      {/* Trades Table */}
      <TradesTable trades={strategyResults?.trades || []} />
    </Box>
  )
}

export default DashboardPage

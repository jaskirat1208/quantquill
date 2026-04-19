import React, { useState } from 'react'
import { 
  Box, 
  Typography, 
  Grid, 
  AppBar, 
  Toolbar,
  CssBaseline
} from '@mui/material'
import { ThemeProvider, createTheme } from '@mui/material/styles'
import Sidebar from './components/Sidebar'
import StrategyPanel from './components/StrategyPanel'
import ChartPanel from './components/ChartPanel'
import TradesTable from './components/TradesTable'
import StatCard from './components/StatCard'
import type { StrategyResult } from './types'

const darkTheme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#0ea5e9',
    },
    secondary: {
      main: '#10b981',
    },
    background: {
      default: '#0f172a',
      paper: '#1e293b',
    },
  },
})

function App() {
  const [activeTab, setActiveTab] = useState<string>('dashboard')
  const [strategyResults, setStrategyResults] = useState<StrategyResult | null>(null)

  const handleStrategyResults = (results: StrategyResult) => {
    setStrategyResults(results)
  }

  return (
    <ThemeProvider theme={darkTheme}>
      <CssBaseline />
      <Box sx={{ display: 'flex', height: '100vh', bgcolor: 'background.default' }}>
        <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />
        
        <Box component="main" sx={{ flexGrow: 1, overflow: 'auto', p: 3 }}>
          <AppBar position="static" elevation={0} sx={{ bgcolor: 'transparent', mb: 3 }}>
            <Toolbar sx={{ px: 0 }}>
              <Typography variant="h4" component="h1" fontWeight="bold" color="white">
                Alpha Dashboard
              </Typography>
            </Toolbar>
          </AppBar>

          <Typography variant="subtitle1" color="text.secondary" sx={{ mb: 4 }}>
            QuantQuill Strategy Execution Platform
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
                value={strategyResults?.profit_loss ? `$${strategyResults.profit_loss.toFixed(2)}` : '$0.00'} 
                color={strategyResults?.profit_loss && strategyResults.profit_loss >= 0 ? '#10b981' : '#ef4444'}
              />
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <StatCard 
                title="Position Size" 
                value="$1,000" 
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

          {/* Trades Table */}
          <TradesTable trades={strategyResults?.trades || []} />
        </Box>
      </Box>
    </ThemeProvider>
  )
}

export default App

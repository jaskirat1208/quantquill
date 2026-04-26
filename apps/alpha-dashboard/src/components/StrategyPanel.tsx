import React, { useState } from 'react'
import {
  Paper,
  Typography,
  TextField,
  Button,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Grid,
  Alert,
  CircularProgress
} from '@mui/material'
import { PlayArrow, CheckCircle } from '@mui/icons-material'
import { strategyApi } from '../services/api'
import type { StrategyPanelProps, MovingAverageParams, RSIParams, StrategyResult } from '../types'

const StrategyPanel: React.FC<StrategyPanelProps> = ({ onResults }) => {
  const [activeStrategy, setActiveStrategy] = useState<string>('moving_average')
  const [loading, setLoading] = useState<boolean>(false)
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState<boolean>(false)

  const [maParams, setMaParams] = useState<MovingAverageParams>({
    symbol: 'AAPL',
    short_window: 10,
    long_window: 30,
    position_size: 1000
  })

  const [rsiParams, setRsiParams] = useState<RSIParams>({
    symbol: 'AAPL',
    rsi_period: 14,
    oversold: 30,
    overbought: 70,
    position_size: 1000
  })

  const executeStrategy = async () => {
    setLoading(true)
    setError(null)
    setSuccess(false)

    try {
      let response
      if (activeStrategy === 'moving_average') {
        response = await strategyApi.executeMovingAverage(maParams)
      } else {
        response = await strategyApi.executeRSI(rsiParams)
      }

      onResults(response.data as StrategyResult)
      setSuccess(true)
      setTimeout(() => setSuccess(false), 3000)
    } catch (err: any) {
      setError(err.response?.data?.message || err.message || 'Failed to execute strategy')
    } finally {
      setLoading(false)
    }
  }

  return (
    <Paper elevation={2} sx={{ p: 3, borderRadius: 2, height: '100%' }}>
      <Typography variant="h6" fontWeight="bold" gutterBottom display="flex" alignItems="center" gap={1}>
        <PlayArrow color="primary" />
        Execute Strategy
      </Typography>

      <FormControl fullWidth sx={{ mb: 3 }}>
        <InputLabel>Select Strategy</InputLabel>
        <Select
          value={activeStrategy}
          label="Select Strategy"
          onChange={(e) => setActiveStrategy(e.target.value)}
        >
          <MenuItem value="moving_average">Moving Average Crossover</MenuItem>
          <MenuItem value="rsi">RSI Overbought/Oversold</MenuItem>
        </Select>
      </FormControl>

      {activeStrategy === 'moving_average' && (
        <Grid container spacing={2}>
          <Grid item xs={12}>
            <TextField
              fullWidth
              label="Symbol"
              value={maParams.symbol}
              onChange={(e) => setMaParams({...maParams, symbol: e.target.value.toUpperCase()})}
              placeholder="e.g., AAPL"
            />
          </Grid>
          <Grid item xs={6}>
            <TextField
              fullWidth
              label="Short Window"
              type="number"
              value={maParams.short_window}
              onChange={(e) => setMaParams({...maParams, short_window: parseInt(e.target.value)})}
              inputProps={{ min: 1, max: 100 }}
            />
          </Grid>
          <Grid item xs={6}>
            <TextField
              fullWidth
              label="Long Window"
              type="number"
              value={maParams.long_window}
              onChange={(e) => setMaParams({...maParams, long_window: parseInt(e.target.value)})}
              inputProps={{ min: 1, max: 200 }}
            />
          </Grid>
          <Grid item xs={12}>
            <TextField
              fullWidth
              label="Position Size (₹)"
              type="number"
              value={maParams.position_size}
              onChange={(e) => setMaParams({...maParams, position_size: parseFloat(e.target.value)})}
              inputProps={{ min: 1 }}
            />
          </Grid>
        </Grid>
      )}

      {activeStrategy === 'rsi' && (
        <Grid container spacing={2}>
          <Grid item xs={12}>
            <TextField
              fullWidth
              label="Symbol"
              value={rsiParams.symbol}
              onChange={(e) => setRsiParams({...rsiParams, symbol: e.target.value.toUpperCase()})}
              placeholder="e.g., AAPL"
            />
          </Grid>
          <Grid item xs={12}>
            <TextField
              fullWidth
              label="RSI Period"
              type="number"
              value={rsiParams.rsi_period}
              onChange={(e) => setRsiParams({...rsiParams, rsi_period: parseInt(e.target.value)})}
              inputProps={{ min: 1, max: 50 }}
            />
          </Grid>
          <Grid item xs={6}>
            <TextField
              fullWidth
              label="Oversold (0-50)"
              type="number"
              value={rsiParams.oversold}
              onChange={(e) => setRsiParams({...rsiParams, oversold: parseFloat(e.target.value)})}
              inputProps={{ min: 0, max: 50 }}
            />
          </Grid>
          <Grid item xs={6}>
            <TextField
              fullWidth
              label="Overbought (50-100)"
              type="number"
              value={rsiParams.overbought}
              onChange={(e) => setRsiParams({...rsiParams, overbought: parseFloat(e.target.value)})}
              inputProps={{ min: 50, max: 100 }}
            />
          </Grid>
          <Grid item xs={12}>
            <TextField
              fullWidth
              label="Position Size (₹)"
              type="number"
              value={rsiParams.position_size}
              onChange={(e) => setRsiParams({...rsiParams, position_size: parseFloat(e.target.value)})}
              inputProps={{ min: 1 }}
            />
          </Grid>
        </Grid>
      )}

      <Button
        variant="contained"
        fullWidth
        size="large"
        startIcon={loading ? <CircularProgress size={20} color="inherit" /> : <PlayArrow />}
        onClick={executeStrategy}
        disabled={loading}
        sx={{ mt: 3 }}
      >
        {loading ? 'Executing...' : 'Execute Strategy'}
      </Button>

      {error && (
        <Alert severity="error" sx={{ mt: 2 }}>
          {error}
        </Alert>
      )}

      {success && (
        <Alert severity="success" sx={{ mt: 2 }} icon={<CheckCircle />}>
          Strategy executed successfully!
        </Alert>
      )}
    </Paper>
  )
}

export default StrategyPanel

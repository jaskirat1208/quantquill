import React from 'react'
import { Paper, Typography, Box } from '@mui/material'
import { Activity, TrendingUp, DollarSign, BarChart3 } from 'lucide-react'

interface StatCardProps {
  title: string
  value: string | number
  color: string
}

const iconMap: Record<string, React.ReactNode> = {
  'Active Strategies': <Activity size={24} />,
  'Total Trades': <BarChart3 size={24} />,
  'Profit/Loss': <TrendingUp size={24} />,
  'Position Size': <DollarSign size={24} />,
}

const StatCard: React.FC<StatCardProps> = ({ title, value, color }) => {
  return (
    <Paper 
      elevation={2} 
      sx={{ 
        p: 3, 
        bgcolor: 'background.paper',
        borderRadius: 2,
        height: '100%'
      }}
    >
      <Box display="flex" alignItems="center" justifyContent="space-between">
        <Box>
          <Typography variant="body2" color="text.secondary" gutterBottom>
            {title}
          </Typography>
          <Typography variant="h4" fontWeight="bold" color="white">
            {value}
          </Typography>
        </Box>
        <Box 
          sx={{ 
            p: 1.5, 
            bgcolor: 'rgba(255,255,255,0.05)', 
            borderRadius: 2,
            color: color
          }}
        >
          {iconMap[title] || <Activity size={24} />}
        </Box>
      </Box>
    </Paper>
  )
}

export default StatCard

import React from 'react'
import { 
  Box, 
  Typography, 
  Grid, 
  Card, 
  CardContent,
  Button,
  Container
} from '@mui/material'
import { 
  TrendingUp, 
  Assessment
} from '@mui/icons-material'
import { useNavigate } from 'react-router-dom'

interface LandingPageCardProps {
  title: string
  description: string
  icon: React.ReactNode
  path: string
  color: string
}

const LandingPageCard: React.FC<LandingPageCardProps> = ({ title, description, icon, path, color }) => {
  const navigate = useNavigate()

  const handleClick = () => {
    navigate(path)
  }

  return (
    <Card 
      sx={{ 
        height: '100%', 
        cursor: 'pointer',
        transition: 'transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out',
        '&:hover': {
          transform: 'translateY(-4px)',
          boxShadow: 4
        }
      }}
      onClick={handleClick}
    >
      <CardContent sx={{ p: 3, textAlign: 'center' }}>
        <Box sx={{ color: color, mb: 2 }}>
          {icon}
        </Box>
        <Typography variant="h6" component="h2" fontWeight="bold" gutterBottom>
          {title}
        </Typography>
        <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
          {description}
        </Typography>
        <Button 
          variant="outlined" 
          size="small"
          onClick={handleClick}
          sx={{ borderColor: color, color: color }}
        >
          Launch
        </Button>
      </CardContent>
    </Card>
  )
}

const LandingPage: React.FC = () => {
  const pages = [
    {
      title: 'NSE AB Backtester',
      description: 'Execute and monitor trading strategies with real-time performance metrics and portfolio analysis.',
      icon: <TrendingUp sx={{ fontSize: 48 }} />,
      path: '/nse-ab-backtester',
      color: '#0ea5e9'
    },
    {
      title: 'Instruments',
      description: 'Browse and search available trading instruments with detailed specifications and market data.',
      icon: <Assessment sx={{ fontSize: 48 }} />,
      path: '/instruments',
      color: '#10b981'
    }
  ]

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Box sx={{ textAlign: 'center', mb: 6 }}>
        <Typography variant="h2" component="h1" fontWeight="bold" gutterBottom>
          QuantQuill Platform
        </Typography>
        <Typography variant="h5" color="text.secondary" sx={{ mb: 2 }}>
          Alpha Generation & Strategy Execution Platform
        </Typography>
        <Typography variant="body1" color="text.secondary" sx={{ maxWidth: 600, mx: 'auto' }}>
          Access powerful trading tools, backtesting capabilities, and real-time analytics for quantitative trading strategies.
        </Typography>
      </Box>

      <Grid container spacing={4}>
        {pages.map((page, index) => (
          <Grid item xs={12} sm={6} md={4} key={index}>
            <LandingPageCard {...page} />
          </Grid>
        ))}
      </Grid>

      <Box sx={{ mt: 6, textAlign: 'center' }}>
        <Typography variant="body2" color="text.secondary">
          © 2026 QuantQuill. Built for quantitative trading excellence.
        </Typography>
      </Box>
    </Container>
  )
}

export default LandingPage

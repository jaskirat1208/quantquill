import React, { useState } from 'react'
import { 
  Box, 
  Typography, 
  AppBar, 
  Toolbar,
  CssBaseline
} from '@mui/material'
import { ThemeProvider, createTheme } from '@mui/material/styles'
import { BrowserRouter as Router, Routes, Route, useNavigate, useLocation } from 'react-router-dom'
import Sidebar from './components/Sidebar'
import DashboardPage from './pages/DashboardPage'
import InstrumentsPage from './pages/InstrumentsPage'

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

// Navigation wrapper component
const AppContent: React.FC = () => {
  const navigate = useNavigate()
  const location = useLocation()

  // Map URL paths to active tabs
  const getActiveTabFromPath = (path: string): string => {
    if (path.startsWith('/instruments')) return 'instruments'
    if (path.startsWith('/execute')) return 'execute'
    if (path.startsWith('/results')) return 'results'
    if (path.startsWith('/settings')) return 'settings'
    return 'dashboard'
  }

  const [activeTab, setActiveTab] = useState<string>(getActiveTabFromPath(location.pathname))

  // Update active tab when location changes
  React.useEffect(() => {
    setActiveTab(getActiveTabFromPath(location.pathname))
  }, [location.pathname])

  const handleTabChange = (tabId: string) => {
    setActiveTab(tabId)
    // Navigate to corresponding URL
    switch (tabId) {
      case 'instruments':
        navigate('/instruments')
        break
      case 'execute':
        navigate('/execute')
        break
      case 'results':
        navigate('/results')
        break
      case 'settings':
        navigate('/settings')
        break
      default:
        navigate('/')
    }
  }

  return (
    <Box sx={{ display: 'flex', height: '100vh', bgcolor: 'background.default' }}>
      <Sidebar activeTab={activeTab} setActiveTab={handleTabChange} />
      
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

        {/* Route-based content */}
        <Routes>
          <Route path="/" element={<DashboardPage />} />
          <Route path="/instruments" element={<InstrumentsPage />} />
          <Route path="/execute" element={<DashboardPage />} />
          <Route path="/results" element={<DashboardPage />} />
          <Route path="/settings" element={<DashboardPage />} />
        </Routes>
      </Box>
    </Box>
  )
}

function App() {
  return (
    <ThemeProvider theme={darkTheme}>
      <CssBaseline />
      <Router>
        <AppContent />
      </Router>
    </ThemeProvider>
  )
}

export default App

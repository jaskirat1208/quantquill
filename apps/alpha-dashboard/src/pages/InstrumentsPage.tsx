import React from 'react'
import { Box, Typography } from '@mui/material'
import InstrumentsTable from '../components/InstrumentsTable'

const InstrumentsPage: React.FC = () => {
  return (
    <Box sx={{ width: '100%' }}>
      <Typography variant="h4" fontWeight="bold" sx={{ mb: 3 }}>
        Instruments
      </Typography>
      
      <Typography variant="body1" color="text.secondary" sx={{ mb: 4 }}>
        Search and browse available trading instruments with advanced filtering options.
      </Typography>
      
      <InstrumentsTable />
    </Box>
  )
}

export default InstrumentsPage

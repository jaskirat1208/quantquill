import unittest
from unittest.mock import Mock, patch, mock_open, MagicMock
import json
import os
import tempfile
import shutil
from datetime import datetime

import sys
sys.path.append('/home/jaskirat/projects/quant-quill/src')

from data.angel_one.SmartAPIWithInstruments import SmartConnect
from data.angel_one.constants import INSTRUMENTS_CACHE_PATH, INSTRUMENTS_URL


class TestSmartConnect(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.test_instruments = [
            {
                "token": "99926000",
                "symbol": "NIFTY 50",
                "name": "NIFTY",
                "expiry": "",
                "strike": "0.000000",
                "lotsize": "1",
                "instrumenttype": "AMXIDX",
                "exch_seg": "NSE",
                "tick_size": "0.000000"
            },
            {
                "token": "99926001",
                "symbol": "BANKNIFTY",
                "name": "BANKNIFTY",
                "expiry": "",
                "strike": "0.000000",
                "lotsize": "1",
                "instrumenttype": "AMXIDX",
                "exch_seg": "NSE",
                "tick_size": "0.000000"
            }
        ]
        
        # Mock the parent class
        with patch('data.angel_one.SmartAPIWithInstruments.api.SmartConnect.__init__'):
            self.smart_connect = SmartConnect()
            self.smart_connect.logger = Mock()
    
    def test_init_calls_loadInstruments(self):
        """Test that loadInstruments is called during initialization."""
        with patch('data.angel_one.SmartAPIWithInstruments.api.SmartConnect.__init__'), \
             patch.object(SmartConnect, 'loadInstruments') as mock_load:
            
            smart_connect = SmartConnect()
            mock_load.assert_called_once()
    
    @patch('data.angel_one.SmartAPIWithInstruments.os.path.exists')
    @patch('data.angel_one.SmartAPIWithInstruments.datetime')
    def test_loadInstruments_from_cache(self, mock_datetime, mock_exists):
        """Test loading instruments from cache file."""
        mock_datetime.now.return_value.strftime.return_value = '20231201'
        mock_exists.return_value = True
        
        with patch('builtins.open', mock_open(read_data=json.dumps(self.test_instruments))):
            self.smart_connect.loadInstruments()
            
            # Verify maps are created correctly
            self.assertEqual(len(self.smart_connect.symbol_map), 2)
            self.assertEqual(len(self.smart_connect.token_map), 2)
            self.assertEqual(self.smart_connect.symbol_map['NIFTY 50']['token'], '99926000')
            self.assertEqual(self.smart_connect.token_map['99926001']['symbol'], 'BANKNIFTY')
    
    @patch('data.angel_one.SmartAPIWithInstruments.os.path.exists')
    @patch('data.angel_one.SmartAPIWithInstruments.datetime')
    def test_loadInstruments_from_api(self, mock_datetime, mock_exists):
        """Test loading instruments from API when cache doesn't exist."""
        mock_datetime.now.return_value.strftime.return_value = '20231201'
        mock_exists.return_value = False
        
        with patch.object(self.smart_connect, '_fetchInstrumentsFromAPI', return_value=self.test_instruments), \
             patch('builtins.open', mock_open()) as mock_file:
            
            self.smart_connect.loadInstruments()
            
            # Verify maps are created
            self.assertEqual(len(self.smart_connect.symbol_map), 2)
            self.assertEqual(len(self.smart_connect.token_map), 2)
            
            # Verify file was written
            mock_file.assert_called_with(f"{INSTRUMENTS_CACHE_PATH}instruments.20231201.json", 'w')
    
    @patch('data.angel_one.SmartAPIWithInstruments.os.path.exists')
    @patch('data.angel_one.SmartAPIWithInstruments.datetime')
    def test_loadInstruments_handles_missing_fields(self, mock_datetime, mock_exists):
        """Test that instruments missing symbol or token fields are skipped."""
        mock_datetime.now.return_value.strftime.return_value = '20231201'
        mock_exists.return_value = True
        
        instruments_with_missing_fields = [
            {"token": "99926000", "symbol": "NIFTY 50"},  # Valid
            {"symbol": "BANKNIFTY"},  # Missing token
            {"token": "99926002"},   # Missing symbol
            {"name": "INVALID"}      # Missing both
        ]
        
        with patch('builtins.open', mock_open(read_data=json.dumps(instruments_with_missing_fields))):
            self.smart_connect.loadInstruments()
            
            # Only valid instrument should be in maps
            self.assertEqual(len(self.smart_connect.symbol_map), 1)
            self.assertEqual(len(self.smart_connect.token_map), 1)
            self.assertIn('NIFTY 50', self.smart_connect.symbol_map)
            self.assertIn('99926000', self.smart_connect.token_map)
    
    @patch('data.angel_one.SmartAPIWithInstruments.os.path.exists')
    @patch('data.angel_one.SmartAPIWithInstruments.datetime')
    def test_loadInstruments_handles_exception(self, mock_datetime, mock_exists):
        """Test that exceptions during loading are handled gracefully."""
        mock_datetime.now.return_value.strftime.return_value = '20231201'
        mock_exists.return_value = True
        
        with patch('builtins.open', side_effect=IOError("File not found")):
            self.smart_connect.loadInstruments()
            
            # Maps should be empty due to exception
            self.assertEqual(len(self.smart_connect.symbol_map), 0)
            self.assertEqual(len(self.smart_connect.token_map), 0)
            self.smart_connect.logger.error.assert_called()
    
    @patch('data.angel_one.SmartAPIWithInstruments.requests.get')
    def test_fetchInstrumentsFromAPI(self, mock_get):
        """Test fetching instruments from API."""
        mock_response = Mock()
        mock_response.json.return_value = self.test_instruments
        mock_get.return_value = mock_response
        
        result = self.smart_connect._fetchInstrumentsFromAPI()
        
        mock_get.assert_called_once_with(INSTRUMENTS_URL)
        self.assertEqual(result, self.test_instruments)
    
    def test_getInstrumentBySymbol_success(self):
        """Test successfully getting instrument by symbol."""
        # Set up the symbol map
        self.smart_connect.symbol_map = {'NIFTY 50': self.test_instruments[0]}
        
        result = self.smart_connect.getInstrumentBySymbol('NIFTY 50')
        
        self.assertEqual(result, self.test_instruments[0])
    
    def test_getInstrumentBySymbol_not_found(self):
        """Test getting instrument by symbol when not found."""
        self.smart_connect.symbol_map = {}
        
        result = self.smart_connect.getInstrumentBySymbol('NONEXISTENT')
        
        self.assertIsNone(result)
        self.smart_connect.logger.warning.assert_called_with("Instrument not found for symbol: NONEXISTENT")
    
    def test_getInstrumentBySymbol_exception(self):
        """Test handling exception when getting instrument by symbol."""
        self.smart_connect.symbol_map = Mock()
        self.smart_connect.symbol_map.get.side_effect = Exception("Test exception")
        
        with self.assertRaises(Exception):
            self.smart_connect.getInstrumentBySymbol('NIFTY 50')
        
        self.smart_connect.logger.error.assert_called()
    
    def test_getInstrumentByToken_success(self):
        """Test successfully getting instrument by token."""
        # Set up the token map
        self.smart_connect.token_map = {'99926000': self.test_instruments[0]}
        
        result = self.smart_connect.getInstrumentByToken('99926000')
        
        self.assertEqual(result, self.test_instruments[0])
    
    def test_getInstrumentByToken_not_found(self):
        """Test getting instrument by token when not found."""
        self.smart_connect.token_map = {}
        
        result = self.smart_connect.getInstrumentByToken('99999999')
        
        self.assertIsNone(result)
        self.smart_connect.logger.warning.assert_called_with("Instrument not found for token: 99999999")
    
    def test_getInstrumentByToken_exception(self):
        """Test handling exception when getting instrument by token."""
        self.smart_connect.token_map = Mock()
        self.smart_connect.token_map.get.side_effect = Exception("Test exception")
        
        with self.assertRaises(Exception):
            self.smart_connect.getInstrumentByToken('99926000')
        
        self.smart_connect.logger.error.assert_called()


class TestSmartConnectIntegration(unittest.TestCase):
    """Integration tests for SmartConnect class."""
    
    def setUp(self):
        """Set up integration test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.original_cache_path = INSTRUMENTS_CACHE_PATH
        
    def tearDown(self):
        """Clean up integration test fixtures."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    @patch('data.angel_one.SmartAPIWithInstruments.api.SmartConnect.__init__')
    def test_full_loadInstruments_workflow(self, mock_parent_init):
        """Test the complete loadInstruments workflow with real file operations."""
        # Mock the cache path to use temp directory
        with patch('data.angel_one.SmartAPIWithInstruments.INSTRUMENTS_CACHE_PATH', self.temp_dir + '/'):
            with patch.object(SmartConnect, '_fetchInstrumentsFromAPI') as mock_fetch:
                mock_fetch.return_value = [
                    {"token": "99926000", "symbol": "NIFTY 50", "name": "NIFTY"}
                ]
                
                with patch('data.angel_one.SmartAPIWithInstruments.datetime') as mock_datetime:
                    mock_datetime.now.return_value.strftime.return_value = '20231201'
                    
                    smart_connect = SmartConnect()
                    smart_connect.logger = Mock()
                    
                    # First load - should fetch from API
                    smart_connect.loadInstruments()
                    
                    # Verify file was created
                    cache_file = f"{self.temp_dir}/instruments.20231201.json"
                    self.assertTrue(os.path.exists(cache_file))
                    
                    # Second load - should use cache
                    smart_connect.loadInstruments()
                    
                    # Verify API was called only once
                    mock_fetch.assert_called_once()


if __name__ == '__main__':
    unittest.main()

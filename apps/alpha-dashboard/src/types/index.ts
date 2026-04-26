// API Types
export interface Trade {
  side: 'BUY' | 'SELL'
  price: number
  quantity: number
  timestamp: string
  token: string
}

export interface PortfolioSnapshot {
  timestamp: string
  price: number
  cash: number
  positions: Record<string, number>
  position_value: number
  total_value: number
  pnl: number
}

export interface StrategyResult {
  strategy_name: string
  symbol: string
  executed_at: string
  parameters: Record<string, unknown>
  success: boolean
  message?: string
  trades: Trade[]
  profit_loss?: number
  max_drawdown?: number
  volatility?: number
  sharpe_ratio?: number
  win_rate?: number
  total_return?: number
  portfolio_snapshots?: PortfolioSnapshot[]
}

export interface StrategyInfo {
  name: string
  description: string
  parameters: string[]
}

export interface StrategiesResponse {
  strategies: StrategyInfo[]
}

// Form Types
export interface MovingAverageParams {
  symbol: string
  short_window: number
  long_window: number
  position_size: number
}

export interface RSIParams {
  symbol: string
  rsi_period: number
  oversold: number
  overbought: number
  position_size: number
}

// Component Props
export interface SidebarProps {
  activeTab: string
  setActiveTab: (tab: string) => void
}

export interface StrategyPanelProps {
  onResults: (results: StrategyResult) => void
}

export interface ChartPanelProps {
  strategyResults: StrategyResult | null
}

export interface TradesTableProps {
  trades: Trade[]
}

// Instrument Types
export interface Instrument {
  token?: string
  symbol?: string
  name?: string
  expiry?: string
  strike?: number
  lotsize?: number
  instrumenttype?: string
  exch_seg?: string
  tick_size?: number
  [key: string]: any
}

export interface InstrumentsResponse {
  instruments: Instrument[]
  pagination: {
    page: number
    page_size: number
    total_items: number
    total_pages: number
    has_next: boolean
    has_prev: boolean
  }
}

export interface InstrumentsTableProps {
  instruments?: Instrument[]
}

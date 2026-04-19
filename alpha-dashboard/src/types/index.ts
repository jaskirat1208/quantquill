// API Types
export interface Trade {
  action: 'BUY' | 'SELL'
  price: number
  quantity: number
  time: string
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

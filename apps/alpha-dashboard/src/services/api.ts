import axios, { AxiosInstance } from 'axios'
import type { StrategyResult, StrategiesResponse, MovingAverageParams, RSIParams } from '../types'

const api: AxiosInstance = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
})

// Strategy API
export const strategyApi = {
  getStrategies: () => api.get<StrategiesResponse>('/strategies'),
  executeMovingAverage: (params: MovingAverageParams) => api.post<StrategyResult>('/strategies/moving_average/execute', params),
  executeRSI: (params: RSIParams) => api.post<StrategyResult>('/strategies/rsi/execute', params),
}

// Health API
export const healthApi = {
  checkHealth: () => api.get<{ status: string; service: string }>('/health'),
  getRoot: () => api.get<{ message: string; status: string }>('/'),
}

export default api

import axios, { AxiosInstance } from 'axios';
import type {
  StrategyResult,
  StrategiesResponse,
  MovingAverageParams,
  RSIParams,
  Instrument,
  InstrumentsResponse,
} from '../types';

const api: AxiosInstance = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Strategy API
export const strategyApi = {
  getStrategies: () => api.get<StrategiesResponse>('/strategies'),
  executeMovingAverage: (params: MovingAverageParams) =>
    api.post<StrategyResult>('/strategies/moving_average/execute', params),
  executeRSI: (params: RSIParams) =>
    api.post<StrategyResult>('/strategies/rsi/execute', params),
};

// Instruments API
export const instrumentsApi = {
  getInstruments: (page: number, pageSize: number, search?: string) => {
    const params: any = {
      page,
      page_size: pageSize,
    };
    if (search) {
      params.search = search;
    }
    return api.get<InstrumentsResponse>('/instruments/search', { params });
  },
  searchInstruments: (
    page: number,
    pageSize: number,
    search?: string,
    exchange?: string,
    instrumentType?: string
  ) => {
    const params: any = {
      page,
      page_size: pageSize,
    };
    if (search) {
      params.search = search;
    }
    if (exchange) {
      params.exchange = exchange;
    }
    if (instrumentType) {
      params.instrument_type = instrumentType;
    }
    return api.get<InstrumentsResponse>('/instruments/search', { params });
  },
  getAllInstruments: (page: number, pageSize: number) => {
    const params: any = {
      page,
      page_size: pageSize,
    };
    return api.get<InstrumentsResponse>('/instruments/all', { params });
  },
};

// Health API
export const healthApi = {
  checkHealth: () => api.get<{ status: string; service: string }>('/health'),
  getRoot: () => api.get<{ message: string; status: string }>('/'),
};

export default api;

// API 服务层 - 适配后端实际接口
const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000/api';

async function fetchAPI<T>(url: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${url}`, {
    headers: {
      'Content-Type': 'application/json',
      ...options?.headers,
    },
    ...options,
  });
  
  if (!response.ok) {
    throw new Error(`API Error: ${response.status}`);
  }
  
  return response.json();
}

// 类型定义 - 适配后端返回格式
export interface MarketIndex {
  code: string;
  name: string;
  current: number;
  change: number;
  changePercent: number;
  volume: number;
  amount?: number;
  open?: number;
  high?: number;
  low?: number;
}

export interface MarketOverview {
  shanghai: { index: number; change_percent: number; volume: number };
  shenzhen: { index: number; change_percent: number; volume: number };
  chinext: { index: number; change_percent: number; volume: number };
}

export interface StockInfo {
  code: string;
  name: string;
  current: number;
  change: number;
  changePercent: number;
  open: number;
  high: number;
  low: number;
  volume: number;
  amount: number;
  turnover?: number;
  pe?: number;
  pb?: number;
  marketCap?: number;
  timestamp?: string;
}

export interface StockRaw {
  code: string;
  name: string;
  current_price: number;
  change: number;
  change_percent: number;
  volume: number;
  amount: number;
  open: number;
  high: number;
  low: number;
  prev_close: number;
  last_updated: string;
}

export interface RankingItem {
  rank: number;
  code: string;
  name: string;
  current: number;
  change: number;
  changePercent: number;
  volume: number;
  amount?: number;
}

export interface RankingRaw {
  up: Array<{ code: string; name: string; current_price: number; change: number; change_percent: number; volume: number; amount?: number }>;
  down: Array<{ code: string; name: string; current_price: number; change: number; change_percent: number; volume: number; amount?: number }>;
}

// 数据转换函数
function convertMarketOverview(data: MarketOverview): MarketIndex[] {
  return [
    { code: '000001', name: '上证指数', current: data.shanghai.index, changePercent: data.shanghai.change_percent, change: data.shanghai.index * data.shanghai.change_percent / 100, volume: data.shanghai.volume },
    { code: '399001', name: '深证成指', current: data.shenzhen.index, changePercent: data.shenzhen.change_percent, change: data.shenzhen.index * data.shenzhen.change_percent / 100, volume: data.shenzhen.volume },
    { code: '399006', name: '创业板指', current: data.chinext.index, changePercent: data.chinext.change_percent, change: data.chinext.index * data.chinext.change_percent / 100, volume: data.chinext.volume },
  ];
}

function convertStockInfo(data: StockRaw): StockInfo {
  return {
    code: data.code,
    name: data.name,
    current: data.current_price,
    change: data.change,
    changePercent: data.change_percent,
    open: data.open,
    high: data.high,
    low: data.low,
    volume: data.volume,
    amount: data.amount,
    timestamp: data.last_updated,
  };
}

function convertRanking(data: RankingRaw, type: string = 'up'): RankingItem[] {
  const list = type === 'down' ? data.down : data.up;
  return list.map((item, idx) => ({
    rank: idx + 1,
    code: item.code,
    name: item.name,
    current: item.current_price,
    change: item.change,
    changePercent: item.change_percent,
    volume: item.volume,
    amount: item.amount,
  }));
}

// API 函数
export const marketAPI = {
  // 获取大盘行情
  getMarket: async () => {
    const data = await fetchAPI<MarketOverview>('/market/overview');
    return convertMarketOverview(data);
  },
  
  // 获取个股详情
  getStock: async (code: string) => {
    const data = await fetchAPI<StockRaw>(`/stocks/${code}`);
    return convertStockInfo(data);
  },
  
  // 获取排行榜
  getRanking: async (type: string = 'up', limit: number = 20) => {
    const data = await fetchAPI<RankingRaw>(`/stocks/rankings?limit=${limit}`);
    const items = convertRanking(data, type);
    return {
      type,
      date: new Date().toISOString().split('T')[0],
      items,
    };
  },
};

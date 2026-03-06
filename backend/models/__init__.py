"""数据模型"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class MarketIndex(BaseModel):
    """大盘指数"""
    code: str  # 指数代码，如 000001（上证指数）
    name: str  # 指数名称
    current: float  # 当前点位
    change: float  # 涨跌额
    change_pct: float  # 涨跌幅(%)
    volume: float  # 成交量(手)
    amount: float  # 成交额(元)
    open: float  # 开盘价
    high: float  # 最高价
    low: float  # 最低价
    prev_close: float  # 昨收价
    updated_at: str  # 更新时间


class StockInfo(BaseModel):
    """个股信息"""
    code: str  # 股票代码
    name: str  # 股票名称
    current: float  # 当前价格
    change: float  # 涨跌额
    change_pct: float  # 涨跌幅(%)
    volume: float  # 成交量(手)
    amount: float  # 成交额(元)
    open: float  # 开盘价
    high: float  # 最高价
    low: float  # 最低价
    prev_close: float  # 昨收价
    turnover_rate: Optional[float] = None  # 换手率(%)
    pe: Optional[float] = None  # 市盈率
    market_cap: Optional[float] = None  # 总市值(元)
    updated_at: str  # 更新时间


class RankingItem(BaseModel):
    """排行榜项"""
    rank: int  # 排名
    code: str  # 股票代码
    name: str  # 股票名称
    current: float  # 当前价格
    change: float  # 涨跌额
    change_pct: float  # 涨跌幅(%)
    volume: float  # 成交量
    amount: float  # 成交额


class RankingResponse(BaseModel):
    """排行榜响应"""
    type: str  # 排行榜类型: up / down / volume
    date: str  # 日期
    items: list[RankingItem]

from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from datetime import datetime

from services.market_service import get_market_index_data, get_stock_data, get_ranking_data
from models import MarketIndex, StockInfo, RankingItem

router = APIRouter(prefix="/api")


@router.get("/market/overview")
async def get_market_overview():
    """获取大盘行情 - 真实数据"""
    try:
        indices = await get_market_index_data()
        
        if not indices:
            raise HTTPException(status_code=503, detail="无法获取行情数据")
        
        # 转换为前端期望的格式
        result = {}
        for idx in indices:
            key = "shanghai" if idx.code == "000001" else ("shenzhen" if idx.code == "399001" else "chinext")
            result[key] = {
                "index": idx.current,
                "change_percent": idx.change_pct,
                "volume": idx.volume,
                "change": idx.change,
                "open": idx.open,
                "high": idx.high,
                "low": idx.low,
                "prev_close": idx.prev_close
            }
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        print(f"大盘行情接口错误：{e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stocks/{code}")
async def get_stock_detail(code: str):
    """获取个股详情 - 真实数据"""
    try:
        stock = await get_stock_data(code)
        
        if not stock:
            raise HTTPException(status_code=404, detail="未找到该股票")
        
        return {
            "code": stock.code,
            "name": stock.name,
            "current_price": stock.current,
            "change": stock.change,
            "change_percent": stock.change_pct,
            "volume": stock.volume,
            "amount": stock.amount,
            "open": stock.open,
            "high": stock.high,
            "low": stock.low,
            "prev_close": stock.prev_close,
            "last_updated": stock.updated_at
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"个股详情接口错误：{e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stocks/rankings")
async def get_stock_rankings(
    limit: int = Query(default=20, ge=1, le=100)
):
    """获取涨跌幅排行榜 - 真实数据"""
    try:
        # 获取涨幅榜和跌幅榜
        up_rankings = await get_ranking_data(rank_type="up", limit=limit)
        down_rankings = await get_ranking_data(rank_type="down", limit=limit)
        
        return {
            "up": [
                {
                    "rank": r.rank,
                    "code": r.code,
                    "name": r.name,
                    "current_price": r.current,
                    "change": r.change,
                    "change_percent": r.change_pct,
                    "volume": r.volume,
                    "amount": r.amount
                }
                for r in up_rankings
            ],
            "down": [
                {
                    "rank": r.rank,
                    "code": r.code,
                    "name": r.name,
                    "current_price": r.current,
                    "change": r.change,
                    "change_percent": r.change_pct,
                    "volume": r.volume,
                    "amount": r.amount
                }
                for r in down_rankings
            ]
        }
    except Exception as e:
        print(f"排行榜接口错误：{e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/search")
async def search_stocks(q: str):
    """股票搜索"""
    try:
        # 使用 adata 获取所有股票代码
        import adata.stock.info as info
        
        all_codes = info.all_code()
        results = []
        
        # 搜索匹配
        for _, row in all_codes.iterrows():
            code = row.get('stock_code', '')
            name = row.get('short_name', '')
            
            if q.lower() in name.lower() or q in code:
                # 获取实时行情
                try:
                    import adata.stock.market as market
                    full_code = f"sh.{code}" if code.startswith('6') else f"sz.{code}"
                    df = market.get_market(stock_code=full_code, k_type=1)
                    
                    if not df.empty:
                        row_data = df.iloc[-1]
                        results.append({
                            "code": code,
                            "name": name,
                            "current_price": float(row_data.get('close', 0))
                        })
                except:
                    # 获取行情失败时返回基本信息
                    results.append({
                        "code": code,
                        "name": name,
                        "current_price": 0
                    })
                
                if len(results) >= 20:
                    break
        
        return {"results": results}
    except Exception as e:
        print(f"搜索接口错误：{e}")
        raise HTTPException(status_code=500, detail=str(e))

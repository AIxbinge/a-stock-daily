"""行情数据服务"""
import json
from datetime import datetime
from typing import Optional

import adata.stock.market as market
import adata.stock.info as info

from db.database import get_redis
from models import MarketIndex, StockInfo, RankingItem


# 缓存 TTL（秒）
CACHE_TTL = 30


async def get_market_index_data() -> list[MarketIndex]:
    """获取大盘行情数据"""
    try:
        redis = await get_redis()
        cache_key = "market:indices"
        cached = await redis.get(cache_key)
        if cached:
            data = json.loads(cached)
            return [MarketIndex(**item) for item in data]
    except Exception:
        pass  # Redis 不可用时跳过缓存
    
    try:
        codes = [
            ("000001", "上证指数"),
            ("399001", "深证成指"),
            ("399006", "创业板指")
        ]
        result = []
        
        for code, name in codes:
            try:
                df = market.get_market_index(index_code=code)
                if not df.empty:
                    row = df.iloc[-1]
                    market_index = MarketIndex(
                        code=code,
                        name=name,
                        current=float(row.get('close', 0)),
                        change=float(row.get('change', 0)),
                        change_pct=float(row.get('change_pct', 0)),
                        volume=float(row.get('volume', 0)) / 100,
                        amount=float(row.get('amount', 0)),
                        open=float(row.get('open', 0)),
                        high=float(row.get('high', 0)),
                        low=float(row.get('low', 0)),
                        prev_close=float(row.get('close', 0)) - float(row.get('change', 0)),
                        updated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    )
                    result.append(market_index)
            except Exception as e:
                print(f"获取 {code} 行情失败: {e}")
                continue
        
        # 缓存结果
        if result:
            try:
                redis = await get_redis()
                await redis.setex(cache_key, CACHE_TTL, json.dumps([m.model_dump() for m in result]))
            except:
                pass
        
        return result
        
    except Exception as e:
        print(f"获取大盘行情失败: {e}")
        return []


async def get_stock_data(code: str) -> Optional[StockInfo]:
    """获取个股行情数据"""
    try:
        redis = await get_redis()
        cache_key = f"stock:{code}"
        cached = await redis.get(cache_key)
        if cached:
            data = json.loads(cached)
            return StockInfo(**data)
    except:
        pass
    
    try:
        # 格式转换
        if code.startswith('6'):
            full_code = f"sh.{code}"
        else:
            full_code = f"sz.{code}"
        
        df = market.get_market(stock_code=full_code, k_type=1)
        if df.empty:
            return None
        
        row = df.iloc[-1]
        
        # 获取名称
        stock_name = code
        try:
            all_codes = info.all_code()
            match = all_codes[all_codes['stock_code'] == code]
            if not match.empty:
                stock_name = match.iloc[0].get('short_name', code)
        except:
            pass
        
        stock_info_data = StockInfo(
            code=code,
            name=stock_name,
            current=float(row.get('close', 0)),
            change=float(row.get('change', 0)),
            change_pct=float(row.get('change_pct', 0)),
            volume=float(row.get('volume', 0)) / 100,
            amount=float(row.get('amount', 0)),
            open=float(row.get('open', 0)),
            high=float(row.get('high', 0)),
            low=float(row.get('low', 0)),
            prev_close=float(row.get('close', 0)) - float(row.get('change', 0)),
            updated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        
        try:
            redis = await get_redis()
            await redis.setex(cache_key, CACHE_TTL, json.dumps(stock_info_data.model_dump()))
        except:
            pass
        
        return stock_info_data
        
    except Exception as e:
        print(f"获取 {code} 行情失败: {e}")
        return None


async def get_ranking_data(rank_type: str = "up", limit: int = 50) -> list[RankingItem]:
    """获取排行榜数据"""
    try:
        redis = await get_redis()
        cache_key = f"ranking:{rank_type}:{limit}"
        cached = await redis.get(cache_key)
        if cached:
            data = json.loads(cached)
            return [RankingItem(**item) for item in data]
    except:
        pass
    
    try:
        result = []
        
        # 使用上证指数历史数据模拟
        df = market.get_market_index(index_code='000001')
        if not df.empty:
            df_sorted = df.sort_values('change_pct', ascending=(rank_type == "down"))
            
            for i, row in df_sorted.head(limit).iterrows():
                ranking_item = RankingItem(
                    rank=len(result) + 1,
                    code=row.get('index_code', ''),
                    name=row.get('index_code', ''),
                    current=float(row.get('close', 0)),
                    change=float(row.get('change', 0)),
                    change_pct=float(row.get('change_pct', 0)),
                    volume=float(row.get('volume', 0)) / 100,
                    amount=float(row.get('amount', 0))
                )
                result.append(ranking_item)
        
        if result:
            try:
                redis = await get_redis()
                await redis.setex(cache_key, CACHE_TTL, json.dumps([r.model_dump() for r in result]))
            except:
                pass
        
        return result
        
    except Exception as e:
        print(f"获取排行榜失败: {e}")
        return []

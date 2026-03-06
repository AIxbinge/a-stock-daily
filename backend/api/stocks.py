from fastapi import APIRouter, HTTPException
from typing import List
from datetime import datetime
import random

router = APIRouter(prefix="/api")


def _generate_mock_data():
    """生成模拟数据"""
    stocks_db = {
        "600000": {"name": "浦发银行", "base_price": 12.50},
        "600036": {"name": "招商银行", "base_price": 35.80},
        "600519": {"name": "贵州茅台", "base_price": 1680.00},
        "000001": {"name": "平安银行", "base_price": 12.30},
        "000002": {"name": "万科A", "base_price": 8.90},
        "300750": {"name": "宁德时代", "base_price": 185.60},
        "601318": {"name": "中国平安", "base_price": 48.50},
        "600276": {"name": "恒瑞医药", "base_price": 52.30},
    }
    
    indices = {
        "shanghai": {"index": 3420.50 + random.uniform(-20, 20), "change_percent": 0.65 + random.uniform(-0.3, 0.3)},
        "shenzhen": {"index": 11580.30 + random.uniform(-50, 50), "change_percent": 1.15 + random.uniform(-0.3, 0.3)},
        "chinext": {"index": 2480.60 + random.uniform(-20, 20), "change_percent": 1.85 + random.uniform(-0.3, 0.3)},
    }
    
    return stocks_db, indices


# 注意：静态路由必须放在路径参数路由之前


@router.get("/stocks/rankings")
async def get_stock_rankings(limit: int = 20):
    """获取涨跌幅排行榜"""
    stocks_db, _ = _generate_mock_data()
    
    rankings = []
    for code, info in stocks_db.items():
        change = random.uniform(-8, 8)
        rankings.append({
            "code": code,
            "name": info["name"],
            "current_price": round(info["base_price"] * (1 + change / 100), 2),
            "change": round(info["base_price"] * change / 100, 2),
            "change_percent": round(change, 2),
            "volume": random.randint(1000000, 50000000)
        })
    
    rankings_up = sorted(rankings, key=lambda x: x["change_percent"], reverse=True)[:limit]
    rankings_down = sorted(rankings, key=lambda x: x["change_percent"])[:limit]
    
    return {"up": rankings_up, "down": rankings_down}


@router.get("/search")
async def search_stocks(q: str):
    """股票搜索"""
    stocks_db, _ = _generate_mock_data()
    
    results = []
    for code, info in stocks_db.items():
        if q.lower() in info["name"].lower() or q in code:
            results.append({
                "code": code,
                "name": info["name"],
                "current_price": info["base_price"]
            })
    
    return {"results": results}


@router.get("/stocks/{code}")
async def get_stock_detail(code: str):
    """获取个股详情"""
    stocks_db, _ = _generate_mock_data()
    
    if code not in stocks_db:
        for k, v in stocks_db.items():
            if k.startswith(code[:3]):
                code = k
                break
        else:
            raise HTTPException(status_code=404, detail="Stock not found")
    
    stock = stocks_db[code]
    change = random.uniform(-3, 3)
    current_price = stock["base_price"] * (1 + change / 100)
    
    return {
        "code": code,
        "name": stock["name"],
        "current_price": round(current_price, 2),
        "change": round(stock["base_price"] * change / 100, 2),
        "change_percent": round(change, 2),
        "volume": random.randint(1000000, 50000000),
        "amount": random.randint(50000000, 5000000000),
        "open": round(stock["base_price"] * (1 + random.uniform(-0.5, 0.5) / 100), 2),
        "high": round(stock["base_price"] * (1 + random.uniform(0, 2) / 100), 2),
        "low": round(stock["base_price"] * (1 + random.uniform(-2, 0) / 100), 2),
        "prev_close": stock["base_price"],
        "last_updated": datetime.now().isoformat()
    }


@router.get("/market/overview")
async def get_market_overview():
    """获取大盘概览"""
    _, indices = _generate_mock_data()
    return {
        "shanghai": {
            "index": round(indices["shanghai"]["index"], 2),
            "change_percent": round(indices["shanghai"]["change_percent"], 2),
            "volume": random.randint(30000000000, 50000000000)
        },
        "shenzhen": {
            "index": round(indices["shenzhen"]["index"], 2),
            "change_percent": round(indices["shenzhen"]["change_percent"], 2),
            "volume": random.randint(25000000000, 45000000000)
        },
        "chinext": {
            "index": round(indices["chinext"]["index"], 2),
            "change_percent": round(indices["chinext"]["change_percent"], 2),
            "volume": random.randint(10000000000, 25000000000)
        }
    }

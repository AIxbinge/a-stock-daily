"""大盘行情 API"""
from fastapi import APIRouter

from services import market_service
from models import MarketIndex

router = APIRouter()


@router.get("/market", response_model=list[MarketIndex])
async def get_market():
    """获取大盘行情
    
    返回上证指数、深证成指、创业板指的实时行情
    """
    return await market_service.get_market_index_data()

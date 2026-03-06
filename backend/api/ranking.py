"""排行榜 API"""
from fastapi import APIRouter, Query

from services import market_service
from models import RankingResponse

router = APIRouter()


@router.get("/ranking", response_model=RankingResponse)
async def get_ranking(
    type: str = Query("up", description="排行榜类型: up-涨幅榜, down-跌幅榜, volume-成交额榜"),
    limit: int = Query(50, ge=1, le=100, description="返回数量")
):
    """获取排行榜数据
    
    返回 A 股涨跌幅排行或成交额排行
    """
    # 验证类型
    if type not in ["up", "down", "volume"]:
        type = "up"
    
    items = await market_service.get_ranking_data(rank_type=type, limit=limit)
    
    from datetime import datetime
    return RankingResponse(
        type=type,
        date=datetime.now().strftime("%Y-%m-%d"),
        items=items
    )

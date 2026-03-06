"""个股详情 API"""
from fastapi import APIRouter, HTTPException, Path

from services import market_service
from models import StockInfo

router = APIRouter()


@router.get("/stock/{code}", response_model=StockInfo)
async def get_stock(code: str = Path(..., description="股票代码，如 600000")):
    """获取个股详情
    
    根据股票代码返回实时行情数据
    """
    # 验证股票代码格式
    if not code or len(code) < 6:
        raise HTTPException(status_code=400, detail="无效的股票代码")
    
    stock_data = await market_service.get_stock_data(code)
    
    if not stock_data:
        raise HTTPException(status_code=404, detail=f"未找到股票 {code} 的数据")
    
    return stock_data

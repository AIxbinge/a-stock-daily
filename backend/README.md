# A股日报后端服务

## 技术栈
- Python 3.9+
- FastAPI
- Redis (缓存)
- PostgreSQL (可选，用于用户数据)

## API 文档
启动服务后访问: `http://localhost:8000/docs`

## 开发环境
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

## 核心API接口
- `GET /api/stocks/{code}` - 个股详情
- `GET /api/market/overview` - 大盘概览  
- `GET /api/stocks/rankings` - 涨跌幅排行榜
- `GET /api/search?q={keyword}` - 股票搜索

## 数据源集成
- 行情数据: Ashare + adata
- 新闻资讯: 聚合数据API
- 缓存: Redis (30秒TTL)
# A 股日报 - 技术架构文档

## 🏗️ 整体架构

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   前端应用   │◄──►│   API 网关    │◄──►│  数据服务层   │
│  React+TS   │    │  FastAPI    │    │  Python     │
└─────────────┘    └─────────────┘    └─────────────┘
                                         │
                    ┌────────────────────┼────────────────────┐
                    │                    │                    │
              ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
              │  行情数据服务  │    │  新闻资讯服务  │    │  缓存服务    │
              │  Ashare     │    │  聚合数据    │    │   Redis    │
              │  adata      │    │            │    │            │
              └─────────────┘    └─────────────┘    └─────────────┘
                                        │
                                 ┌─────────────┐
                                 │  PostgreSQL │
                                 │  数据库     │
                                 └─────────────┘
```

---

## 📂 模块划分

### 前端模块 (`/frontend`)

| 模块 | 说明 |
|------|------|
| `components/` | 通用组件库 |
| `pages/` | 页面组件（首页/个股/排行/新闻） |
| `services/` | API 调用封装 |
| `store/` | 状态管理 (Redux) |
| `utils/` | 工具函数 |
| `hooks/` | 自定义 Hooks |

### 后端模块 (`/backend`)

| 模块 | 说明 |
|------|------|
| `api/` | RESTful API 路由 |
| `services/` | 业务逻辑层 |
| `models/` | 数据模型 |
| `db/` | 数据库配置 |
| `utils/` | 工具函数 |
| `tasks/` | 定时任务 (Celery) |

### 测试模块 (`/tests`)

| 模块 | 说明 |
|------|------|
| `test-cases/` | 测试用例文档 |
| `scripts/` | 自动化测试脚本 |
| `config/` | 测试配置 |
| `reports/` | 测试报告 |

---

## 🔄 数据流设计

### 行情数据流

```
第三方 API (Ashare/adata)
        ↓
   数据服务层 (清洗/转换)
        ↓
     Redis 缓存 (TTL=30s)
        ↓
     API 网关 (FastAPI)
        ↓
    前端应用 (React)
        ↓
    ECharts 渲染
```

### 用户自选股数据流

```
前端提交自选股
        ↓
   API 网关验证
        ↓
  PostgreSQL 存储
        ↓
     返回确认
```

---

## 🛠️ 技术栈

### 前端

- **框架**: React 18 + TypeScript
- **UI 库**: Ant Design 5.x
- **图表**: ECharts 5.x
- **状态管理**: Redux Toolkit
- **构建工具**: Vite

### 后端

- **框架**: FastAPI
- **语言**: Python 3.9+
- **数据库**: PostgreSQL 14
- **缓存**: Redis 7
- **任务队列**: Celery + Redis

### 运维

- **容器**: Docker + Docker Compose
- **CI/CD**: GitHub Actions
- **监控**: Prometheus + Grafana

---

## 📊 数据库设计

### 用户表 (`users`)

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 自选股表 (`user_stocks`)

```sql
CREATE TABLE user_stocks (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    stock_code VARCHAR(10) NOT NULL,
    stock_name VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, stock_code)
);
```

---

## 🔐 安全规范

- API Key 存储在环境变量，不提交到 Git
- 用户密码使用 bcrypt 加密
- API 接口实施限流（Redis 计数器）
- 敏感操作记录审计日志

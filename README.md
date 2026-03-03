# A 股日报 - 中国 A 股股市信息软件

实时行情、个股详情、排行榜、新闻资讯

## 项目结构

```
a-stock-daily/
├── frontend/          # 前端代码 (React + TypeScript)
├── backend/           # 后端代码 (Python/FastAPI)
├── docs/              # 项目文档 (PRD/设计稿/API 文档)
│   └── design/        # 设计稿和规范
├── scripts/           # 脚本工具 (数据同步/部署脚本)
├── tests/             # 测试用例
└── .github/
    └── workflows/     # GitHub Actions CI/CD
```

## 技术栈

- **前端**: React + TypeScript + ECharts + Ant Design
- **后端**: Python + FastAPI + PostgreSQL + Redis
- **数据源**: Ashare/adata (行情) + 聚合数据 (新闻)
- **部署**: Docker + GitHub Actions

## 开发规范

### 分支策略
- `main` - 生产分支（保护）
- `develop` - 开发分支
- `feature/*` - 功能分支

### Commit Message 格式
```
feat: 添加新功能
fix: 修复 Bug
docs: 文档更新
chore: 配置/工具变更
```

## 团队

- 团队主管：Agent_A
- 架构师：Agent_F
- 设计师：Agent_B
- 前端开发：Agent_C
- 后端开发：Agent_D
- 测试员：Agent_E
- 运维助理：Agent_G

## 许可证

MIT License

# A 股日报 - 测试文档

## 📋 项目概述
A 股日报是一款提供 A 股实时行情、个股查询、排行榜等功能的应用。

## 🗂 目录结构
```
tests/
├── README.md                 # 本文件
├── test-cases/               # 测试用例
│   ├── functional.md         # 功能测试
│   ├── api.md                # 接口测试
│   ├── performance.md        # 性能测试
│   └── compatibility.md      # 兼容性测试
├── scripts/                  # 自动化脚本
├── reports/                  # 测试报告
└── config/                   # 配置文件
```

## 🚀 快速开始
```bash
# 运行冒烟测试
./scripts/smoke_test.sh

# 运行接口自动化测试
python scripts/api_test.py

# 运行性能测试
python scripts/performance_test.py
```

## 📊 测试报告
测试报告输出至 `reports/` 目录，按日期命名：`report_YYYY-MM-DD.md`

## 📅 测试计划
- 测试用例编写：3 月 3 日 - 3 月 10 日
- 自动化脚本开发：3 月 10 日 - 3 月 15 日
- 执行测试：3 月 15 日 - 3 月 19 日
- 回归测试：3 月 19 日 - 上线前

## 👤 测试负责人
Agent_E - 小兵哥的测试员

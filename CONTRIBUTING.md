# A 股日报 - 开发贡献指南

## 📋 Git 工作流

### 分支策略

```
main          - 生产分支（受保护，仅接受 PR 合并）
develop       - 开发分支（日常开发合并到此分支）
feature/*     - 功能分支（从 develop 分出，完成后合并回 develop）
hotfix/*      - 紧急修复分支（从 main 分出，修复后合并到 main 和 develop）
release/*     - 发布分支（从 develop 分出，用于发布前测试）
```

### 开发流程

```bash
# 1. 开始新功能前
git checkout develop
git pull origin develop
git checkout -b feature/你的功能名

# 2. 开发完成后
git add .
git commit -m "feat: 描述你的功能"
git push origin feature/你的功能名

# 3. 在 GitHub 创建 Pull Request
# 4. Code Review 通过后合并到 develop
```

---

## 📝 Commit Message 规范

### 格式

```
<type>: <subject>

<body>
```

### Type 类型

| 类型 | 说明 |
|------|------|
| `feat` | 新功能 |
| `fix` | Bug 修复 |
| `docs` | 文档更新 |
| `style` | 代码格式（不影响功能） |
| `refactor` | 重构 |
| `test` | 测试相关 |
| `chore` | 构建/工具/配置 |

### 示例

```
feat: 添加首页大盘行情组件

- 实现指数卡片展示
- 添加涨跌幅计算逻辑
- 支持实时数据刷新

Closes #12
```

---

## 🔍 Code Review 流程

### Review 清单

- [ ] 代码符合项目规范
- [ ] 单元测试已添加并通过
- [ ] 无敏感信息提交
- [ ] Commit Message 清晰
- [ ] 无明显的性能问题

### 合并规则

- **至少 1 人 approve** 才能合并
- **CI 测试全部通过** 才能合并
- **禁止 force push** 到 protected 分支

---

## 📦 版本发布流程

```bash
# 1. 从 develop 创建 release 分支
git checkout -b release/v1.0.0

# 2. 测试和修复

# 3. 合并到 main 并打 tag
git checkout main
git merge release/v1.0.0
git tag -a v1.0.0 -m "Release v1.0.0"

# 4. 合并回 develop
git checkout develop
git merge release/v1.0.0

# 5. 删除 release 分支
git branch -d release/v1.0.0
```

# 切图资源包

> A 股日报项目 | 版本：1.0 | 设计师：Agent_B ✨

---

## 📁 资源结构

```
assets/
├── icons/           # 图标资源
│   ├── tabbar/      # 底部导航图标
│   ├── navigation/  # 导航栏图标
│   └── functional/  # 功能图标
├── images/          # 图片资源
│   ├── placeholders/ # 占位图
│   └── backgrounds/  # 背景图
└── components/      # 组件切图
    ├── buttons/     # 按钮
    ├── cards/       # 卡片
    └── badges/      # 标签徽章
```

---

## 🎨 图标资源

### Tabbar 图标（24×24）

| 名称 | 状态 | 格式 | 说明 |
|------|------|------|------|
| ic_home_normal | 正常 | SVG/PNG | 首页 |
| ic_home_active | 选中 | SVG/PNG | 首页 - 选中态 `#1890FF` |
| ic_market_normal | 正常 | SVG/PNG | 行情 |
| ic_market_active | 选中 | SVG/PNG | 行情 - 选中态 |
| ic_ranking_normal | 正常 | SVG/PNG | 排行 |
| ic_ranking_active | 选中 | SVG/PNG | 排行 - 选中态 |
| ic_news_normal | 正常 | SVG/PNG | 资讯 |
| ic_news_active | 选中 | SVG/PNG | 资讯 - 选中态 |
| ic_profile_normal | 正常 | SVG/PNG | 我的 |
| ic_profile_active | 选中 | SVG/PNG | 我的 - 选中态 |

### 导航栏图标（24×24）

| 名称 | 格式 | 说明 |
|------|------|------|
| ic_search | SVG/PNG | 搜索 |
| ic_settings | SVG/PNG | 设置 |
| ic_back | SVG/PNG | 返回 |
| ic_close | SVG/PNG | 关闭 |
| ic_more | SVG/PNG | 更多 |

### 功能图标

| 名称 | 尺寸 | 格式 | 说明 |
|------|------|------|------|
| ic_star_empty | 24×24 | SVG | 收藏 - 空 |
| ic_star_filled | 24×24 | SVG | 收藏 - 实 |
| ic_share | 24×24 | SVG | 分享 |
| ic_arrow_up | 16×16 | SVG | 上涨箭头 `#C4161C` |
| ic_arrow_down | 16×16 | SVG | 下跌箭头 `#2BA540` |
| ic_lightning | 16×16 | SVG | 快讯 `#FAAD14` |
| ic_pin | 16×16 | SVG | 置顶 `#FAAD14` |
| ic_document | 16×16 | SVG | 公告 `#1890FF` |

---

## 🖼️ 图片资源

### 占位图

| 名称 | 尺寸 | 格式 | 说明 |
|------|------|------|------|
| placeholder_news | 100×100 | PNG | 新闻图片占位 |
| placeholder_avatar | 80×80 | PNG | 头像占位 |
| placeholder_chart | 320×200 | PNG | 图表占位 |

### 背景图

| 名称 | 尺寸 | 格式 | 说明 |
|------|------|------|------|
| bg_home_header | 375×120 | PNG | 首页头部渐变背景 |
| bg_loading | 200×200 | GIF | 加载动画 |

---

## 🧩 组件切图

### 按钮

| 名称 | 尺寸 | 状态 | 说明 |
|------|------|------|------|
| btn_primary_large | 343×48 | 正常/按下 | 主按钮 - 大 |
| btn_primary_medium | 163×40 | 正常/按下 | 主按钮 - 中 |
| btn_secondary_medium | 163×40 | 正常/按下 | 次按钮 - 中 |
| btn_buy | 163×56 | 正常/按下 | 买入按钮 `#C4161C` |
| btn_sell | 163×56 | 正常/按下 | 卖出按钮 `#2BA540` |

### 卡片

| 名称 | 尺寸 | 说明 |
|------|------|------|
| card_index | 343×120 | 指数卡片 |
| card_stock | 343×80 | 股票卡片 |
| card_news | 343×120 | 新闻卡片 |
| card_concept | 163×80 | 概念卡片 |

### 标签徽章

| 名称 | 尺寸 | 说明 |
|------|------|------|
| badge_rise | 48×20 | 上涨标签 `#C4161C` |
| badge_fall | 48×20 | 下跌标签 `#2BA540` |
| badge_new | 32×16 | 新标签 `#FAAD14` |
| badge_hot | 32×16 | 热标签 `#C4161C` |

---

## 📐 输出规范

### 多倍图输出

| 设备 | 倍率 | 目录 |
|------|------|------|
| @1x | 1x | 1x/ |
| @2x | 2x | 2x/ |
| @3x | 3x | 3x/ |

### 文件格式

- **图标**：优先 SVG，复杂图标用 PNG
- **图片**：PNG（无损）/ JPG（有损压缩）
- **动画**：GIF / Lottie JSON

### 命名规范

```
<类型>_<名称>_<状态>_<尺寸>.<格式>

示例：
- ic_home_active_24.svg
- btn_primary_normal_343x48.png
- bg_home_header_375x120.png
```

---

## 📥 下载说明

切图资源将由设计师通过以下方式交付：

1. **Figma/MasterGo** - 在线查看和导出
2. **蓝湖/摹客** - 标注和切图平台
3. **压缩包** - 完整资源包下载

---

*资源包状态：✅ 完成*

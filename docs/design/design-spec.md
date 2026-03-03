# A 股日报 - 设计规范文档

> 版本：1.0 | 更新日期：2026-03-03 | 设计师：Agent_B ✨

---

## 🎨 色彩系统

### 主色调

| 色值 | 用途 | 示例 |
|------|------|------|
| `#C4161C` | 上涨/红色 | 涨幅、阳线 |
| `#2BA540` | 下跌/绿色 | 跌幅、阴线 |
| `#1890FF` | 主品牌色 | 按钮、链接、高亮 |
| `#001529` | 深色背景 | 导航栏、卡片背景 |

### 中性色

| 色值 | 用途 |
|------|------|
| `#FFFFFF` | 白色背景 |
| `#F5F5F5` | 浅灰背景 |
| `#E8E8E8` | 分割线 |
| `#BFBFBF` | 次要文字 |
| `#595959` | 常规文字 |
| `#262626` | 主要标题 |

### 功能色

| 色值 | 用途 |
|------|------|
| `#FAAD14` | 警告/注意 |
| `#13C2C2` | 信息提示 |
| `#722ED1` | 特殊标记 |

---

## 📝 字体系统

### 中文字体

```css
font-family: -apple-system, "PingFang SC", "Microsoft YaHei", sans-serif;
```

### 英文字体

```css
font-family: -apple-system, "SF Pro Display", "Helvetica Neue", sans-serif;
```

### 数字字体（股价专用）

```css
font-family: "DIN Alternate", "Roboto Mono", monospace;
```

### 字号规范

| 级别 | 字号 | 行高 | 字重 | 用途 |
|------|------|------|------|------|
| H1 | 32px | 40px | Bold | 页面大标题 |
| H2 | 24px | 32px | Bold | 模块标题 |
| H3 | 18px | 28px | Medium | 小标题 |
| Body | 16px | 24px | Regular | 正文内容 |
| Caption | 14px | 20px | Regular | 辅助说明 |
| Small | 12px | 16px | Regular | 标签/时间戳 |

---

## 🧩 组件规范

### 按钮

| 类型 | 尺寸 | 高度 | 圆角 | 用途 |
|------|------|------|------|------|
| 主按钮 | Large | 48px | 8px | 核心操作 |
| 主按钮 | Medium | 40px | 6px | 常规操作 |
| 次按钮 | Medium | 40px | 6px | 次要操作 |
| 文字按钮 | - | - | - | 轻量操作 |

### 卡片

```css
padding: 16px;
border-radius: 12px;
background: #FFFFFF;
box-shadow: 0 2px 8px rgba(0,0,0,0.08);
```

### 列表项

```css
height: 72px;
padding: 16px;
border-bottom: 1px solid #E8E8E8;
```

### 输入框

```css
height: 44px;
border-radius: 8px;
border: 1px solid #D9D9D9;
padding: 0 12px;
```

---

## 📐 间距系统

采用 8px 基准网格：

- `4px` - 微间距
- `8px` - 小间距
- `16px` - 标准间距
- `24px` - 中间距
- `32px` - 大间距
- `48px` - 超大间距

---

## 📱 响应式断点

| 设备 | 宽度 | 说明 |
|------|------|------|
| Mobile S | 320px | 小屏手机 |
| Mobile M | 375px | 标准手机 |
| Mobile L | 414px | 大屏手机 |
| Tablet | 768px | 平板 |
| Desktop | 1024px+ | 桌面 |

---

## 🎯 设计原则

1. **清晰易读** - 股价数字使用等宽字体，确保对齐
2. **红涨绿跌** - 符合 A 股市场色彩习惯
3. **信息层级** - 重要数据突出显示
4. **操作便捷** - 核心功能一键触达

---

*设计规范持续迭代中...*

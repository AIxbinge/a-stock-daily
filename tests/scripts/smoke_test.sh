#!/bin/bash
# A 股日报 - 冒烟测试脚本
# 测试负责人：Agent_E

set -e

BASE_URL="${1:-http://localhost:8080}"
PASS_COUNT=0
FAIL_COUNT=0

echo "============================================================"
echo "🔍 A 股日报 - 冒烟测试"
echo "============================================================"
echo "🎯 测试目标：$BASE_URL"
echo ""

# 颜色定义
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 测试函数
test_api() {
    local name="$1"
    local url="$2"
    local expected_status="$3"
    
    start_time=$(date +%s%N)
    response=$(curl -s -o /dev/null -w "%{http_code}" "$url" --max-time 5 2>/dev/null || echo "000")
    end_time=$(date +%s%N)
    
    elapsed=$(( (end_time - start_time) / 1000000 ))
    
    if [ "$response" == "$expected_status" ]; then
        echo -e "${GREEN}✅${NC} [$name] 状态码：$response (${elapsed}ms)"
        PASS_COUNT=$((PASS_COUNT + 1))
    else
        echo -e "${RED}❌${NC} [$name] 期望：$expected_status, 实际：$response (${elapsed}ms)"
        FAIL_COUNT=$((FAIL_COUNT + 1))
    fi
}

# ==================== 冒烟测试用例 ====================

echo "【核心接口连通性测试】"
echo ""

# 大盘指数接口
test_api "大盘指数" "$BASE_URL/api/index" "200"

# 个股行情接口
test_api "个股行情 - 贵州茅台" "$BASE_URL/api/quote/600519" "200"
test_api "个股行情 - 五粮液" "$BASE_URL/api/quote/000858" "200"
test_api "个股行情 - 宁德时代" "$BASE_URL/api/quote/300750" "200"

# 排行榜接口
test_api "涨跌幅榜" "$BASE_URL/api/ranking/change_percent" "200"
test_api "成交量榜" "$BASE_URL/api/ranking/volume" "200"
test_api "换手率榜" "$BASE_URL/api/ranking/turnover_rate" "200"

# 搜索接口
test_api "搜索 - 茅台" "$BASE_URL/api/search?q=茅台" "200"

echo ""
echo "【异常场景测试】"
echo ""

# 无效股票代码
test_api "无效股票代码" "$BASE_URL/api/quote/999999" "404"

echo ""
echo "============================================================"
echo "📊 测试结果：通过 $PASS_COUNT | 失败 $FAIL_COUNT"
echo "============================================================"

if [ $FAIL_COUNT -eq 0 ]; then
    echo -e "${GREEN}✅ 冒烟测试通过！${NC}"
    exit 0
else
    echo -e "${RED}❌ 冒烟测试失败！${NC}"
    exit 1
fi

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A 股日报 - 接口自动化测试脚本
测试负责人：Agent_E
"""

import requests
import json
import time
from datetime import datetime

# 测试配置
BASE_URL = "http://localhost:8080"  # 待配置
TIMEOUT = 5

# 测试用例股票列表
TEST_STOCKS = [
    {"code": "600519", "name": "贵州茅台"},
    {"code": "000858", "name": "五粮液"},
    {"code": "300750", "name": "宁德时代"},
]

class StockAPITest:
    def __init__(self, base_url):
        self.base_url = base_url
        self.results = []
    
    def log(self, test_id, name, status, message="", response_time=None):
        result = {
            "test_id": test_id,
            "name": name,
            "status": status,
            "message": message,
            "response_time": response_time,
            "timestamp": datetime.now().isoformat()
        }
        self.results.append(result)
        status_icon = "✅" if status == "PASS" else "❌"
        time_str = f" ({response_time:.2f}ms)" if response_time else ""
        print(f"{status_icon} [{test_id}] {name}{time_str}")
        if message and status == "FAIL":
            print(f"   └─ {message}")
    
    # ==================== 连通性测试 ====================
    
    def test_index_api(self):
        """TC-API-002: 大盘指数接口"""
        start = time.time()
        try:
            resp = requests.get(f"{self.base_url}/api/index", timeout=TIMEOUT)
            elapsed = (time.time() - start) * 1000
            if resp.status_code == 200:
                data = resp.json()
                if "shanghai" in data or "shenzhen" in data:
                    self.log("TC-API-002", "大盘指数接口", "PASS", response_time=elapsed)
                else:
                    self.log("TC-API-002", "大盘指数接口", "FAIL", "返回数据缺少必要字段", elapsed)
            else:
                self.log("TC-API-002", "大盘指数接口", "FAIL", f"状态码：{resp.status_code}", elapsed)
        except Exception as e:
            self.log("TC-API-002", "大盘指数接口", "FAIL", str(e))
    
    def test_quote_api(self):
        """TC-API-001: 个股行情接口"""
        for stock in TEST_STOCKS:
            test_id = f"TC-API-001-{stock['code']}"
            start = time.time()
            try:
                resp = requests.get(f"{self.base_url}/api/quote/{stock['code']}", timeout=TIMEOUT)
                elapsed = (time.time() - start) * 1000
                if resp.status_code == 200:
                    data = resp.json()
                    required_fields = ["code", "name", "price", "change_percent"]
                    if all(field in data for field in required_fields):
                        self.log(test_id, f"个股行情接口-{stock['name']}", "PASS", response_time=elapsed)
                    else:
                        self.log(test_id, f"个股行情接口-{stock['name']}", "FAIL", "返回数据缺少必要字段", elapsed)
                else:
                    self.log(test_id, f"个股行情接口-{stock['name']}", "FAIL", f"状态码：{resp.status_code}", elapsed)
            except Exception as e:
                self.log(test_id, f"个股行情接口-{stock['name']}", "FAIL", str(e))
    
    def test_ranking_api(self):
        """TC-API-003: 排行榜接口"""
        ranking_types = [
            ("change_percent", "涨跌幅榜"),
            ("volume", "成交量榜"),
            ("turnover_rate", "换手率榜"),
        ]
        for rank_type, name in ranking_types:
            test_id = f"TC-API-003-{rank_type}"
            start = time.time()
            try:
                resp = requests.get(f"{self.base_url}/api/ranking/{rank_type}", timeout=TIMEOUT)
                elapsed = (time.time() - start) * 1000
                if resp.status_code == 200:
                    data = resp.json()
                    if isinstance(data, list) and len(data) > 0:
                        self.log(test_id, f"排行榜接口-{name}", "PASS", response_time=elapsed)
                    else:
                        self.log(test_id, f"排行榜接口-{name}", "FAIL", "返回数据格式错误", elapsed)
                else:
                    self.log(test_id, f"排行榜接口-{name}", "FAIL", f"状态码：{resp.status_code}", elapsed)
            except Exception as e:
                self.log(test_id, f"排行榜接口-{name}", "FAIL", str(e))
    
    def test_search_api(self):
        """TC-API-004: 搜索接口"""
        test_cases = [
            ("茅台", "搜索 - 茅台", True),
            ("600519", "搜索 - 代码", True),
            ("不存在的股票", "搜索 - 无结果", False),
        ]
        for keyword, name, should_have_results in test_cases:
            test_id = f"TC-API-004-{keyword[:10]}"
            start = time.time()
            try:
                resp = requests.get(f"{self.base_url}/api/search", params={"q": keyword}, timeout=TIMEOUT)
                elapsed = (time.time() - start) * 1000
                if resp.status_code == 200:
                    data = resp.json()
                    has_results = isinstance(data, list) and len(data) > 0
                    if has_results == should_have_results:
                        self.log(test_id, name, "PASS", response_time=elapsed)
                    else:
                        self.log(test_id, name, "FAIL", f"预期有结果={should_have_results}, 实际={has_results}", elapsed)
                else:
                    self.log(test_id, name, "FAIL", f"状态码：{resp.status_code}", elapsed)
            except Exception as e:
                self.log(test_id, name, "FAIL", str(e))
    
    # ==================== 异常场景测试 ====================
    
    def test_invalid_stock(self):
        """TC-API-008: 无效股票代码"""
        start = time.time()
        try:
            resp = requests.get(f"{self.base_url}/api/quote/999999", timeout=TIMEOUT)
            elapsed = (time.time() - start) * 1000
            if resp.status_code in [404, 400]:
                self.log("TC-API-008", "无效股票代码", "PASS", response_time=elapsed)
            elif resp.status_code == 200:
                data = resp.json()
                if "error" in data:
                    self.log("TC-API-008", "无效股票代码", "PASS", response_time=elapsed)
                else:
                    self.log("TC-API-008", "无效股票代码", "FAIL", "应返回错误信息", elapsed)
            else:
                self.log("TC-API-008", "无效股票代码", "FAIL", f"状态码：{resp.status_code}", elapsed)
        except Exception as e:
            self.log("TC-API-008", "无效股票代码", "FAIL", str(e))
    
    def test_missing_params(self):
        """TC-API-009: 参数缺失"""
        start = time.time()
        try:
            resp = requests.get(f"{self.base_url}/api/quote", timeout=TIMEOUT)
            elapsed = (time.time() - start) * 1000
            if resp.status_code == 400:
                self.log("TC-API-009", "参数缺失", "PASS", response_time=elapsed)
            else:
                self.log("TC-API-009", "参数缺失", "FAIL", f"预期 400, 实际：{resp.status_code}", elapsed)
        except Exception as e:
            self.log("TC-API-009", "参数缺失", "FAIL", str(e))
    
    # ==================== 性能测试 ====================
    
    def test_response_time(self):
        """TC-API-012: 接口响应时间"""
        endpoints = [
            "/api/index",
            "/api/quote/600519",
            "/api/ranking/change_percent",
        ]
        for endpoint in endpoints:
            times = []
            for i in range(10):
                start = time.time()
                try:
                    requests.get(f"{self.base_url}{endpoint}", timeout=TIMEOUT)
                    elapsed = (time.time() - start) * 1000
                    times.append(elapsed)
                except:
                    pass
            if times:
                avg = sum(times) / len(times)
                p95 = sorted(times)[int(len(times) * 0.95)] if len(times) >= 20 else max(times)
                status = "PASS" if avg < 500 else "WARN"
                self.log(f"TC-API-012-{endpoint}", f"响应时间-{endpoint}", status, f"平均:{avg:.2f}ms, P95:{p95:.2f}ms")
    
    # ==================== 运行所有测试 ====================
    
    def run_all(self):
        print("\n" + "="*60)
        print("🔍 A 股日报 - 接口自动化测试")
        print("="*60 + "\n")
        
        print("【连通性测试】")
        self.test_index_api()
        self.test_quote_api()
        self.test_ranking_api()
        self.test_search_api()
        
        print("\n【异常场景测试】")
        self.test_invalid_stock()
        self.test_missing_params()
        
        print("\n【性能测试】")
        self.test_response_time()
        
        # 输出统计
        total = len(self.results)
        passed = sum(1 for r in self.results if r["status"] == "PASS")
        failed = sum(1 for r in self.results if r["status"] == "FAIL")
        
        print("\n" + "="*60)
        print(f"📊 测试完成：总计 {total} | ✅ 通过 {passed} | ❌ 失败 {failed}")
        print("="*60 + "\n")
        
        return passed == total


if __name__ == "__main__":
    import sys
    base_url = sys.argv[1] if len(sys.argv) > 1 else BASE_URL
    print(f"🎯 测试目标：{base_url}\n")
    
    tester = StockAPITest(base_url)
    success = tester.run_all()
    
    # 保存报告
    report_path = "reports/api_test_report.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(tester.results, f, ensure_ascii=False, indent=2)
    print(f"📄 报告已保存：{report_path}\n")
    
    sys.exit(0 if success else 1)

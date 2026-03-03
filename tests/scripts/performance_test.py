#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A 股日报 - 性能测试脚本
测试负责人：Agent_E
"""

import requests
import time
import threading
import statistics
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

# 测试配置
BASE_URL = "http://localhost:8080"
TEST_STOCK = "600519"

class PerformanceTest:
    def __init__(self, base_url):
        self.base_url = base_url
        self.results = []
        self.lock = threading.Lock()
    
    def single_request(self, endpoint):
        """单次请求"""
        start = time.time()
        try:
            resp = requests.get(f"{self.base_url}{endpoint}", timeout=10)
            elapsed = (time.time() - start) * 1000
            return {
                "status": resp.status_code,
                "time": elapsed,
                "success": resp.status_code == 200
            }
        except Exception as e:
            return {
                "status": 0,
                "time": (time.time() - start) * 1000,
                "success": False,
                "error": str(e)
            }
    
    def concurrent_test(self, endpoint, concurrency, duration_seconds):
        """并发测试"""
        print(f"\n📈 并发测试：{endpoint} | 并发数：{concurrency} | 持续时间：{duration_seconds}s")
        
        results = []
        stop_time = time.time() + duration_seconds
        request_count = [0]
        error_count = [0]
        
        def worker():
            while time.time() < stop_time:
                result = self.single_request(endpoint)
                with self.lock:
                    results.append(result)
                    request_count[0] += 1
                    if not result["success"]:
                        error_count[0] += 1
        
        # 启动并发线程
        threads = []
        for _ in range(concurrency):
            t = threading.Thread(target=worker)
            t.start()
            threads.append(t)
        
        # 等待完成
        for t in threads:
            t.join()
        
        # 统计结果
        success_times = [r["time"] for r in results if r["success"]]
        if success_times:
            avg_time = statistics.mean(success_times)
            p95_time = sorted(success_times)[int(len(success_times) * 0.95)]
            p99_time = sorted(success_times)[int(len(success_times) * 0.99)]
            qps = request_count[0] / duration_seconds
            error_rate = (error_count[0] / request_count[0]) * 100 if request_count[0] > 0 else 0
            
            print(f"   请求总数：{request_count[0]}")
            print(f"   QPS: {qps:.2f}")
            print(f"   平均响应：{avg_time:.2f}ms")
            print(f"   P95 响应：{p95_time:.2f}ms")
            print(f"   P99 响应：{p99_time:.2f}ms")
            print(f"   错误率：{error_rate:.2f}%")
            
            return {
                "endpoint": endpoint,
                "concurrency": concurrency,
                "duration": duration_seconds,
                "total_requests": request_count[0],
                "qps": qps,
                "avg_time": avg_time,
                "p95_time": p95_time,
                "p99_time": p99_time,
                "error_rate": error_rate,
                "success": error_rate < 1
            }
        else:
            print(f"   ❌ 无成功请求")
            return None
    
    def run_load_test(self):
        """负载测试"""
        print("\n" + "="*60)
        print("🚀 A 股日报 - 负载测试")
        print("="*60)
        
        test_cases = [
            (10, 300, "/api/quote/600519"),   # 10 并发，5 分钟
            (50, 600, "/api/quote/600519"),   # 50 并发，10 分钟
            (100, 900, "/api/quote/600519"),  # 100 并发，15 分钟
        ]
        
        results = []
        for concurrency, duration, endpoint in test_cases:
            result = self.concurrent_test(endpoint, concurrency, duration)
            if result:
                results.append(result)
        
        return results
    
    def run_stress_test(self):
        """压力测试 - 找到系统瓶颈"""
        print("\n" + "="*60)
        print("💥 A 股日报 - 压力测试")
        print("="*60)
        
        endpoint = "/api/quote/600519"
        concurrency_levels = [50, 100, 200, 500, 1000]
        
        for concurrency in concurrency_levels:
            print(f"\n测试并发数：{concurrency}")
            result = self.concurrent_test(endpoint, concurrency, 60)
            if result and result["error_rate"] > 5:
                print(f"⚠️  错误率超过 5%，停止测试")
                break
            time.sleep(5)  # 冷却时间
    
    def run_baseline_test(self):
        """基准测试 - 单次请求性能"""
        print("\n" + "="*60)
        print("📏 A 股日报 - 基准测试")
        print("="*60)
        
        endpoints = [
            "/api/index",
            "/api/quote/600519",
            "/api/ranking/change_percent",
            "/api/search?q=茅台",
        ]
        
        results = []
        for endpoint in endpoints:
            times = []
            print(f"\n测试接口：{endpoint}")
            
            for i in range(100):
                result = self.single_request(endpoint)
                if result["success"]:
                    times.append(result["time"])
            
            if times:
                avg = statistics.mean(times)
                p95 = sorted(times)[95]
                p99 = sorted(times)[99]
                min_t = min(times)
                max_t = max(times)
                
                print(f"   平均：{avg:.2f}ms | P95: {p95:.2f}ms | P99: {p99:.2f}ms")
                print(f"   最小：{min_t:.2f}ms | 最大：{max_t:.2f}ms")
                
                results.append({
                    "endpoint": endpoint,
                    "avg": avg,
                    "p95": p95,
                    "p99": p99,
                    "min": min_t,
                    "max": max_t,
                    "pass": p95 < 500
                })
        
        return results
    
    def run_all(self):
        """运行所有性能测试"""
        print("\n" + "="*60)
        print("🔍 A 股日报 - 性能测试套件")
        print("测试负责人：Agent_E")
        print("="*60)
        print(f"🎯 测试目标：{self.base_url}")
        
        # 基准测试
        baseline_results = self.run_baseline_test()
        
        # 负载测试（可选，耗时较长）
        # load_results = self.run_load_test()
        
        # 压力测试（可选，可能影响服务）
        # stress_results = self.run_stress_test()
        
        print("\n" + "="*60)
        print("📊 性能测试完成")
        print("="*60 + "\n")
        
        return baseline_results


if __name__ == "__main__":
    import sys
    import json
    
    base_url = sys.argv[1] if len(sys.argv) > 1 else BASE_URL
    
    tester = PerformanceTest(base_url)
    results = tester.run_all()
    
    # 保存报告
    report = {
        "timestamp": datetime.now().isoformat(),
        "base_url": base_url,
        "results": results
    }
    
    report_path = "reports/performance_test_report.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"📄 报告已保存：{report_path}\n")

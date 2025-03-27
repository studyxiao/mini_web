#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
比较 os.scandir 和 os.listdir 的效率测试
"""
import os
import time
import statistics
from pathlib import Path


def test_listdir(directory, iterations=1000):
    """测试 os.listdir 的执行时间"""
    start_time = time.perf_counter()
    
    for _ in range(iterations):
        entries = os.listdir(directory)
        # 模拟对每个文件名进行一些基本处理
        for entry in entries:
            path = os.path.join(directory, entry)
            is_dir = os.path.isdir(path)
            is_file = os.path.isfile(path)
            name = os.path.basename(path)
    
    end_time = time.perf_counter()
    return end_time - start_time


def test_scandir(directory, iterations=1000):
    """测试 os.scandir 的执行时间"""
    start_time = time.perf_counter()
    
    for _ in range(iterations):
        with os.scandir(directory) as entries:
            # 使用 scandir 获取文件信息不需要额外调用 os.path 方法
            for entry in entries:
                is_dir = entry.is_dir()
                is_file = entry.is_file()
                name = entry.name
    
    end_time = time.perf_counter()
    return end_time - start_time


def run_benchmark(directory_path, iterations=1000, runs=5):
    """运行多次测试并统计结果"""
    listdir_times = []
    scandir_times = []
    
    print(f"开始测试目录: {directory_path}")
    print(f"每次测试迭代 {iterations} 次，共运行 {runs} 次测试\n")
    
    for i in range(runs):
        print(f"运行测试 {i+1}/{runs}")
        
        # 测试 listdir
        listdir_time = test_listdir(directory_path, iterations)
        listdir_times.append(listdir_time)
        print(f"os.listdir  耗时: {listdir_time:.6f} 秒")
        
        # 测试 scandir
        scandir_time = test_scandir(directory_path, iterations)
        scandir_times.append(scandir_time)
        print(f"os.scandir 耗时: {scandir_time:.6f} 秒")
        
        # 计算性能差异
        diff_percent = (listdir_time - scandir_time) / listdir_time * 100
        print(f"scandir 比 listdir 快了 {diff_percent:.2f}%\n")
    
    # 计算平均值和中位数
    avg_listdir = statistics.mean(listdir_times)
    avg_scandir = statistics.mean(scandir_times)
    med_listdir = statistics.median(listdir_times)
    med_scandir = statistics.median(scandir_times)
    
    print("\n====== 测试结果汇总 ======")
    print(f"os.listdir  平均耗时: {avg_listdir:.6f} 秒, 中位数: {med_listdir:.6f} 秒")
    print(f"os.scandir 平均耗时: {avg_scandir:.6f} 秒, 中位数: {med_scandir:.6f} 秒")
    
    avg_diff_percent = (avg_listdir - avg_scandir) / avg_listdir * 100
    print(f"平均而言，scandir 比 listdir 快了 {avg_diff_percent:.2f}%")


if __name__ == "__main__":
    # 测试不同类型的目录
    test_dirs = [
        os.path.dirname(os.path.abspath(__file__)),  # 当前目录
        os.path.expanduser("~"),                     # 用户主目录
        "/tmp" if os.name != "nt" else "C:\\Windows\\Temp",  # 临时目录
    ]
    
    for directory in test_dirs:
        try:
            print("\n" + "="*60)
            print(f"测试目录: {directory}")
            print("="*60)
            # 获取目录中文件数量
            file_count = len(os.listdir(directory))
            print(f"目录中文件数量: {file_count}")
            
            # 根据文件数量调整迭代次数
            if file_count > 1000:
                iterations = 100
            elif file_count > 100:
                iterations = 500
            else:
                iterations = 1000
                
            run_benchmark(directory, iterations=iterations, runs=3)
        except PermissionError:
            print(f"无法访问目录: {directory}，权限被拒绝")
        except Exception as e:
            print(f"测试目录 {directory} 时出错: {e}")
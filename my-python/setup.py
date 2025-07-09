#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
项目初始化脚本
快速设置 Python 爬虫项目环境
"""

import os
import subprocess
import sys

def run_command(command, description):
    """执行命令并显示进度"""
    print(f"正在{description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✓ {description}成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description}失败: {e}")
        return False

def check_python():
    """检查 Python 环境"""
    print("检查 Python 环境...")
    # 尝试 python3 命令
    try:
        result = subprocess.run(['python3', '--version'], capture_output=True, text=True)
        print(f"✓ Python 版本: {result.stdout.strip()}")
        return True
    except FileNotFoundError:
        # 尝试 python 命令
        try:
            result = subprocess.run(['python', '--version'], capture_output=True, text=True)
            print(f"✓ Python 版本: {result.stdout.strip()}")
            return True
        except FileNotFoundError:
            print("✗ 未找到 Python，请先安装 Python")
            return False

def create_virtual_env():
    """创建虚拟环境"""
    if os.path.exists('venv'):
        print("✓ 虚拟环境已存在")
        return True
    
    # 尝试使用 python3 创建虚拟环境
    try:
        result = subprocess.run(['python3', '-m', 'venv', 'venv'], check=True, capture_output=True, text=True)
        print("✓ 创建虚拟环境成功")
        return True
    except subprocess.CalledProcessError:
        # 如果 python3 失败，尝试 python
        return run_command('python -m venv venv', '创建虚拟环境')

def install_dependencies():
    """安装依赖包"""
    # 激活虚拟环境并安装依赖
    if os.name == 'nt':  # Windows
        activate_cmd = 'venv\\Scripts\\activate && pip install -r requirements.txt'
    else:  # macOS/Linux
        activate_cmd = 'source venv/bin/activate && pip install -r requirements.txt'
    
    return run_command(activate_cmd, '安装依赖包')

def verify_installation():
    """验证安装"""
    print("验证安装...")
    try:
        # 测试导入所有依赖包
        test_script = '''
import requests
import bs4
import openpyxl
print("✓ 所有依赖包安装成功！")
'''
        result = subprocess.run([sys.executable, '-c', test_script], capture_output=True, text=True)
        print(result.stdout.strip())
        return True
    except Exception as e:
        print(f"✗ 验证失败: {e}")
        return False

def main():
    """主函数"""
    print("=" * 50)
    print("Python 爬虫项目初始化")
    print("=" * 50)
    
    # 检查 Python 环境
    if not check_python():
        return False
    
    # 创建虚拟环境
    if not create_virtual_env():
        return False
    
    # 安装依赖
    if not install_dependencies():
        return False
    
    # 验证安装
    if not verify_installation():
        return False
    
    print("\n" + "=" * 50)
    print("项目初始化完成！")
    print("=" * 50)
    print("下一步操作：")
    print("1. 激活虚拟环境：")
    if os.name == 'nt':
        print("   venv\\Scripts\\activate")
    else:
        print("   source venv/bin/activate")
    print("2. 运行爬虫：")
    print("   python douban_top250.py")
    print("=" * 50)
    
    return True

if __name__ == "__main__":
    main() 
#!/bin/bash

echo "🚀 Python 爬虫项目启动脚本"
echo "================================"

# 检测 Python 命令
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
    PIP_CMD="pip3"
    echo "✓ 使用 python3 命令"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
    PIP_CMD="pip"
    echo "✓ 使用 python 命令"
else
    echo "❌ 未找到 Python，请先安装 Python"
    exit 1
fi

# 检查虚拟环境是否存在
if [ ! -d "venv" ]; then
    echo "📦 创建虚拟环境..."
    $PYTHON_CMD -m venv venv
fi

# 激活虚拟环境
echo "🔧 激活虚拟环境..."
source venv/bin/activate

echo "📦 安装依赖包..."
pip install -r requirements.txt

echo "🔧 验证安装..."
python -c "import requests, bs4, openpyxl; print('✅ 所有依赖包安装成功！')"

echo "🕷️ 开始运行爬虫..."
python douban_top250.py

echo "🎉 完成！请查看生成的 douban_top250.xlsx 文件" 
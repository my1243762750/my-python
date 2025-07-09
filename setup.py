#!/usr/bin/env python3
"""
节奏视频剪辑器安装脚本
"""

import subprocess
import sys
import os
import platform

def check_python_version():
    """检查Python版本"""
    if sys.version_info < (3, 7):
        print("❌ 错误: 需要Python 3.7或更高版本")
        print(f"当前版本: {sys.version}")
        return False
    print(f"✅ Python版本检查通过: {sys.version}")
    return True

def install_requirements():
    """安装依赖包"""
    print("📦 安装依赖包...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ 依赖包安装成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 依赖包安装失败: {e}")
        return False

def check_ffmpeg():
    """检查FFmpeg是否安装"""
    try:
        result = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ FFmpeg已安装")
            return True
        else:
            print("❌ FFmpeg未安装或不可用")
            return False
    except FileNotFoundError:
        print("❌ FFmpeg未安装")
        return False

def install_ffmpeg():
    """安装FFmpeg"""
    system = platform.system().lower()
    
    print("🔧 安装FFmpeg...")
    
    if system == "darwin":  # macOS
        try:
            subprocess.check_call(["brew", "install", "ffmpeg"])
            print("✅ FFmpeg安装成功 (macOS)")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ 请手动安装FFmpeg:")
            print("   1. 安装Homebrew: https://brew.sh/")
            print("   2. 运行: brew install ffmpeg")
            return False
    
    elif system == "linux":
        print("❌ 请手动安装FFmpeg:")
        print("   Ubuntu/Debian: sudo apt-get install ffmpeg")
        print("   CentOS/RHEL: sudo yum install ffmpeg")
        return False
    
    elif system == "windows":
        print("❌ 请手动安装FFmpeg:")
        print("   1. 下载: https://ffmpeg.org/download.html")
        print("   2. 添加到系统PATH")
        return False
    
    else:
        print(f"❌ 不支持的操作系统: {system}")
        return False

def create_directories():
    """创建必要的目录"""
    directories = ["audio_files", "video_files", "output"]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✅ 创建目录: {directory}")
        else:
            print(f"📁 目录已存在: {directory}")

def test_imports():
    """测试关键模块导入"""
    print("🧪 测试模块导入...")
    
    modules = [
        ("librosa", "音频处理"),
        ("moviepy", "视频处理"),
        ("cv2", "计算机视觉"),
        ("numpy", "数值计算"),
        ("scipy", "科学计算")
    ]
    
    all_success = True
    
    for module_name, description in modules:
        try:
            __import__(module_name)
            print(f"✅ {module_name} ({description})")
        except ImportError as e:
            print(f"❌ {module_name} ({description}): {e}")
            all_success = False
    
    return all_success

def main():
    """主安装流程"""
    print("🎬 节奏视频剪辑器 - 安装脚本")
    print("=" * 50)
    
    # 检查Python版本
    if not check_python_version():
        return
    
    # 创建目录
    create_directories()
    
    # 安装依赖包
    if not install_requirements():
        print("❌ 安装失败，请检查网络连接或手动安装依赖")
        return
    
    # 测试模块导入
    if not test_imports():
        print("❌ 模块导入测试失败，请检查安装")
        return
    
    # 检查FFmpeg
    if not check_ffmpeg():
        print("⚠️  FFmpeg未安装，尝试自动安装...")
        if not install_ffmpeg():
            print("⚠️  FFmpeg安装失败，某些功能可能不可用")
    
    print("\n🎉 安装完成！")
    print("\n📋 下一步:")
    print("1. 将音频文件放在 audio_files 目录中")
    print("2. 将视频文件放在 video_files 目录中")
    print("3. 运行: python example.py")
    print("\n📖 详细说明请查看 README.md")

if __name__ == "__main__":
    main() 
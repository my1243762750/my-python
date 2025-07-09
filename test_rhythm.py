#!/usr/bin/env python3
"""
节奏视频剪辑器测试脚本
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from rhythm_video_editor import RhythmVideoEditor

def test_audio_analysis():
    """测试音频分析功能"""
    print("🎵 测试音频分析功能...")
    
    # 检查是否有音频文件
    audio_files = []
    if os.path.exists("audio_files"):
        for file in os.listdir("audio_files"):
            if file.lower().endswith(('.mp3', '.wav', '.m4a', '.flac', '.ogg')):
                audio_files.append(os.path.join("audio_files", file))
    
    if not audio_files:
        print("❌ 没有找到音频文件")
        print("请将音频文件放在 audio_files 目录中")
        return False
    
    # 测试第一个音频文件
    audio_path = audio_files[0]
    print(f"📁 测试音频文件: {audio_path}")
    
    try:
        # 创建编辑器实例
        editor = RhythmVideoEditor(audio_path, "video_files", "output/test.mp4")
        
        # 分析音频节奏
        beat_times = editor.analyze_audio_rhythm()
        
        if not beat_times:
            print("❌ 没有检测到节奏点")
            return False
        
        print(f"✅ 检测到 {len(beat_times)} 个节奏点")
        print(f"🎵 音乐时长: {beat_times[-1]:.2f} 秒")
        print(f"📊 平均节奏间隔: {np.mean(np.diff(beat_times)):.2f} 秒")
        
        # 显示前10个节奏点
        print("\n前10个节奏点:")
        for i, time in enumerate(beat_times[:10]):
            print(f"  {i+1:2d}. {time:6.2f}秒")
        
        return True
        
    except Exception as e:
        print(f"❌ 音频分析失败: {e}")
        return False

def test_video_loading():
    """测试视频加载功能"""
    print("\n🎬 测试视频加载功能...")
    
    # 检查是否有视频文件
    video_files = []
    if os.path.exists("video_files"):
        for file in os.listdir("video_files"):
            if file.lower().endswith(('.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv')):
                video_files.append(os.path.join("video_files", file))
    
    if not video_files:
        print("❌ 没有找到视频文件")
        print("请将视频文件放在 video_files 目录中")
        return False
    
    print(f"✅ 找到 {len(video_files)} 个视频文件")
    
    # 测试动态分数计算
    try:
        editor = RhythmVideoEditor("audio_files/test.mp3", "video_files", "output/test.mp4")
        
        print("\n📊 视频动态分数:")
        for video_path in video_files[:5]:  # 只测试前5个
            score = editor.calculate_video_dynamic_score(video_path)
            filename = os.path.basename(video_path)
            print(f"  {filename}: {score:.2f}")
        
        return True
        
    except Exception as e:
        print(f"❌ 视频分析失败: {e}")
        return False

def create_test_audio():
    """创建测试音频文件（如果不存在）"""
    if not os.path.exists("audio_files"):
        os.makedirs("audio_files")
    
    # 检查是否已有音频文件
    audio_files = []
    if os.path.exists("audio_files"):
        for file in os.listdir("audio_files"):
            if file.lower().endswith(('.mp3', '.wav', '.m4a', '.flac', '.ogg')):
                audio_files.append(file)
    
    if audio_files:
        print(f"✅ 发现音频文件: {audio_files[0]}")
        return True
    
    print("⚠️  没有找到音频文件")
    print("请将音频文件放在 audio_files 目录中")
    return False

def main():
    """主测试流程"""
    print("🧪 节奏视频剪辑器 - 测试脚本")
    print("=" * 50)
    
    # 检查目录结构
    print("📁 检查目录结构...")
    for directory in ["audio_files", "video_files", "output"]:
        if os.path.exists(directory):
            file_count = len(os.listdir(directory))
            print(f"  {directory}/: {file_count} 个文件")
        else:
            print(f"  {directory}/: 目录不存在")
    
    # 创建测试音频
    if not create_test_audio():
        return
    
    # 测试音频分析
    audio_success = test_audio_analysis()
    
    # 测试视频加载
    video_success = test_video_loading()
    
    print("\n" + "=" * 50)
    print("📊 测试结果:")
    print(f"  音频分析: {'✅ 通过' if audio_success else '❌ 失败'}")
    print(f"  视频加载: {'✅ 通过' if video_success else '❌ 失败'}")
    
    if audio_success and video_success:
        print("\n🎉 所有测试通过！可以开始使用节奏视频剪辑器了。")
        print("\n📋 下一步:")
        print("1. 运行: python example.py")
        print("2. 或运行: python rhythm_video_editor.py")
    else:
        print("\n⚠️  部分测试失败，请检查文件和环境配置。")

if __name__ == "__main__":
    main() 
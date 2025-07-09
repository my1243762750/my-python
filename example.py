#!/usr/bin/env python3
"""
节奏视频剪辑器使用示例
"""

import os
from rhythm_video_editor import RhythmVideoEditor

def create_rhythm_video_example():
    """
    创建节奏视频的示例
    """
    # 配置路径
    audio_path = "audio_files/music.mp3"  # 音频文件路径
    video_dir = "video_files"  # 视频文件目录
    output_path = "output/rhythm_video.mp4"  # 输出文件路径
    
    # 检查文件是否存在
    if not os.path.exists(audio_path):
        print(f"❌ 错误: 音频文件不存在: {audio_path}")
        print("请将音频文件放在 audio_files 目录中")
        return False
    
    if not os.path.exists(video_dir) or not os.listdir(video_dir):
        print(f"❌ 错误: 视频目录为空: {video_dir}")
        print("请将视频文件放在 video_files 目录中")
        return False
    
    print("🎵 开始创建节奏视频...")
    
    # 创建编辑器实例
    editor = RhythmVideoEditor(audio_path, video_dir, output_path)
    
    try:
        # 创建节奏视频
        output_file = editor.create_rhythm_video(segment_duration=1.0)
        print(f"✅ 视频创建成功: {output_file}")
        return True
    except Exception as e:
        print(f"❌ 创建视频时出错: {e}")
        return False

def analyze_audio_only():
    """
    仅分析音频节奏的示例
    """
    audio_path = "audio_files/music.mp3"
    
    if not os.path.exists(audio_path):
        print(f"❌ 错误: 音频文件不存在: {audio_path}")
        return
    
    print("🎵 分析音频节奏...")
    
    editor = RhythmVideoEditor(audio_path, "video_files", "output/temp.mp4")
    beat_times = editor.analyze_audio_rhythm()
    
    print(f"📊 检测到 {len(beat_times)} 个节奏点")
    print("前10个节奏点时间:")
    for i, time in enumerate(beat_times[:10]):
        print(f"  {i+1}. {time:.2f}秒")

if __name__ == "__main__":
    print("🎬 节奏视频剪辑器")
    print("=" * 50)
    
    # 检查目录结构
    print("📁 检查目录结构...")
    if not os.path.exists("audio_files"):
        os.makedirs("audio_files")
        print("✅ 创建 audio_files 目录")
    
    if not os.path.exists("video_files"):
        os.makedirs("video_files")
        print("✅ 创建 video_files 目录")
    
    if not os.path.exists("output"):
        os.makedirs("output")
        print("✅ 创建 output 目录")
    
    print("\n📋 使用说明:")
    print("1. 将音频文件放在 audio_files 目录中")
    print("2. 将视频文件放在 video_files 目录中")
    print("3. 运行此脚本创建节奏视频")
    
    # 尝试分析音频
    if os.path.exists("audio_files") and any(f.endswith(('.mp3', '.wav', '.m4a')) for f in os.listdir("audio_files")):
        print("\n🎵 检测到音频文件，开始分析...")
        analyze_audio_only()
    
    # 尝试创建视频
    print("\n🎬 尝试创建节奏视频...")
    success = create_rhythm_video_example()
    
    if success:
        print("\n🎉 完成！请查看 output 目录中的结果文件。")
    else:
        print("\n💡 请确保已安装所需依赖并放入音频和视频文件。") 
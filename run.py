#!/usr/bin/env python3
"""
节奏视频剪辑器 - 快速启动脚本
"""

import os
import sys
import argparse
from rhythm_video_editor import RhythmVideoEditor

def check_files():
    """检查必要文件是否存在"""
    issues = []
    
    # 检查音频文件
    if not os.path.exists("audio_files"):
        issues.append("audio_files 目录不存在")
    else:
        audio_files = [f for f in os.listdir("audio_files") 
                      if f.lower().endswith(('.mp3', '.wav', '.m4a', '.flac', '.ogg'))]
        if not audio_files:
            issues.append("audio_files 目录中没有音频文件")
    
    # 检查视频文件
    if not os.path.exists("video_files"):
        issues.append("video_files 目录不存在")
    else:
        video_files = [f for f in os.listdir("video_files") 
                      if f.lower().endswith(('.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv'))]
        if not video_files:
            issues.append("video_files 目录中没有视频文件")
    
    return issues

def list_files():
    """列出可用的音频和视频文件"""
    print("📁 可用文件:")
    
    # 音频文件
    if os.path.exists("audio_files"):
        audio_files = [f for f in os.listdir("audio_files") 
                      if f.lower().endswith(('.mp3', '.wav', '.m4a', '.flac', '.ogg'))]
        if audio_files:
            print(f"  🎵 音频文件 ({len(audio_files)}个):")
            for file in audio_files:
                print(f"    - {file}")
        else:
            print("  🎵 音频文件: 无")
    else:
        print("  🎵 音频文件: audio_files 目录不存在")
    
    # 视频文件
    if os.path.exists("video_files"):
        video_files = [f for f in os.listdir("video_files") 
                      if f.lower().endswith(('.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv'))]
        if video_files:
            print(f"  🎬 视频文件 ({len(video_files)}个):")
            for file in video_files[:10]:  # 只显示前10个
                print(f"    - {file}")
            if len(video_files) > 10:
                print(f"    ... 还有 {len(video_files) - 10} 个文件")
        else:
            print("  🎬 视频文件: 无")
    else:
        print("  🎬 视频文件: video_files 目录不存在")

def create_video(audio_file=None, segment_duration=1.0, output_name="rhythm_video.mp4"):
    """创建节奏视频"""
    
    # 确定音频文件
    if not audio_file:
        if os.path.exists("audio_files"):
            audio_files = [f for f in os.listdir("audio_files") 
                          if f.lower().endswith(('.mp3', '.wav', '.m4a', '.flac', '.ogg'))]
            if audio_files:
                audio_file = os.path.join("audio_files", audio_files[0])
            else:
                print("❌ 没有找到音频文件")
                return False
        else:
            print("❌ audio_files 目录不存在")
            return False
    
    # 检查输出目录
    if not os.path.exists("output"):
        os.makedirs("output")
    
    output_path = os.path.join("output", output_name)
    
    print(f"🎵 音频文件: {audio_file}")
    print(f"🎬 视频目录: video_files")
    print(f"📁 输出文件: {output_path}")
    print(f"⏱️  片段时长: {segment_duration}秒")
    
    try:
        # 创建编辑器实例
        editor = RhythmVideoEditor(audio_file, "video_files", output_path)
        
        # 创建节奏视频
        result_file = editor.create_rhythm_video(segment_duration=segment_duration)
        
        print(f"✅ 视频创建成功: {result_file}")
        return True
        
    except Exception as e:
        print(f"❌ 创建视频失败: {e}")
        return False

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="节奏视频剪辑器")
    parser.add_argument("--list", action="store_true", help="列出可用文件")
    parser.add_argument("--audio", type=str, help="指定音频文件路径")
    parser.add_argument("--duration", type=float, default=1.0, help="视频片段时长（秒）")
    parser.add_argument("--output", type=str, default="rhythm_video.mp4", help="输出文件名")
    parser.add_argument("--check", action="store_true", help="检查环境")
    
    args = parser.parse_args()
    
    print("🎬 节奏视频剪辑器")
    print("=" * 50)
    
    # 检查环境
    if args.check:
        print("🔍 检查环境...")
        issues = check_files()
        if issues:
            print("❌ 发现问题:")
            for issue in issues:
                print(f"  - {issue}")
            print("\n💡 请确保:")
            print("  1. 将音频文件放在 audio_files 目录中")
            print("  2. 将视频文件放在 video_files 目录中")
            return
        else:
            print("✅ 环境检查通过")
            return
    
    # 列出文件
    if args.list:
        list_files()
        return
    
    # 检查文件
    issues = check_files()
    if issues:
        print("❌ 发现问题:")
        for issue in issues:
            print(f"  - {issue}")
        print("\n💡 请确保:")
        print("  1. 将音频文件放在 audio_files 目录中")
        print("  2. 将视频文件放在 video_files 目录中")
        return
    
    # 创建视频
    print("🚀 开始创建节奏视频...")
    success = create_video(args.audio, args.duration, args.output)
    
    if success:
        print("\n🎉 完成！")
        print(f"📁 输出文件: output/{args.output}")
    else:
        print("\n❌ 创建失败，请检查错误信息")

if __name__ == "__main__":
    main() 
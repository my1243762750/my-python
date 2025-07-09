import os
import librosa
import numpy as np
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips
from scipy.signal import find_peaks
import cv2
from tqdm import tqdm
import random
from typing import List, Tuple, Optional
import logging

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class RhythmVideoEditor:
    def __init__(self, audio_path: str, video_dir: str, output_path: str):
        """
        初始化节奏视频编辑器
        
        Args:
            audio_path: 音频文件路径
            video_dir: 视频文件目录
            output_path: 输出文件路径
        """
        self.audio_path = audio_path
        self.video_dir = video_dir
        self.output_path = output_path
        self.beat_times = []
        self.video_clips = []
        self.audio_clip = None
        
    def analyze_audio_rhythm(self, hop_length: int = 512, sr: int = 22050) -> List[float]:
        """
        分析音频节奏，提取节拍时间点
        
        Args:
            hop_length: 音频分析步长
            sr: 采样率
            
        Returns:
            节拍时间点列表（秒）
        """
        logger.info("开始分析音频节奏...")
        
        # 加载音频文件
        y, sr = librosa.load(self.audio_path, sr=sr)
        
        # 提取节拍
        tempo, beats = librosa.beat.beat_track(y=y, sr=sr, hop_length=hop_length)
        
        # 将节拍帧转换为时间
        beat_times = librosa.frames_to_time(beats, sr=sr, hop_length=hop_length)
        
        # 提取onset（音频起始点）
        onset_frames = librosa.onset.onset_detect(y=y, sr=sr, hop_length=hop_length)
        onset_times = librosa.frames_to_time(onset_frames, sr=sr, hop_length=hop_length)
        
        # 结合节拍和onset，去重并排序
        all_times = np.concatenate([beat_times, onset_times])
        all_times = np.unique(all_times)
        all_times.sort()
        
        # 过滤太密集的时间点（间隔小于0.3秒的）
        filtered_times = [all_times[0]]
        for time in all_times[1:]:
            if time - filtered_times[-1] >= 0.3:
                filtered_times.append(time)
        
        self.beat_times = filtered_times
        logger.info(f"检测到 {len(self.beat_times)} 个节奏点，音乐速度: {tempo:.1f} BPM")
        
        return self.beat_times
    
    def load_video_files(self) -> List[str]:
        """
        加载视频文件列表
        
        Returns:
            视频文件路径列表
        """
        video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv']
        video_files = []
        
        for file in os.listdir(self.video_dir):
            if any(file.lower().endswith(ext) for ext in video_extensions):
                video_files.append(os.path.join(self.video_dir, file))
        
        logger.info(f"找到 {len(video_files)} 个视频文件")
        return video_files
    
    def calculate_video_dynamic_score(self, video_path: str, sample_frames: int = 10) -> float:
        """
        计算视频的动态程度分数
        
        Args:
            video_path: 视频文件路径
            sample_frames: 采样帧数
            
        Returns:
            动态程度分数
        """
        try:
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                return 0.0
            
            frames = []
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            # 均匀采样帧
            frame_indices = np.linspace(0, total_frames-1, sample_frames, dtype=int)
            
            for idx in frame_indices:
                cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
                ret, frame = cap.read()
                if ret:
                    # 转换为灰度图
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    frames.append(gray)
            
            cap.release()
            
            if len(frames) < 2:
                return 0.0
            
            # 计算帧间差异
            differences = []
            for i in range(1, len(frames)):
                diff = cv2.absdiff(frames[i], frames[i-1])
                mean_diff = np.mean(diff)
                differences.append(mean_diff)
            
            # 返回平均差异作为动态分数
            return np.mean(differences)
            
        except Exception as e:
            logger.warning(f"计算视频动态分数时出错: {e}")
            return 0.0
    
    def select_video_segments(self, segment_duration: float = 1.0) -> List[Tuple[str, float, float]]:
        """
        为每个节奏点选择视频片段
        
        Args:
            segment_duration: 每个片段的持续时间
            
        Returns:
            视频片段列表，每个元素为 (视频路径, 开始时间, 结束时间)
        """
        video_files = self.load_video_files()
        if not video_files:
            raise ValueError("没有找到视频文件")
        
        # 计算每个视频的动态分数
        video_scores = {}
        for video_path in video_files:
            score = self.calculate_video_dynamic_score(video_path)
            video_scores[video_path] = score
        
        # 按动态分数排序视频
        sorted_videos = sorted(video_scores.items(), key=lambda x: x[1], reverse=True)
        
        segments = []
        video_usage_count = {video: 0 for video in video_scores.keys()}
        
        for i, beat_time in enumerate(self.beat_times):
            # 选择使用次数最少的视频，优先选择动态分数高的
            available_videos = [(video, score) for video, score in sorted_videos 
                              if video_usage_count[video] < 3]  # 限制每个视频最多使用3次
            
            if not available_videos:
                # 如果所有视频都使用过多，重置计数
                video_usage_count = {video: 0 for video in video_scores.keys()}
                available_videos = sorted_videos
            
            # 选择视频
            selected_video = available_videos[0][0]
            video_usage_count[selected_video] += 1
            
            # 获取视频时长
            try:
                clip = VideoFileClip(selected_video)
                video_duration = clip.duration
                clip.close()
                
                # 随机选择开始时间，确保片段完整
                max_start = max(0, video_duration - segment_duration)
                if max_start > 0:
                    start_time = random.uniform(0, max_start)
                else:
                    start_time = 0
                
                end_time = min(start_time + segment_duration, video_duration)
                
                segments.append((selected_video, start_time, end_time))
                
            except Exception as e:
                logger.warning(f"处理视频 {selected_video} 时出错: {e}")
                # 如果出错，使用第一个可用视频
                if segments:
                    segments.append(segments[-1])  # 重复上一个片段
                else:
                    # 如果还没有片段，创建一个默认的
                    segments.append((video_files[0], 0, segment_duration))
        
        return segments
    
    def create_rhythm_video(self, segment_duration: float = 1.0) -> str:
        """
        创建节奏视频
        
        Args:
            segment_duration: 每个片段的持续时间
            
        Returns:
            输出文件路径
        """
        logger.info("开始创建节奏视频...")
        
        # 分析音频节奏
        if not self.beat_times:
            self.analyze_audio_rhythm()
        
        # 选择视频片段
        segments = self.select_video_segments(segment_duration)
        
        # 创建视频片段
        video_clips = []
        logger.info("正在处理视频片段...")
        
        for i, (video_path, start_time, end_time) in enumerate(tqdm(segments, desc="处理视频片段")):
            try:
                clip = VideoFileClip(video_path).subclip(start_time, end_time)
                
                # 调整片段时长以匹配节奏
                if i < len(self.beat_times) - 1:
                    target_duration = self.beat_times[i + 1] - self.beat_times[i]
                else:
                    target_duration = segment_duration
                
                # 如果片段太短，循环播放；如果太长，裁剪
                if clip.duration < target_duration:
                    # 循环播放直到达到目标时长
                    loops_needed = int(np.ceil(target_duration / clip.duration))
                    clip = concatenate_videoclips([clip] * loops_needed)
                    clip = clip.subclip(0, target_duration)
                elif clip.duration > target_duration:
                    clip = clip.subclip(0, target_duration)
                
                video_clips.append(clip)
                
            except Exception as e:
                logger.warning(f"处理视频片段 {video_path} 时出错: {e}")
                # 如果出错，创建一个黑色片段
                from moviepy.video.VideoClip import ColorClip
                fallback_clip = ColorClip(size=(1920, 1080), color=(0, 0, 0), duration=segment_duration)
                video_clips.append(fallback_clip)
        
        # 拼接视频片段
        logger.info("正在拼接视频片段...")
        final_video = concatenate_videoclips(video_clips)
        
        # 加载音频
        logger.info("正在加载音频...")
        audio_clip = AudioFileClip(self.audio_path)
        
        # 确保视频和音频长度匹配
        if final_video.duration > audio_clip.duration:
            final_video = final_video.subclip(0, audio_clip.duration)
        elif final_video.duration < audio_clip.duration:
            audio_clip = audio_clip.subclip(0, final_video.duration)
        
        # 设置音频
        final_video = final_video.set_audio(audio_clip)
        
        # 导出视频
        logger.info(f"正在导出视频到: {self.output_path}")
        final_video.write_videofile(
            self.output_path,
            codec='libx264',
            audio_codec='aac',
            temp_audiofile='temp-audio.m4a',
            remove_temp=True,
            verbose=False,
            logger=None
        )
        
        # 清理资源
        final_video.close()
        audio_clip.close()
        for clip in video_clips:
            clip.close()
        
        logger.info("视频创建完成！")
        return self.output_path

def main():
    """
    主函数示例
    """
    # 配置路径
    audio_path = "audio_files/music.mp3"  # 请将音频文件放在这里
    video_dir = "video_files"  # 请将视频文件放在这里
    output_path = "output/rhythm_video.mp4"
    
    # 检查文件是否存在
    if not os.path.exists(audio_path):
        print(f"错误: 音频文件不存在: {audio_path}")
        print("请将音频文件放在 audio_files 目录中")
        return
    
    if not os.path.exists(video_dir) or not os.listdir(video_dir):
        print(f"错误: 视频目录为空: {video_dir}")
        print("请将视频文件放在 video_files 目录中")
        return
    
    # 创建编辑器实例
    editor = RhythmVideoEditor(audio_path, video_dir, output_path)
    
    # 创建节奏视频
    try:
        output_file = editor.create_rhythm_video(segment_duration=1.0)
        print(f"视频创建成功: {output_file}")
    except Exception as e:
        print(f"创建视频时出错: {e}")

if __name__ == "__main__":
    main() 
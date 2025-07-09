# 节奏视频剪辑器 🎬

一个基于音乐节奏自动剪辑视频的Python工具，能够分析音频的节拍和鼓点，然后从多个视频文件中剪辑出符合音乐节奏的视频片段，最终拼接成一个"踩点"视频。

## 功能特点 ✨

- 🎵 **音频节奏分析**: 使用librosa库精确检测音乐的节拍、鼓点和音频起始点
- 🎬 **智能视频选择**: 根据视频的动态程度自动选择最适合的片段
- ⚡ **自动剪辑拼接**: 按节奏点时间间隔自动剪辑视频片段并拼接
- 🎯 **踩点效果**: 视频画面切换与音乐节奏完美同步
- 🔄 **防重复机制**: 避免同一视频片段过度使用，确保画面多样性

## 项目结构 📁

```
my-python/
├── audio_files/          # 音频文件目录
├── video_files/          # 视频文件目录  
├── output/               # 输出文件目录
├── rhythm_video_editor.py # 主要功能模块
├── example.py            # 使用示例
├── requirements.txt      # 依赖包列表
└── README.md            # 项目说明
```

## 安装依赖 📦

1. 确保已安装Python 3.7+
2. 安装所需依赖包：

```bash
pip install -r requirements.txt
```

### 依赖包说明

- `librosa`: 专业音频处理库，用于节奏分析
- `moviepy`: 视频处理库，用于视频剪辑和拼接
- `opencv-python`: 计算机视觉库，用于视频动态分析
- `numpy`: 数值计算库
- `scipy`: 科学计算库
- `tqdm`: 进度条显示

## 使用方法 🚀

### 1. 准备文件

将你的音频文件放在 `audio_files` 目录中：
```
audio_files/
└── music.mp3  # 你的音乐文件
```

将视频文件放在 `video_files` 目录中：
```
video_files/
├── video1.mp4
├── video2.mp4
├── video3.mp4
└── ...
```

### 2. 运行程序

#### 方法一：使用示例脚本
```bash
python example.py
```

#### 方法二：直接使用主模块
```bash
python rhythm_video_editor.py
```

#### 方法三：在代码中使用
```python
from rhythm_video_editor import RhythmVideoEditor

# 创建编辑器实例
editor = RhythmVideoEditor(
    audio_path="audio_files/music.mp3",
    video_dir="video_files",
    output_path="output/rhythm_video.mp4"
)

# 创建节奏视频
output_file = editor.create_rhythm_video(segment_duration=1.0)
print(f"视频创建成功: {output_file}")
```

### 3. 查看结果

生成的视频文件将保存在 `output` 目录中。

## 核心算法 🔧

### 音频节奏分析
1. **节拍检测**: 使用librosa的`beat_track`函数检测音乐节拍
2. **起始点检测**: 使用`onset_detect`函数检测音频起始点
3. **时间点合并**: 将节拍和起始点合并，去重并排序
4. **密度过滤**: 过滤掉间隔过小的时间点（默认小于0.3秒）

### 视频片段选择
1. **动态评分**: 计算每个视频的动态程度分数
2. **智能选择**: 优先选择动态分数高的视频，避免重复使用
3. **随机切片**: 从选中的视频中随机选择片段起始时间

### 视频拼接
1. **时长匹配**: 根据节奏点间隔调整视频片段时长
2. **循环播放**: 如果片段太短，循环播放直到达到目标时长
3. **音频同步**: 将原音频与视频同步

## 参数配置 ⚙️

### 音频分析参数
- `hop_length`: 音频分析步长（默认512）
- `sr`: 采样率（默认22050Hz）

### 视频剪辑参数
- `segment_duration`: 每个片段的默认持续时间（默认1.0秒）
- `sample_frames`: 视频动态分析采样帧数（默认10帧）

### 视频选择参数
- 每个视频最多使用3次（避免过度重复）
- 动态分数阈值可调整

## 支持的文件格式 📄

### 音频格式
- MP3
- WAV
- M4A
- FLAC
- OGG

### 视频格式
- MP4
- AVI
- MOV
- MKV
- FLV
- WMV

## 输出格式 🎥

- 视频编码: H.264
- 音频编码: AAC
- 分辨率: 保持原视频分辨率
- 帧率: 保持原视频帧率

## 注意事项 ⚠️

1. **内存使用**: 处理大文件时可能需要较多内存
2. **处理时间**: 视频处理时间取决于文件大小和数量
3. **文件路径**: 确保文件路径不包含特殊字符
4. **依赖安装**: 某些依赖可能需要额外的系统库（如ffmpeg）

## 故障排除 🔧

### 常见问题

1. **ImportError: No module named 'librosa'**
   ```bash
   pip install librosa
   ```

2. **FFmpeg相关错误**
   ```bash
   # macOS
   brew install ffmpeg
   
   # Ubuntu/Debian
   sudo apt-get install ffmpeg
   ```

3. **内存不足**
   - 减少视频文件数量
   - 降低视频分辨率
   - 使用更短的音频文件

4. **处理速度慢**
   - 使用SSD硬盘
   - 增加系统内存
   - 减少同时处理的文件数量

## 示例效果 🎯

输入：
- 音频：4分钟流行音乐
- 视频：10个不同的视频文件

输出：
- 检测到约300个节奏点
- 生成300个视频片段
- 每个片段0.8-1.2秒不等
- 视频画面随音乐节奏切换

## 许可证 📄

MIT License

## 贡献 🤝

欢迎提交Issue和Pull Request来改进这个项目！

---

**享受你的节奏视频创作！** 🎬✨ 
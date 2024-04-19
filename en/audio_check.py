import os
import glob
from pydub import AudioSegment

# 遍历当前目录及其所有子目录
for dirpath, dirnames, filenames in os.walk('.'):
    # 找到所有的wav文件
    wav_files = glob.glob(os.path.join(dirpath, '*.wav'))
    # 如果子目录中没有wav文件，跳过
    if not wav_files:
        continue
    # 按照1, 2, 3, ...的顺序重命名文件
    for i, wav_file in enumerate(sorted(wav_files), 1):
        # 读取音频文件
        audio = AudioSegment.from_wav(wav_file)
        # 设置采样率
        audio = audio.set_frame_rate(22050)
        # 保存音频文件
        new_file = os.path.join(dirpath, f'{i}.wav')
        audio.export(new_file, format='wav')
        # 删除原文件
        if wav_file != new_file:
            os.remove(wav_file)
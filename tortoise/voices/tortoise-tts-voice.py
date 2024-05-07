import os
import random
from pydub import AudioSegment
from scipy.io import wavfile

# 读取 speakerlist.txt 文件的第11-20行
with open("speakerlist.txt", "r") as f:
    dirs = [next(f).strip() for _ in range(10, 20)]

# 依次访问每个路径
for i, dir in enumerate(dirs, start=1):
    # 获取路径中的所有 wav 文件
    wav_files = [f for f in os.listdir(dir) if f.endswith(".wav")]

    # 随机选取25个 wav 文件
    selected_files = random.sample(wav_files, 25)

    # 每5个合成一个
    for j in range(5):
        combined = AudioSegment.empty()
        for file in selected_files[j * 5 : (j + 1) * 5]:
            sound = AudioSegment.from_wav(os.path.join(dir, file))
            combined += sound

        # 重新采样频率22050
        data = np.array(combined.get_array_of_samples())
        resampled_data = signal.resample(
            data, int(len(data) * 22050 / combined.frame_rate)
        )
        resampled_sound = AudioSegment(
            resampled_data.tobytes(),
            frame_rate=22050,
            sample_width=resampled_data.dtype.itemsize,
            channels=1,
        )

        # 保存新的 wav 文件
        output_dir = (
            f"/home/ydoit/AIGC/tortoise/tortoise-tts/tortoise/voices/speaker{i}"
        )
        os.makedirs(output_dir, exist_ok=True)
        resampled_sound.export(os.path.join(output_dir, f"{j+1}.wav"), format="wav")

import argparse
import os

import torch
import torchaudio

from api import TextToSpeech, MODELS_DIR
from utils.audio import load_voices
# args = parser.parse_args()
preset='fast'
use_deepspeed=False
kv_cache=True
half=True
output_path='results/'
model_dir=MODELS_DIR
candidates=1
seed=None
produce_debug_state=True
cvvp_amount=.0
if torch.backends.mps.is_available():
    use_deepspeed = False
os.makedirs(output_path, exist_ok=True)
tts = TextToSpeech(models_dir=model_dir, use_deepspeed=use_deepspeed, kv_cache=kv_cache, half=half)
def tts_gen_func(text,voice,index):
    selected_voices = voice.split(',')
    for k, selected_voice in enumerate(selected_voices):
        if '&' in selected_voice:
            voice_sel = selected_voice.split('&')
        else:
            voice_sel = [selected_voice]
        voice_samples, conditioning_latents = load_voices(voice_sel)

        gen, dbg_state = tts.tts_with_preset(text, k=candidates, voice_samples=voice_samples, conditioning_latents=conditioning_latents,
                                    preset=preset, use_deterministic_seed=seed, return_deterministic_state=True, cvvp_amount=cvvp_amount)
        if isinstance(gen, list):
            for j, g in enumerate(gen):
                torchaudio.save(os.path.join(output_path, voice,f'audio{index}_{k}_{j}.wav'), g.squeeze(0).cpu(), 24000)
        else:
            torchaudio.save(os.path.join(output_path,voice, f'audio{index}_{k}.wav'), gen.squeeze(0).cpu(), 24000)
        with open(os.path.join(output_path,voice,f'audio{index}.txt'), 'w') as f:
            f.write(text)

        if produce_debug_state:
            os.makedirs('debug_states', exist_ok=True)
            torch.save(dbg_state, f'debug_states/do_tts_debug_{selected_voice}.pth')
text_path='./tortoise/text.txt'
with open(text_path, 'r') as f:
    textall = f.readlines()
    count=0
    for row in textall:
        sp_index=int(count/10)+1
        audio_index=int(count%10)+1
        tts_gen_func(text=row,voice=f'speaker{sp_index}',index=audio_index)
        count+=1


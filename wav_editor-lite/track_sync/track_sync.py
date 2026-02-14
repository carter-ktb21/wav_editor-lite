import json
from pydub import AudioSegment
from pydub.silence import detect_nonsilent

def sync(track, data):
    audio_begin_pos = detect_nonsilent(track, min_silence_len=5, silence_thresh=-55)
    print(f"{audio_begin_pos[0][0]}")
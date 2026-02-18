from pydub import AudioSegment
from pydub.silence import detect_nonsilent

def sync(track, data) -> AudioSegment:
    audio_begin_pos = detect_nonsilent(track, min_silence_len=5, silence_thresh=-200, seek_step=1)
    print(audio_begin_pos[0][0])
    if audio_begin_pos[0][0] > 0:
        new_track = track[audio_begin_pos[0][0]:]
    else:
        new_track = track
    new_track = add_intro_silence(new_track, data)
    new_track = new_track[:data["total_track_duration"]]
    return new_track

def add_intro_silence(track, data):
    intro_silence = data["total_track_duration"] - data["track_duration_no_intro_silence"]
    if intro_silence > 0:
        print("Adding intro silence...")
        silence = AudioSegment.silent(duration=intro_silence)
        new_track = silence + track
        return new_track
    else:
        return track
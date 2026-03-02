from pydub import AudioSegment

def add_silence_blocks(track: AudioSegment, data) -> AudioSegment:
    new_wav = track
    for silence in data.get("silence_blocks", []):
        silence_duration = silence["silence_end"] - silence["silence_start"]
        if silence["silence_start"] > 0:
            pre_silence = new_wav[:silence["silence_start"]]
            if silence.get("pre_silence_fade"):
                pre_silence = silence_fade(pre_silence, silence["pre_silence_fade"])
            post_silence = new_wav[silence["silence_start"]:]
            if silence.get("post_silence_fade"):
                post_silence = silence_fade(post_silence, silence["post_silence_fade"])
            new_wav = pre_silence + AudioSegment.silent(duration=silence_duration) + post_silence
        else:
            new_wav = silence_fade(new_wav, silence)
            new_wav = AudioSegment.silent(duration=silence_duration) + new_wav
    return new_wav

def silence_fade(track: AudioSegment, data) -> AudioSegment:
    new_wav = track
    match data.get("type", "").lower():
        case "fade_in":
            new_wav = new_wav.fade_in(duration=data.get("fade_amount", 0))
        case "fade_out":
            new_wav = new_wav.fade_out(duration=data.get("fade_amount", 0))

    return new_wav
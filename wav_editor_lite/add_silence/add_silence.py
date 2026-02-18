from pydub import AudioSegment

def add_silence_blocks(track: AudioSegment, data) -> AudioSegment:
    new_wav = track
    for silence in data.get("silence_blocks", []):
        silence_duration = silence["silence_end"] - silence["silence_start"]
        if silence["silence_start"] > 0:
            new_wav = silence_fade(new_wav, silence)
            new_wav = new_wav[:silence["silence_start"]] + AudioSegment.silent(duration=silence_duration) + new_wav[silence["silence_end"]:]
            # new_wav = silence_fade(new_wav, silence)
        else:
            new_wav = silence_fade(new_wav, silence)
            new_wav = AudioSegment.silent(duration=silence_duration) + new_wav
            # new_wav = silence_fade(new_wav, silence)
    return new_wav

def silence_fade(track: AudioSegment, data) -> AudioSegment:
    new_wav = track
    for fade_data in data.get("surrounding_fade", []):
        match fade_data["type"].lower():
            case "fade_in":
                new_wav = new_wav.fade_in(duration=fade_data.get("fade_amount", 0))
            case "fade_out":
                print("TRUE")
                new_wav = new_wav.fade_out(duration=fade_data.get("fade_amount", 0))

    return new_wav
from pydub import AudioSegment

def add_amplify_blocks(track: AudioSegment, data) -> AudioSegment:
    new_wav = track
    for amplify_block in data.get("amplify_blocks", []):
        # amplify_duration = amplify_block["amplify_end"] - amplify_block["amplify_start"]
        if amplify_block.get("amplify_start"):
            if amplify_block["amplify_start"] > 0:
                pre_amplify = new_wav[:amplify_block["amplify_start"]]
                # if amplify_block.get("pre_amplify_fade"):
                #     pre_amplify = silence_fade(pre_silence, silence["pre_silence_fade"])
                post_amplify = new_wav[amplify_block["amplify_end"]:]
                amplify_segment = new_wav[amplify_block["amplify_start"]:amplify_block["amplify_end"]]
                amplify_segment = amplify_segment + amplify_block["amplify_amount"]
                # if silence.get("post_silence_fade"):
                #     post_amplify = silence_fade(post_amplify, silence["post_silence_fade"])
                new_wav = pre_amplify + amplify_segment + post_amplify
        else:
            new_wav = new_wav + amplify_block["amplify_amount"]
    return new_wav
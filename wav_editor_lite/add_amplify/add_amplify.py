from pydub import AudioSegment

def add_amplify_blocks(track: AudioSegment, data) -> AudioSegment:
    new_wav = track
    for amplify_block in data.get("amplify_blocks", []):
        if amplify_block.get("rise"):
            pre_amplify = new_wav[:amplify_block["amplify_start"]]
            post_amplify = new_wav[amplify_block["amplify_end"]:]
            amplify_rise_segment = new_wav[amplify_block["amplify_start"]:amplify_block["rise_end"]]
            amplify_rise_segment = amplify_rise_segment.fade(to_gain=amplify_block["rise"], start=0, duration=amplify_block["rise_end"]-amplify_block["amplify_start"])
            amplify_fall_segment = new_wav[amplify_block["rise_end"]:amplify_block["amplify_end"]]
            amplify_fall_segment = amplify_fall_segment.fade(from_gain=amplify_block["rise"], to_gain=0, start=0, duration=amplify_block["amplify_end"]-amplify_block["rise_end"])
            new_wav = pre_amplify + amplify_rise_segment + amplify_fall_segment + post_amplify
        elif amplify_block.get("amplify_start"):
            if amplify_block["amplify_start"] > 0:
                pre_amplify = new_wav[:amplify_block["amplify_start"]]
                post_amplify = new_wav[amplify_block["amplify_end"]:]
                amplify_segment = new_wav[amplify_block["amplify_start"]:amplify_block["amplify_end"]]
                amplify_segment = amplify_segment + amplify_block["amplify_amount"]
                new_wav = pre_amplify + amplify_segment + post_amplify
        else:
            new_wav = new_wav + amplify_block["amplify_amount"]
    return new_wav
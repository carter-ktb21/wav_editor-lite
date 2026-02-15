from pydub import AudioSegment

def arrange_clips(track: AudioSegment, data):
    new_track = track
    for clip_json in data["clips"]:
        match clip_json["type"].lower():
            case "trim":
                new_track = new_track[clip_json["clip_start_pos"]:clip_json["clip_end_pos"]]
            
            case "cut":
                pre_cut_segment = new_track[:clip_json["clip_start_pos"]]
                silence = AudioSegment.silent(duration=0)
                post_cut_segment = new_track[clip_json["clip_end_pos"]:]
                if clip_json.get("fade_out_pre_clip", 0) > 0:
                    pre_cut_segment = pre_cut_segment.fade_out(clip_json["fade_out_pre_clip"])

                silence = AudioSegment.silent(duration=clip_json.get("silence", 0))

                if clip_json.get("fade_in_post_clip", 0) > 0:
                    post_cut_segment = post_cut_segment.fade_in(clip_json["fade_in_post_clip"])

                new_track = pre_cut_segment + silence + post_cut_segment

            # case "overlay":

    return new_track
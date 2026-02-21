from pydub import AudioSegment
from pathlib import Path

def arrange_clips(track: AudioSegment, data, ext_wav_folder: Path="") -> AudioSegment:
    new_track = track
    for clip_json in data.get("clips", []):
        if clip_json.get("is_external_clip", 0) == 1:
            new_track = handle_external_clip(new_track, clip_json, ext_wav_folder)
        else:
            match clip_json.get("type", "").lower():
                case "trim":
                    new_track = new_track[clip_json["clip_start_pos"]:clip_json["clip_end_pos"]]

                    if clip_json.get("fade_in", 0) > 0:
                        new_track = new_track.fade_in(clip_json["fade_in"])
                
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

                case "move":
                    clip = new_track[clip_json["clip_start_pos"]:clip_json["clip_end_pos"]]

                    if clip_json.get("fade_in", 0) > 0:
                        clip = clip.fade_in(clip_json["fade_in"])

                    if clip_json.get("clip_placement_pos", 0) > 0:
                        pre_clip_segment = new_track[:clip_json["main_track_end_pos"]]
                        if clip_json.get("pre_clip_fade_out", 0) > 0:
                            pre_clip_segment = pre_clip_segment.fade_out(clip_json["pre_clip_fade_out"])
                            pre_clip_segment = pre_clip_segment + AudioSegment.silent()
                        new_track = pre_clip_segment.overlay(clip, clip_json["clip_placement_pos"]) + new_track[clip_json["clip_placement_pos"] + len(clip):]
                    else:
                        new_track = clip + new_track

                # todo - finish overlay
                case "overlay":
                    match clip_json.get("overlay_type", ""):
                        case "repeat":
                            clip = new_track[clip_json["clip_start_pos"]:clip_json["clip_end_pos"]]
                            pre_clip_segment = new_track[:clip_json["clip_end_pos"]]
                            if clip_json.get("fade_out_pre_clip", 0) > 0:
                                pre_clip_segment = pre_clip_segment.fade_out(clip_json["fade_out_pre_clip"])
                            if clip_json.get("fade_in_post_clip", 0) > 0:
                                clip = clip.fade_in(clip_json["fade_in_post_clip"])
                            new_track = pre_clip_segment.overlay(clip, clip_json["overlay_start_pos"])
                        case "loop_setup":
                            clip = new_track[clip_json["clip_start_pos"]:clip_json["clip_end_pos"]]
                            if clip_json.get("fade_out_pre_clip", 0) > 0:
                                new_track = new_track.fade_out(clip_json["fade_out_pre_clip"])
                            if clip_json.get("clip_fade_in", 0) > 0:
                                clip = clip.fade_in(clip_json["clip_fade_in"])
                            new_track = new_track.overlay(clip, clip_json["overlay_start_pos"])
                        case "insert_and_cut":
                            clip = new_track[clip_json["clip_start_pos"]:clip_json["clip_end_pos"]]
                            clip = clip.fade_in(clip_json["fade_in"])
                            pre_clip_segment = new_track[:clip_json["working_track_new_end"]]
                            pre_clip_segment = pre_clip_segment.fade_out(clip_json["fade_out"])
                            overlap_len = clip_json["working_track_new_end"] - clip_json["clip_placement_pos"]
                            silence_duration = len(clip) - overlap_len
                            pre_clip_segment = pre_clip_segment + AudioSegment.silent(duration=silence_duration)
                            pre_clip_segment = pre_clip_segment.overlay(clip, clip_json["clip_placement_pos"])
                            new_track = pre_clip_segment

    return new_track

def handle_external_clip(track: AudioSegment, data, ext_wav_folder: Path="") -> AudioSegment:
    new_track = track
    ext_wav_file = AudioSegment.from_wav(f"{ext_wav_folder}/{data["external_wav_name"]}.wav")
    ext_clip = ext_wav_file[data["ext_clip_start_pos"]:data["ext_clip_end_pos"]]

    # i.e. if clip is not inserted at the beginning
    if data["start_pos_in_track"] > 0:
        # todo
        return new_track
    else:
        if data.get("main_track_fade_in"):
            new_track = new_track.fade_in(data["main_track_fade_in"])
        if data.get("ext_clip_fade_out"):
            ext_clip = ext_clip.fade_out(data["ext_clip_fade_out"])
        ext_clip = ext_clip + AudioSegment.silent(duration=(len(new_track) - (data["ext_clip_end_pos"] - data["main_track_new_start_pos"])))
        new_track = ext_clip.overlay(new_track, data["main_track_new_start_pos"])


    return new_track
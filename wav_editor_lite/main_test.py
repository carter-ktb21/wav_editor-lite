from track_sync import sync
from arrange_clips import arrange_clips
from json_processor import process_json_folder
from pathlib import Path
from pydub import AudioSegment, effects
import imageio_ffmpeg as ffmpeg

json_list = process_json_folder(Path("C:/Users/Carter/Git_Repos/wav_editor-lite/wav_editor-lite/json_data_test"))

wav_path = Path("C:/Users/Carter/Twilight_Princess/Twilight Symphony/11_Hyrule_Field.wav")
stem = wav_path.stem

for json_file in json_list:
    if stem == json_file["track_name"]:
        print(json_file["track_name"])
        wav_file = AudioSegment.from_wav(wav_path)
        new_wav = sync(wav_file, json_file)
        new_wav = arrange_clips(new_wav, json_file)

        new_wav = new_wav.fade_out(json_file.get("fade_out", 0))

        # Amplification
        new_wav = new_wav + json_file.get("amplify", 0)

        # Sample Rate
        new_wav = new_wav.set_frame_rate(json_file.get("sample_rate", 48000))

        # Compression
        AudioSegment.converter = ffmpeg.get_ffmpeg_exe()
        path = ffmpeg.get_ffmpeg_exe()
        print(path)
        new_wav.export(
            "output.wav",
            format="wav",
            parameters=[
                "-af", "acompressor=threshold=-1dB:ratio=4:attack=5:release=50"
            ]
        )
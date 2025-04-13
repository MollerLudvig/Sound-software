import os
from pydub import AudioSegment

# TODO: Make it so that it converts all mp3 in a folder into wav and puts in another folder

AudioSegment.converter = r"C:\ffmpeg\bin\ffmpeg.exe"

def convert_mp3_to_wav(mp3_path, wav_folder):
    if not os.path.isfile(mp3_path):
        print(f"File not found: {mp3_path}")
        return

    if not os.path.exists(wav_folder):
        print(f"Folder not found: {wav_folder}. Creating it...")
        os.makedirs(wav_folder)

    audio = AudioSegment.from_mp3(mp3_path)

    wav_filename = os.path.splitext(os.path.basename(mp3_path))[0] + ".wav"
    wav_path = os.path.join(wav_folder, wav_filename)

    audio.export(wav_path, format="wav")
    print(f"✅ Converted to: {wav_path}")

convert_mp3_to_wav("mp3_files\Jet Set Radio - All Spray Sound Effects (HQ).mp3", "wav_files")

import os
import pygame
from pydub import AudioSegment
import librosa
import numpy as np
import soundfile as sf

class SoundHandler:
    def __init__(self, note_folder="pitched_wav", ffmpeg_path=r"C:\ffmpeg\bin\ffmpeg.exe"):
        # Setup ffmpeg for pydub
        AudioSegment.converter = ffmpeg_path
        self.note_folder = note_folder
        pygame.mixer.init()

    def convert_mp3_to_wav(self, mp3_path, wav_folder):
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

    def get_average_pitch_and_note(self, filepath):
        y, sr = librosa.load(filepath)
    
        # Use YIN for fundamental frequency estimation
        f0 = librosa.yin(y, fmin=librosa.note_to_hz('C1'), fmax=librosa.note_to_hz('C8'))
        
        # Filter out unvoiced (zero or nan) values
        f0 = f0[~np.isnan(f0)]
        
        if len(f0) == 0:
            return None, None

        average_pitch = np.median(f0)  # Median often more robust than mean
        note_name = librosa.hz_to_note(average_pitch)
        return average_pitch, note_name

    def play_single_note(self, filename):
        filepath = os.path.join(self.note_folder, filename)
        print(f"▶️ Playing: {filename}")
        try:
            pygame.mixer.music.load(filepath)
            pygame.mixer.music.play()
        except Exception as e:
            print(f"⚠️ Could not play {filename}: {e}")

    def pitch_shift_audio(self, input_file, output_folder, n_steps):
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        y, sr = librosa.load(input_file)
        y_shifted = librosa.effects.pitch_shift(y=y, sr=sr, n_steps=n_steps)

        full_filename = os.path.basename(input_file)
        filename, ext = os.path.splitext(full_filename)
        output_file = os.path.join(output_folder, f"pitched_{filename}_{n_steps}{ext}")

        sf.write(output_file, y_shifted, sr)
        print(f"✅ Pitched audio saved to: {output_file}")

    def pitch_files_in_folder(self, input_folder, output_folder, n_steps):
        for filename in os.listdir(input_folder):
            if filename.endswith(".wav"):
                input_file = os.path.join(input_folder, filename)
                self.pitch_shift_audio(input_file, output_folder, n_steps)





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
        self.NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

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

    
    def semitone_to_note_name(self, base_note='C4', n_steps=0):
        """Returns the note name N semitones from the base note."""
        # Convert base note (like C4) to MIDI number
        base_name = base_note[:-1]
        base_octave = int(base_note[-1])
        base_index = self.NOTE_NAMES.index(base_name)
        base_midi = base_octave * 12 + base_index

        new_midi = base_midi + n_steps
        new_octave = new_midi // 12
        note_index = new_midi % 12

        return f"{self.NOTE_NAMES[note_index]}{new_octave}"

    def pitch_shift_audio(self, input_file, output_folder, n_steps, base_note='C4'):
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        y, sr = librosa.load(input_file)
        y_shifted = librosa.effects.pitch_shift(y=y, sr=sr, n_steps=n_steps)

        note_name = self.semitone_to_note_name(base_note, n_steps)
        output_file = os.path.join(output_folder, f"{note_name}.wav")

        sf.write(output_file, y_shifted, sr)
        print(f"✅ Saved: {output_file}")

    def pitch_files_in_folder(self, input_folder, output_folder, steps_range=(-10, 25), base_note='C4'):
        for filename in os.listdir(input_folder):
            if filename.endswith(".wav"):
                input_file = os.path.join(input_folder, filename)
                for n_steps in range(steps_range[0], steps_range[1]):
                    self.pitch_shift_audio(input_file, output_folder, n_steps, base_note)






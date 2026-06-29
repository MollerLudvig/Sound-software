import os
import pygame
from pydub import AudioSegment
import librosa
import numpy as np
import soundfile as sf

import matplotlib.pyplot as plt
from scipy.io import wavfile # get the api
from scipy.fftpack import fft
from pylab import *

class SoundHandler:
    def __init__(self, ffmpeg_path=r"C:\ffmpeg\bin\ffmpeg.exe"):
        AudioSegment.converter = ffmpeg_path
        pygame.mixer.init()
        self.NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

    def convert_mp3_to_wav(self, mp3_path, wav_folder):
        if not os.path.isfile(mp3_path):
            print(f"File not found: {mp3_path}")
            return

        if not os.path.exists(wav_folder):
            print(f"Output folder {wav_folder} not found, creating it in current directory")
            os.makedirs(wav_folder)

        audio = AudioSegment.from_mp3(mp3_path)
        wav_filename = os.path.splitext(os.path.basename(mp3_path))[0] + ".wav"
        wav_path = os.path.join(wav_folder, wav_filename)

        audio.export(wav_path, format="wav")
        print(f"Converted to: {wav_path}")
        return wav_path

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
    
    def semitone_to_note_name(self, base_note='C4', n_steps=0):
        # Convert base note (like C4) to MIDI number
        base_name = base_note[:-1]
        base_octave = int(base_note[-1])
        base_index = self.NOTE_NAMES.index(base_name)
        base_midi = base_octave * 12 + base_index

        new_midi = base_midi + n_steps
        new_octave = new_midi // 12
        note_index = new_midi % 12

        return f"{self.NOTE_NAMES[note_index]}{new_octave}"

    def pitch_shift_audio(self, input_file, n_steps, base_note='C4'):
        y, sr = librosa.load(input_file)
        y_shifted = librosa.effects.pitch_shift(y=y, sr=sr, n_steps=n_steps)
        note_name = self.semitone_to_note_name(base_note, n_steps)
        print(f"Pitched: {note_name}")
        return note_name, y_shifted, sr
        # Create additional waveforms here: Pitch shift while keeping length (current), pitch shift changing length, and just sample

    def pitch_files_in_folder(self, input_folder, output_folder, steps_range=(-10, 25), base_note='C4'):

        if not os.path.exists(output_folder):
            print(f"Output folder {output_folder} not found, creating it in current directory")
            os.makedirs(output_folder)

        for filename in os.listdir(input_folder):
            if filename.endswith(".wav"):
                input_file = os.path.join(input_folder, filename)
                for n_steps in range(steps_range[0], steps_range[1]):
                    self.pitch_shift_audio(input_file, output_folder, n_steps, base_note)

    def fft(self, filepath):
        time_series, sample_rate = librosa.load(filepath, sr=None)
        fft_result = np.fft.fft(time_series)
        magnitude = np.abs(fft_result)
        frequency = np.fft.fftfreq(len(magnitude), d=1/sample_rate)

        # First half of fft is negative
        half_len = len(magnitude) // 2
        magnitude = magnitude[:half_len]
        frequency = frequency[:half_len]

        plt.figure(figsize=(12, 6))
        plt.plot(frequency, magnitude, color='tomato')
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Magnitude')
        plt.title('Frequency Spectrum')
        plt.grid(True)
        filename = os.path.splitext(os.path.basename(filepath))
        plt.savefig(f"plots/{filename[0]}", dpi=300)







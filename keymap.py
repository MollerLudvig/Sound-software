import os
import re
import pygame

# Full key layout: 1-0, Q-P, A-L, Z-M
key_labels = [
    '1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
    'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P',
    'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L',
    'Z', 'X', 'C', 'V', 'B', 'N', 'M'
]

# Convert to pygame key constants
key_order = [(label, getattr(pygame, f'K_{label.lower()}')) for label in key_labels]

sound_folder = "pitched_wav"

# Regex to extract pitch number from filename
def extract_pitch_value(filename):
    match = re.search(r'(-?\d+)', filename)
    return int(match.group(1)) if match else 0

# Sort all .wav files numerically by pitch
wav_files = sorted(
    [f for f in os.listdir(sound_folder) if f.endswith(".wav")],
    key=extract_pitch_value
)

# Match sounds to keys
keymap = []
for (label, key), filename in zip(key_order, wav_files):
    keymap.append((label, key, filename))

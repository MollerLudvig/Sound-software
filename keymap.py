import os
import re
import pygame

# Full key layout: 1-0, Q-P, A-L, Z-M (35 keys total)
key_labels = [
    '1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
    'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P',
    'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L',
    'Z', 'X', 'C', 'V', 'B', 'N', 'M'
]

# Convert to pygame key constants
key_order = [(label, getattr(pygame, f'K_{label.lower()}')) for label in key_labels]

sound_folder = "pitched_wav"

if not os.path.exists(sound_folder):
    print(f"Output folder {sound_folder} not found, creating it in current directory")
    os.makedirs(sound_folder)

# Helper to extract MIDI number from a note name like "C#4"
def note_to_midi(note):
    note_names = {'C': 0, 'C#': 1, 'D': 2, 'D#': 3, 'E': 4,
                  'F': 5, 'F#': 6, 'G': 7, 'G#': 8, 'A': 9, 'A#': 10, 'B': 11}
    match = re.match(r"([A-G]#?)(-?\d+)", note)
    if match:
        name, octave = match.groups()
        return (int(octave) + 1) * 12 + note_names[name]
    return 0  # fallback if the format is wrong

# Get and sort .wav files by MIDI pitch
wav_files = sorted(
    [f for f in os.listdir(sound_folder) if f.endswith(".wav")],
    key=lambda f: note_to_midi(os.path.splitext(f)[0])
)

# Match sounds to keys
keymap = []
for (label, key), filename in zip(key_order, wav_files):
    note_name = os.path.splitext(filename)[0]
    keymap.append((label, key, filename, note_name))

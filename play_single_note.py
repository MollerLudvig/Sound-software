import pygame
import os

note_folder = "pitched_wav"

# Only initialize mixer once, ideally at app start
pygame.mixer.init()

def play_single_note(filename):
    filepath = os.path.join(note_folder, filename)
    print(f"▶️ Playing: {filename}")
    try:
        pygame.mixer.music.load(filepath)
        pygame.mixer.music.play()
        # No blocking — returns immediately
    except Exception as e:
        print(f"⚠️ Could not play {filename}: {e}")

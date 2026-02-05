import os
import pygame
import time

def play_with_pygame(folder):
    pygame.mixer.init()
    wav_files = sorted([f for f in os.listdir(folder) if f.endswith(".wav")])

    for filename in wav_files:
        filepath = os.path.join(folder, filename)
        print(f"▶️ Playing: {filename}")
        try:
            pygame.mixer.music.load(filepath)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)  # check every 100ms if playback is done
        except Exception as e:
            print(f"⚠️ Could not play {filename}: {e}")

play_with_pygame("pitched_wav")

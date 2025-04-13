import sounddevice as sd
import soundfile as sf
import threading
import time
import os
import pygame

def record_audio(filename, duration, device, samplerate=44100, channels=2):
    print("🔴 Recording started...")
    recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=channels, dtype='float32', device=device)
    sd.wait()
    sf.write(filename, recording, samplerate)
    print(f"💾 Recording saved to: {filename}")

def play_overlapping_sequence(folder, sequence, delays=None):
    pygame.mixer.init()
    last_sound = None
    total_play_time = 0.0

    for i, number in enumerate(sequence):
        matching_files = [f for f in os.listdir(folder) if f.endswith(f"_{number}.wav")]
        if not matching_files:
            print(f"⚠️ No file found for number {number}")
            continue

        filename = matching_files[0]
        filepath = os.path.join(folder, filename)
        print(f"▶️ Playing: {filename}")

        try:
            sound = pygame.mixer.Sound(filepath)
            sound.play()
            last_sound = sound
        except Exception as e:
            print(f"⚠️ Could not play {filename}: {e}")

        if delays and i < len(delays):
            total_play_time += delays[i]
            time.sleep(delays[i])

    if last_sound:
        final_delay = last_sound.get_length() + 0.1
        total_play_time += final_delay
        time.sleep(final_delay)

    return total_play_time

# Example usage
sequence = [0, 1, 2, 3, 4, 5, 0, 3, 5, 0, 0, 3, 4, 5]
delays = [0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.1, 0.2, 0.7, 0.1, 0.2, 0.2, 0.2]  # len = len(sequence) - 1

device = -1  # Device index or device name

estimated_duration = sum(delays) + 3  # quick estimate, adjusted later
record_thread = threading.Thread(target=record_audio, args=("output.wav", estimated_duration, device))
record_thread.start()

# Now play the sound sequence
actual_duration = play_overlapping_sequence("pitched_wav", sequence, delays)

# Wait for recording to finish
record_thread.join()

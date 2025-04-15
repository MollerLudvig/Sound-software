import librosa
import numpy as np

def get_average_pitch_and_note(filepath):
    y, sr = librosa.load(filepath)
    pitches, magnitudes = librosa.piptrack(y=y, sr=sr)

    pitch_values = []
    for i in range(pitches.shape[1]):
        index = magnitudes[:, i].argmax()
        pitch = pitches[index, i]
        if pitch > 0:
            pitch_values.append(pitch)

    if not pitch_values:
        return None, None  # In case no pitch was detected

    average_pitch = np.mean(pitch_values)
    note_name = librosa.hz_to_note(average_pitch)

    return average_pitch, note_name

avg_pitch, note = get_average_pitch_and_note("pitched_wav/pitched_combo_sound_1.wav")
if avg_pitch is not None:
    print(f"Average pitch: {avg_pitch:.2f} Hz → Note: {note}")
else:
    print("No pitch detected in the audio.")
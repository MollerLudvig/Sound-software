import os
import librosa
import soundfile as sf

# TODO: Make a GUI that can for example choose what files in a directory to convert
# And what pitches to convert those files into

def pitch_shift_audio(input_file, output_folder, n_steps):
    if not os.path.exists(output_folder):
        print(f"Folder not found: {output_folder}. Creating it...")
        os.makedirs(output_folder)

    y, sr = librosa.load(input_file)

    y_shifted = librosa.effects.pitch_shift(y=y, sr=sr, n_steps=n_steps) 

    full_filename = os.path.basename(input_file)
    filename, extention = os.path.splitext(full_filename)

    output_file = os.path.join(output_folder, f"pitched_{filename}_{n_steps}{extention}")


    sf.write(output_file, y_shifted, sr)
    print(f"✅ Pitched audio saved to: {output_file}")

def pitch_files_in_folder(input_folder, output_folder, n_steps):
    for filename in os.listdir(input_folder):
        if filename.endswith(".wav"):  
            input_file = os.path.join(input_folder, filename)
            pitch_shift_audio(input_file, output_folder, n_steps)


input_folder = "wav_files"
output_folder = "pitched_wav"

for n_steps in range(10):
    pitch_files_in_folder(input_folder, output_folder, n_steps)

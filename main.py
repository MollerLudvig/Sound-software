from KeyboardApp import KeyboardApp
import os
import glob
import time


#TODO: Make so that you can play multiple notes at once and hold down notes
if __name__ == '__main__':
    pitched_files = glob.glob('pitched_wav/*.wav')
    for f in pitched_files:
        os.remove(f)
    
    wav_files = glob.glob('wav_files/*.wav')
    for f in wav_files:
        os.remove(f)

    time.sleep(2)
    app = KeyboardApp()
    app.run()
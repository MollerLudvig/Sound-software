from KeyboardApp import KeyboardApp
import os
import glob



#TODO: Make so that you can play multiple notes at once and hold down notes
if __name__ == '__main__':
    files = glob.glob('pitched_wav/*.wav')
    for f in files:
        os.remove(f)

    app = KeyboardApp()
    app.run()
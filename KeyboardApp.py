import pygame
from SoundHandler import SoundHandler
from KeyButton import KeyButton
import time
import tkinter as tk
from tkinter import filedialog
import os
import importlib
import keymap


class KeyboardApp:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((2000, 500))
        pygame.display.set_caption("Virtual Keyboard")
        self.font = pygame.font.SysFont('Georgia', 20, bold=True)
        self.clock = pygame.time.Clock()
        self.running = True

        self.sound_handler = SoundHandler()
        self.buttons = []

        self.init_keyboard()

        load_btn_rect = (15, 20, 100, 40)
        self.load_btn = KeyButton(rect=load_btn_rect, label="Load", key=None,
            sound_file=None, note_name="", sound_handler=self.sound_handler
        )

        self.load_btn.set_click_callback(self.load_and_process_file)

    def init_keyboard(self):
        # Fuckass solution to just import again to run 'keymap' file again with updated sound folder
        # Should probably make a class of 'keymap' with an update method and whatever else...
        importlib.reload(keymap)
        self.keymap = keymap.keymap
        for i, (label, key, sound, note_name) in enumerate(self.keymap):
            x = 15 + i*55
            y = 200
            btn = KeyButton(rect=(x, y, 50, 300), label=label, key=key,
                    sound_file=sound, note_name=note_name, sound_handler=self.sound_handler)
            #TODO: Could maybe do callback function for these too
            self.buttons.append(btn)

    def load_and_process_file(self):
    
        root = tk.Tk()
        root.withdraw()

        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav")])
        if not file_path:
            print("No file selected.")
            return

        # Remove current sounds if a new sound file has been selected
        # Which in turn clears the part of the RAM that was taken up by the sound object
        pygame.mixer.stop()
        self.buttons.clear()

        filename = os.path.basename(file_path)
        name_no_extention, extention = os.path.splitext(filename)

        if extention.lower() == '.mp3':
            wav_output_path = os.path.join('wav_files', name_no_extention + '.wav')
            self.sound_handler.convert_mp3_to_wav(file_path, 'wav_files')
        elif extention.lower() == '.wav':
            wav_output_path = file_path
        else:
            print("Unsupported format")
            return

        # TODO: Pitch detection of OG file to know base note
        for n_steps in range(-10, 25):
            self.sound_handler.pitch_shift_audio(wav_output_path, "pitched_wav", n_steps, base_note='F4')

        self.init_keyboard()

    def run(self):

        while self.running:
            self.screen.fill('grey')
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                for button in self.buttons:
                    button.handle_event(event, mouse_pos)
                self.load_btn.handle_event(event, mouse_pos)

            for button in self.buttons:
                button.draw(self.screen, self.font)
            self.load_btn.draw(self.screen, self.font)

            pygame.display.update()
            self.clock.tick(60)  # Cap frame rate

        pygame.quit()

import pygame
from SoundHandler import SoundHandler
from KeyButton import KeyButton
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
        self.font = pygame.font.SysFont('Georgia', 14, bold=True)
        self.clock = pygame.time.Clock()
        self.running = True

        self.sound_handler = SoundHandler()

        self.init_keyboard()

        load_btn_rect = (15, 20, 100, 40)
        self.load_btn = KeyButton(rect=load_btn_rect, label="Load", key=None,
            sound_file=None, note_name="", sound_handler=self.sound_handler
        )
        self.load_btn.set_click_callback(self.load_and_process_file)

    def init_keyboard(self):
        importlib.reload(keymap)
        self.keymap = keymap.keymap
        self.white_buttons = []
        self.black_buttons = []

        WHITE_W, WHITE_H = 50, 280
        BLACK_W, BLACK_H = 30, 170
        START_X = 15
        KEY_Y = 180

        current_x = START_X

        for (label, key, sound_file, note_name) in self.keymap:
            is_black = '#' in note_name

            if is_black:
                # Centre over the gap between the previous and next white key
                x = current_x - BLACK_W // 2
                btn = KeyButton(
                    rect=(x, KEY_Y, BLACK_W, BLACK_H),
                    label=label, key=key, sound_file=sound_file,
                    note_name=note_name, sound_handler=self.sound_handler,
                    is_black=True
                )
                self.black_buttons.append(btn)
            else:
                btn = KeyButton(
                    rect=(current_x, KEY_Y, WHITE_W, WHITE_H),
                    label=label, key=key, sound_file=sound_file,
                    note_name=note_name, sound_handler=self.sound_handler,
                    is_black=False
                )
                self.white_buttons.append(btn)
                current_x += WHITE_W + 2

    def load_and_process_file(self):
        root = tk.Tk()
        root.withdraw()

        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav")])
        if not file_path:
            print("No file selected.")
            return

        pygame.mixer.stop()
        self.white_buttons.clear()
        self.black_buttons.clear()

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

        for n_steps in range(-10, 25):
            self.sound_handler.pitch_shift_audio(wav_output_path, "pitched_wav", n_steps, base_note='F4')

        self.init_keyboard()

    def run(self):
        while self.running:
            self.screen.fill((100, 100, 100))
            mouse_pos = pygame.mouse.get_pos()
 
            over_black_key = any(btn.rect.collidepoint(mouse_pos) for btn in self.black_buttons)
 
            # Update hovered state for all buttons once per frame
            for button in self.white_buttons:
                button.update(mouse_pos, over_black_key)
            for button in self.black_buttons:
                button.update(mouse_pos)
            self.load_btn.update(mouse_pos)
 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                for button in self.white_buttons:
                    button.handle_event(event)
                for button in self.black_buttons:
                    button.handle_event(event)
                self.load_btn.handle_event(event)
 
            for button in self.white_buttons:
                button.draw(self.screen, self.font)
            for button in self.black_buttons:
                button.draw(self.screen, self.font)
            self.load_btn.draw(self.screen, self.font)
 
            pygame.display.update()
            self.clock.tick(60)

        pygame.quit()
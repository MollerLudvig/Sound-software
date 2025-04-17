import pygame
from SoundHandler import SoundHandler
from KeyButton import KeyButton
import keymap
import time

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

        for i, (label, key, sound, note_name) in enumerate(keymap.keymap):
            x = 15 + i*55
            y = 200
            btn = KeyButton(rect=(x, y, 50, 300), label=label, key=key,
                    sound_file=sound, note_name=note_name, sound_handler=self.sound_handler)
            self.buttons.append(btn)

    def run(self):
        #TODO: Make button to load a mp3 file and use that as the sound
        self.sound_handler.convert_mp3_to_wav('mp3_files/combo_sound.mp3', 'wav_files')
        self.sound_handler.pitch_files_in_folder('wav_files', 'pitched_wav', (-10, 25), 'F4')

        #TODO: Do fft to figure out the pitch of the sound
        print(self.sound_handler.get_average_pitch_and_note('wav_files/combo_sound.wav'))

        time.sleep(2)

        while self.running:
            self.screen.fill('pink')
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                for button in self.buttons:
                    button.handle_event(event, mouse_pos)

            for button in self.buttons:
                button.draw(self.screen, self.font)

            pygame.display.update()
            self.clock.tick(60)  # Cap frame rate

        pygame.quit()

import pygame
from SoundHandler import SoundHandler
from KeyButton import KeyButton

class KeyboardApp:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((2000, 500))
        pygame.display.set_caption("Virtual Keyboard")
        self.font = pygame.font.SysFont('Georgia', 40, bold=True)
        self.clock = pygame.time.Clock()
        self.running = True

        self.sound_handler = SoundHandler()
        self.buttons = [
            KeyButton(rect=(30, 200, 60, 300), label='A', key=pygame.K_a,
                      sound_file='pitched_combo_sound_0.wav', sound_handler=self.sound_handler)
            # Add more buttons here later!
        ]

    def run(self):
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

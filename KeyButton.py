import pygame
import os

class KeyButton:
    def __init__(self, rect, label, key, sound_file, note_name, sound_handler, is_black=False):
        self.rect = pygame.Rect(rect)
        self.label = label
        self.key = key
        self.sound_file = sound_file
        self.note_name = note_name
        self.sound_handler = sound_handler
        self.is_black = is_black

        # Load sounds into RAM once instead of each time i press a key
        self.sound = None
        if sound_file:
            path = os.path.join(sound_handler.note_folder, sound_file)
            try:
                self.sound = pygame.mixer.Sound(path)
            except Exception as e:
                print(f"Failed loading {sound_file}: {e}")

        if is_black:
            self.color_default = (30, 30, 30)
            self.color_hover   = (70, 70, 70)
            self.color_pressed = (80, 110, 220)
        else:
            self.color_default = (255, 255, 255)
            self.color_hover   = (180, 180, 180)
            self.color_pressed = (100, 150, 255)

        self.click_callback = None
        self.mouse_held = False
        self.key_held = False
        self.hovered = False

    # Update hovered state for the key
    def update(self, mouse_pos, over_black_key=False):
        self.hovered = self.rect.collidepoint(mouse_pos) and not (not self.is_black and over_black_key)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == self.key:
            if self.sound:
                self.sound.play()
            self.key_held = True

        elif event.type == pygame.KEYUP and event.key == self.key:
            self.key_held = False

        elif event.type == pygame.MOUSEBUTTONDOWN and self.hovered:
            if self.sound:
                self.sound.play()
            if self.click_callback:
                self.click_callback()
            self.mouse_held = True

        elif event.type == pygame.MOUSEBUTTONUP:
            self.mouse_held = False

    def draw(self, screen, font):
        if (self.hovered and self.mouse_held) or self.key_held:
            color = self.color_pressed
        elif self.hovered:
            color = self.color_hover
        else:
            color = self.color_default

        pygame.draw.rect(screen, color, self.rect)

        # Outline for white keys so they have visible borders
        if not self.is_black:
            pygame.draw.rect(screen, (0, 0, 0), self.rect, 1)

        # Keyboard shortcut label near top
        label_surface = font.render(self.label, True, 'white' if self.is_black else 'black')
        label_text_rect = label_surface.get_rect(center=(self.rect.centerx, self.rect.y + 12))
        screen.blit(label_surface, label_text_rect)

        # Note name near bottom
        note_surface = font.render(self.note_name, True, 'white' if self.is_black else 'black')
        note_text_rect = note_surface.get_rect(center=(self.rect.centerx, self.rect.bottom - 15))
        screen.blit(note_surface, note_text_rect)

    def set_click_callback(self, callback):
        self.click_callback = callback
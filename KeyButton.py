import pygame
import os

class KeyButton:
    def __init__(self, rect, label, key, sound_file, note_name, sound_handler):
        self.rect = pygame.Rect(rect)
        self.label = label
        self.key = key
        self.sound_file = sound_file
        self.note_name = note_name
        self.sound_handler = sound_handler

        self.sound = None
        if sound_file:
            path = os.path.join(sound_handler.note_folder, sound_file)
            try:
                self.sound = pygame.mixer.Sound(path)
            except Exception as e:
                print(f"Failed loading {sound_file}: {e}")

        self.color_default = (255, 255, 255)
        self.color_hover = (180, 180, 180)
        self.color_pressed = (100, 150, 255)

        self.click_callback = None
        self.mouse_held = False
        self.key_held = False

    def handle_event(self, event, mouse_pos):
        hovered = self.rect.collidepoint(mouse_pos)

        if event.type == pygame.KEYDOWN and event.key == self.key:
            self.sound_handler.play_single_note(self.sound_file)
            self.key_held = True

        elif event.type == pygame.KEYUP and event.key == self.key:
            self.key_held = False

        elif event.type == pygame.MOUSEBUTTONDOWN and hovered:
            if self.sound:
                self.sound.play()
            
            if self.click_callback:
                self.click_callback()
            self.mouse_held = True
            

        elif event.type == pygame.MOUSEBUTTONUP:
            self.mouse_held = False

    def draw(self, screen, font):
        hovered = self.rect.collidepoint(pygame.mouse.get_pos())

        if (hovered and self.mouse_held) or self.key_held:
            color = self.color_pressed
        elif hovered:
            color = self.color_hover
        else:
            color = self.color_default

        pygame.draw.rect(screen, color, self.rect)
        label_surface = font.render(self.label, True, 'black')
        label_text_rect = label_surface.get_rect(center=(self.rect.centerx, self.rect.y+10))
        screen.blit(label_surface, label_text_rect)

        note_surface = font.render(self.note_name, True, 'black')
        note_text_rect = note_surface.get_rect(center=(self.rect.centerx, self.rect.centery + self.rect.height/2 - 15))
        screen.blit(note_surface, note_text_rect)

    def set_click_callback(self, callback):
        self.click_callback = callback
import pygame
from SoundHandler import SoundHandler

pygame.init()
screen = pygame.display.set_mode((2000, 500))
font = pygame.font.SysFont('Georgia', 40, bold=True)

sh = SoundHandler()

# Button setup
button = pygame.Rect(30, 200, 60, 300)
color_default = (255, 255, 255)     # white
color_hover = (180, 180, 180)       # gray
color_pressed = (100, 150, 255)     # blue

# State tracking
mouse_held = False
key_held = False
running = True

while running:
    screen.fill('pink')
    mouse_pos = pygame.mouse.get_pos()
    button_hovered = button.collidepoint(mouse_pos)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Keyboard press
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                sh.play_single_note("pitched_combo_sound_0.wav")
                key_held = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                key_held = False

        # Mouse pressed down
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_hovered:
                sh.play_single_note("pitched_combo_sound_0.wav")
                mouse_held = True

        # Mouse released
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_held = False

    # Draw the button with the right color
    if (button_hovered and mouse_held) or key_held:
        color = color_pressed
    elif button_hovered:
        color = color_hover
    else:
        color = color_default

    pygame.draw.rect(screen, color, button)

    label = font.render('A', True, 'black')
    screen.blit(label, (button.x + 15, button.y + 10))

    pygame.display.update()

pygame.quit()

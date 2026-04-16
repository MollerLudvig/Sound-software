import pygame

# Full key layout: 1-0, Q-P, A-L, Z-M (35 keys total)
key_labels = [
    '1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
    'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P',
    'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L',
    'Z', 'X', 'C', 'V', 'B', 'N', 'M'
]

keymap = [(label, getattr(pygame, f'K_{label.lower()}')) for label in key_labels]
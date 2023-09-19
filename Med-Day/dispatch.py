import pygame
from pygame.locals import *
import subprocess

pygame.init()
pygame.mixer.init()  # Initialize the mixer


# Colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Constants
WIDTH, HEIGHT = 800, 600
FADE_SPEED = 0.15  # How much alpha will change each frame
WAIT_TIME = 3000  # How long to wait (in frames) at full transparency

sound_effect = pygame.mixer.Sound('game-start-6104.mp3')

# Play the sound effect immediately
sound_effect.play()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Narration Screen')
font = pygame.font.SysFont('Courier New', 17)

# Text for the dispatch and EMT
dispatch_text = ("200, 210 on the fill. E2 response to 500 S. Bouquet St in Oakland "
                 "for a 32 year old male complaining of chest pain. Patient called and reported it "
                 "started about an hour ago. Recommendation to enter through back door. Time out [22:39]")
emt_text = "205 en route. Time out [22:39]"

# Alpha and direction for fade effect
alpha = 0
fade_direction = FADE_SPEED
wait_counter = 0

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == MOUSEBUTTONDOWN:
            subprocess.call(["python", "gameInterface.py"])
            pygame.quit()

    # Fade logic
    alpha += fade_direction
    if alpha >= 255:
        alpha = 255
        if wait_counter >= WAIT_TIME:
            fade_direction = -FADE_SPEED
            wait_counter = 1
        else:
            wait_counter += 1
    elif alpha <= 0:
        alpha = 0
        if wait_counter >= WAIT_TIME:
            fade_direction = FADE_SPEED
            wait_counter = 0
        else:
            wait_counter += 1

    # Drawing
    screen.fill(BLACK)
    
    dispatch_label = font.render("Dispatch:", True, RED)
    screen.blit(dispatch_label, (WIDTH // 2 - dispatch_label.get_width() // 2, 90))
    
    y_offset = 140
    for line_text in dispatch_text.split('. '):
        line = font.render(line_text, True, [min(c, alpha) for c in WHITE])
        screen.blit(line, (WIDTH // 2 - line.get_width() // 2, y_offset))
        y_offset += line.get_height() + 5

    emt_label = font.render("EMT:", True, RED)
    screen.blit(emt_label, (WIDTH // 2 - emt_label.get_width() // 2, 370))

    emt_line_surf = font.render(emt_text, True, WHITE)
    emt_line_surf.set_alpha(alpha)
    screen.blit(emt_line_surf, (WIDTH // 2 - emt_line_surf.get_width() // 2, 420))

    pygame.display.flip()

pygame.quit()

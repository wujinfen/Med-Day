import pygame
import random
import time
import math
import subprocess

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Load and play music
pygame.mixer.music.load('happy-14585.mp3')
pygame.mixer.music.play(-1)  # -1 means loop indefinitely

# Screen dimensions
WIDTH, HEIGHT = 800, 600

# Colors
BLACK = (0, 0, 0)
GLOW = (255, 255, 200)
RED = (255, 0, 0)
ROAD_COLOR = (100, 100, 100)
GUARDRAIL_COLOR = (60, 60, 60)
BLUE = (173, 216, 230)
WHITE = (255, 255, 255)
BUTTON_WIDTH, BUTTON_HEIGHT = 360, 108
BUTTON_X, BUTTON_Y = (WIDTH - BUTTON_WIDTH) // 1.5, HEIGHT * 0.37
BUTTON_OUTLINE_COLOR = (0, 0, 139)
BUTTON_OUTLINE_WIDTH = 4
click_sound = pygame.mixer.Sound('click.mp3')
driving = False
fade_out_started = False
fade_out_start_time = None


def draw_rounded_rect(screen, rect, color, border_radius, border_color=None, border_width=0):
    if border_color:
        # Draw the filled border rectangle first
        pygame.draw.rect(screen, border_color, rect)
    
    inner_rect = (
        rect[0] + border_width,
        rect[1] + border_width,
        rect[2] - 2 * border_width,
        rect[3] - 2 * border_width
    )
    pygame.draw.rect(screen, color, inner_rect)
    
    # Top-left corner
    pygame.draw.circle(screen, color, (inner_rect[0] + border_radius, inner_rect[1] + border_radius), border_radius)
    # Top-right corner
    pygame.draw.circle(screen, color, (inner_rect[0] + inner_rect[2] - border_radius, inner_rect[1] + border_radius), border_radius)
    # Bottom-left corner
    pygame.draw.circle(screen, color, (inner_rect[0] + border_radius, inner_rect[1] + inner_rect[3] - border_radius), border_radius)
    # Bottom-right corner
    pygame.draw.circle(screen, color, (inner_rect[0] + inner_rect[2] - border_radius, inner_rect[1] + inner_rect[3] - border_radius), border_radius)


ambulance_bounce_time = 0  # to keep track of time for the sine function
ambulance_bounce_amplitude = 2  # How much the ambulance moves up and down
ambulance_sway_amplitude = 2  # How much the ambulance moves left and right

def draw_button_text(screen, text, position, font_size, color):
    font = pygame.font.Font('font1.ttf', font_size)  # Use the font_size parameter
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=position)
    screen.blit(text_surface, text_rect)


def random_yellowish_white():
    r = random.randint(220, 255)
    g = random.randint(220, 255)
    b = random.randint(180, 220)
    return r, g, b

# Star properties
NUM_STARS = 150
stars = [{'x': random.randint(0, WIDTH),
          'y': random.randint(0, int(HEIGHT * 0.8)),
          'size': random.randint(3, 6),
          'max_size': random.randint(7, 10),
          'min_size': random.randint(2, 4),
          'speed': random.uniform(0.01, 0.05),
          'direction': 1,
          'color': random_yellowish_white()} for _ in range(NUM_STARS)]

def update_stars():
    for star in stars:
        star['size'] += star['speed'] * star['direction']
        if star['size'] > star['max_size'] or star['size'] < star['min_size']:
            star['direction'] *= -1

def draw_stars(screen):
    for star in stars:
        pygame.draw.circle(screen, star['color'], (star['x'], star['y']), 2)
        pygame.draw.line(screen, star['color'], 
                         (star['x'] - star['size'], star['y']), 
                         (star['x'] + star['size'], star['y']))
        pygame.draw.line(screen, star['color'], 
                         (star['x'], star['y'] - star['size']), 
                         (star['x'], star['y'] + star['size']))

def draw_moon(screen):
    moon_image = pygame.image.load('moon-removebg-preview.png').convert_alpha()  # Ensure transparency is handled
    moon_image = pygame.transform.scale(moon_image, (300, 300))
    moon_x = WIDTH * 0.15 - moon_image.get_width() // 2  # Positioned on the left
    moon_y = HEIGHT * 0.2 - moon_image.get_height() // 2  # Positioned slightly lower
    screen.blit(moon_image, (moon_x, moon_y))

def draw_title_text(screen):
    font = pygame.font.Font('font1.ttf', 75)
    
    # Render "Med-Day:" in red
    text_med_day = font.render("Med-Day:", True, RED)
    text_med_day_x = WIDTH - text_med_day.get_width() - 250  # position calculation
    text_med_day_y = 150  # Just a little padding from the top
    screen.blit(text_med_day, (text_med_day_x, text_med_day_y))
    
    # Render "EMT" in blue
    text_emt = font.render("EMT", True, BLUE)
    text_emt_x = text_med_day_x + text_med_day.get_width()  # position to the right of "Med-Day:"
    text_emt_y = 150  # Just a little padding from the top
    screen.blit(text_emt, (text_emt_x, text_emt_y))



def draw_highway(screen):
    road_height = 0.08 * HEIGHT
    guardrail_height = 0.01 * HEIGHT
    pygame.draw.rect(screen, ROAD_COLOR, (0, HEIGHT - road_height, WIDTH, road_height))
    pygame.draw.rect(screen, GUARDRAIL_COLOR, (0, HEIGHT - road_height, WIDTH, guardrail_height))
    pygame.draw.rect(screen, GUARDRAIL_COLOR, (0, HEIGHT - guardrail_height, WIDTH, guardrail_height))



# Ambulance properties
ambulance_img_original = pygame.image.load('amb-removebg-preview.png')
# Scale the ambulance image to make it smaller
ambulance_img = pygame.transform.scale(ambulance_img_original, (ambulance_img_original.get_width() // 4, ambulance_img_original.get_height() // 4))

ambulance_rect = ambulance_img.get_rect()
ambulance_x = WIDTH - ambulance_img.get_width()  # Start at the right edge, but consider the width of the ambulance
ambulance_y = HEIGHT - (0.23*HEIGHT)
ambulance_speed = -1  # Negative speed to move left
delay_applied = False

# Trees properties
TREES = [
    {"type": 1, "x": -25, "y": HEIGHT - 0.5*HEIGHT},
    {"type": 2, "x": 75, "y": HEIGHT - 0.6*HEIGHT},
    {"type": 1, "x": 600, "y": HEIGHT - 0.47*HEIGHT},
    {"type": 2, "x": 275, "y": HEIGHT - 0.63*HEIGHT},
    {"type": 3, "x": 525, "y": HEIGHT - 0.18*HEIGHT},
    {"type": 3, "x": 125, "y": HEIGHT - 0.18*HEIGHT}
]

def draw_trees(screen):
    for tree in TREES:
        if tree["type"] == 1:
            screen.blit(tree1_img, (tree["x"], tree["y"]))
        elif tree["type"] == 2:
            screen.blit(tree2_img, (tree["x"], tree["y"]))
        elif tree["type"] == 3:
            screen.blit(tree3_img, (tree["x"], tree["y"]))


# Main loop
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Night Scene with Ambulance")

# Load and scale down tree images after initializing the video mode
tree1_img_original = pygame.image.load('tree1.png').convert_alpha()
tree1_img = pygame.transform.scale(tree1_img_original, (tree1_img_original.get_width() // 2, tree1_img_original.get_height() // 2))  # Scaling to half the original size

tree2_img_original = pygame.image.load('tree2.png').convert_alpha()
tree2_img = pygame.transform.scale(tree2_img_original, (tree2_img_original.get_width() // 1.2, tree2_img_original.get_height()))

tree3_img_original = pygame.image.load('bush.png').convert_alpha()
tree3_img = pygame.transform.scale(tree3_img_original, (tree3_img_original.get_width() // 4, tree3_img_original.get_height() // 4))  # Scaling to half the original size

running = True
while running:
    screen.fill(BLACK)
    driving = True
    draw_moon(screen)
    update_stars()
    draw_stars(screen)
    draw_trees(screen)
    draw_highway(screen)
    draw_title_text(screen)
    draw_rounded_rect(screen, (BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT), BLUE, 15, BUTTON_OUTLINE_COLOR, BUTTON_OUTLINE_WIDTH)
    draw_button_text(screen, "Play Game", (BUTTON_X + BUTTON_WIDTH // 2, BUTTON_Y + BUTTON_HEIGHT // 2), 50, BUTTON_OUTLINE_COLOR)

    
    # Update ambulance position
    ambulance_bounce_time += 0.02  # Increase to adjust speed
    ambulance_y_offset = math.sin(ambulance_bounce_time) * ambulance_bounce_amplitude
    ambulance_x_offset = math.cos(ambulance_bounce_time) * ambulance_sway_amplitude
    screen.blit(ambulance_img, (ambulance_x + ambulance_x_offset, ambulance_y + ambulance_y_offset))
    # Update ambulance position
    if driving:
        ambulance_x += ambulance_speed
        if ambulance_x > WIDTH:
            if not fade_out_started:
                fade_out_started = True
                fade_out_start_time = pygame.time.get_ticks()
    else:
        ambulance_bounce_time += 0.02  # Increase to adjust speed
        ambulance_y_offset = math.sin(ambulance_bounce_time) * ambulance_bounce_amplitude
        ambulance_x_offset = math.cos(ambulance_bounce_time) * ambulance_sway_amplitude
        screen.blit(ambulance_img, (ambulance_x + ambulance_x_offset, ambulance_y + ambulance_y_offset))


        # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:  # Check for a mouse click
            if event.button == 1:  # Left mouse button
                button_rect = pygame.Rect(BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT)
                if button_rect.collidepoint(event.pos):
                    click_sound.play()  # Play the sound
                    pygame.mixer.music.stop()
                    subprocess.call(["python", "dispatch.py"])

    # Fade out screen to black
    # Fade out screen to black
    if fade_out_started:
        elapsed_time = pygame.time.get_ticks() - fade_out_start_time

        if elapsed_time <= 2000:  # 2 seconds for full fade
            alpha_value = min((elapsed_time / 2000.0) * 255, 255)
            fade_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            fade_surface.fill((0, 0, 0, alpha_value))
            screen.blit(fade_surface, (0, 0))




    pygame.display.flip()

pygame.quit()
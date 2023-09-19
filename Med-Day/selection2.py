import pygame
import random
import math

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Game Over Screen')

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_GRAY = (0, 40, 250)  # For rain
DARK_GREEN = (0, 100, 0)  # For grass
BROWN = (139, 69, 19)     # For dirt

# Load assets
FONT_FILE = 'font1.ttf'  # Replace with the name of your font file
GRAVESTONE_SCALE = 0.3  # adjust as needed
TREE_SCALE = 0.5  # adjust as needed
TREE2_SCALE = 1  # adjust as needed

# Load and scale assets
GRAVESTONE = pygame.image.load('gravestone.png')
GRAVESTONE = pygame.transform.scale(GRAVESTONE, (int(GRAVESTONE.get_width() * GRAVESTONE_SCALE), int(GRAVESTONE.get_height() * GRAVESTONE_SCALE)))

TREE = pygame.image.load('deadTree.png')
TREE = pygame.transform.scale(TREE, (int(TREE.get_width() * TREE_SCALE), int(TREE.get_height() * TREE_SCALE)))

TREE2 = pygame.image.load('deadTree2.png')
TREE2 = pygame.transform.scale(TREE2, (int(TREE2.get_width() * TREE2_SCALE), int(TREE2.get_height() * TREE2_SCALE)))

font_big = pygame.font.Font(FONT_FILE, 72)

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

class Raindrop:
    def __init__(self):
        self.x = random.randint(-150, WIDTH)
        self.y = random.randint(-20, HEIGHT)
        self.angle = random.uniform(0, 45)
        self.speed = random.randint(3, 6)
        self.dx = self.speed * math.sin(math.radians(self.angle))  # horizontal speed component
        self.dy = self.speed * math.cos(math.radians(self.angle))  # vertical speed component
    def init_position(self):
        # Only in the bottom left 1/4 of the screen
        self.x = random.randint(0, WIDTH // 4)
        self.y = random.randint(3 * HEIGHT // 4, HEIGHT)
    def move(self):
        self.x += self.dx
        self.y += self.dy

        # Handle the case where the raindrop goes off the screen
        if self.y > HEIGHT or self.x > WIDTH:
            self.x = random.randint(0, WIDTH)
            self.y = random.randint(-20, -1)
            self.angle = random.uniform(25, 45)
            self.dx = self.speed * math.sin(math.radians(self.angle))
            self.dy = self.speed * math.cos(math.radians(self.angle))
    
    def draw(self):
        end_x = self.x + self.dx
        end_y = self.y + self.dy
        pygame.draw.line(screen, DARK_GRAY, (self.x, self.y), (end_x, end_y), 2)


def draw_moon(screen):
    moon_image = pygame.image.load('moon-removebg-preview.png').convert_alpha()  # Ensure transparency is handled
    moon_image = pygame.transform.scale(moon_image, (300, 300))
    moon_x = WIDTH * 0.15 - moon_image.get_width() // 2  # Positioned on the left
    moon_y = HEIGHT * 0.2 - moon_image.get_height() // 2  # Positioned slightly lower
    screen.blit(moon_image, (moon_x, moon_y))

LIGHTNING_PROBABILITY = 0.01  # Adjust this for more/less frequent lightning
LIGHTNING_DURATION = 5  # Number of frames the lightning will be visible

def random_lightning(screen, clock):
    # If a random number between 0 and 1 is less than LIGHTNING_PROBABILITY, simulate lightning
    if random.random() < LIGHTNING_PROBABILITY:
        screen.fill(WHITE)
        pygame.display.flip()
        for _ in range(LIGHTNING_DURATION):
            clock.tick(60)

ambulance_bounce_time = 0  # to keep track of time for the sine function
ambulance_bounce_amplitude = 2  # How much the ambulance moves up and down
ambulance_sway_amplitude = 2  # How much the ambulance moves left and right
driving = False

# Ambulance properties
ambulance_img_original = pygame.image.load('amb-removebg-preview.png')
# Scale the ambulance image to make it smaller
ambulance_img = pygame.transform.scale(ambulance_img_original, (ambulance_img_original.get_width() // 4, ambulance_img_original.get_height() // 4))

ambulance_rect = ambulance_img.get_rect()
ambulance_x = WIDTH - ambulance_img.get_width()  # Start at the right edge, but consider the width of the ambulance
ambulance_y = HEIGHT - (0.23*HEIGHT)
ambulance_speed = -1  # Negative speed to move left
delay_applied = False
fade_out_started = False

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

def main():
    clock = pygame.time.Clock()
    raindrops = [Raindrop() for _ in range(100)]

    ambulance_bounce_time = 0  # to keep track of time for the sine function
    ambulance_bounce_amplitude = 2  # How much the ambulance moves up and down
    ambulance_sway_amplitude = 2  # How much the ambulance moves left and right
    driving = False

    ambulance_x = WIDTH -700 + ambulance_img.get_width()  # Start at the right edge, but consider the width of the ambulance
    ambulance_y = HEIGHT - (0.23*HEIGHT)
    ambulance_speed = -1  # Negative speed to move left

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        screen.fill(BLACK)
        draw_moon(screen)
        update_stars()
        draw_stars(screen)
        random_lightning(screen, clock)
        
        # Draw trees first so they appear behind the ground
        screen.blit(TREE, (10, HEIGHT - 5 - TREE.get_height()))
        screen.blit(TREE, (WIDTH + 50 - TREE.get_width(), HEIGHT - 10 - TREE.get_height()))
        screen.blit(TREE2, (WIDTH -200 - TREE2.get_width(), HEIGHT - 5 - TREE2.get_height()))

        # Draw ground
        pygame.draw.rect(screen, BROWN, (0, HEIGHT - 50, WIDTH, 40))
        pygame.draw.rect(screen, DARK_GREEN, (0, HEIGHT - 50, WIDTH, 10))

        # Draw gravestone
        gravestone_x = (WIDTH // 2 - GRAVESTONE.get_width() // 2)
        gravestone_y = HEIGHT - 25 - GRAVESTONE.get_height()
        screen.blit(GRAVESTONE, (gravestone_x, gravestone_y))

        # Draw "Game Over" text
        text_surf = font_big.render('GAME OVER', True, WHITE)
        text_rect = text_surf.get_rect(center=(WIDTH//2, HEIGHT//3))
        screen.blit(text_surf, text_rect)


        # Draw rain
        for drop in raindrops:
            drop.move()
            drop.draw()

        if driving:
            ambulance_x += ambulance_speed
            if ambulance_x + ambulance_img.get_width() < 0:  # Check if ambulance is off the screen
                driving = False
        else:
            ambulance_bounce_time += 0.02  # Increase to adjust speed
            ambulance_y_offset = math.sin(ambulance_bounce_time) * ambulance_bounce_amplitude
            ambulance_x_offset = math.cos(ambulance_bounce_time) * ambulance_sway_amplitude
            screen.blit(ambulance_img, (ambulance_x + ambulance_x_offset, ambulance_y + ambulance_y_offset))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()



if __name__ == "__main__":
    main()

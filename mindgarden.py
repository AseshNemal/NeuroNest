import pygame
import time
import random

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Setup screen
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("🌱 MindGarden: Relax to Grow")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)

# Load background music (MP3)
try:
    pygame.mixer.music.load("calm.mp3")
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)
except Exception as e:
    print("Error loading calm.mp3:", e)

# Load water sound effect (WAV)
try:
    water_sound = pygame.mixer.Sound("water.wav")
    water_sound.set_volume(0.6)
except:
    print("Water sound not found.")
    water_sound = None

# Load tree images
try:
    tree_small = pygame.image.load("tree_small.png").convert_alpha()
    tree_medium = pygame.image.load("tree_medium.png").convert_alpha()
    tree_large = pygame.image.load("tree_large.png").convert_alpha()
except Exception as e:
    print("Error loading tree images:", e)
    exit()

# Game state
tree_height = 100  # Logical height
blink_times = []

# Sky color stages
sky_colors = [
    (135, 206, 235),
    (100, 149, 237),
    (70, 130, 180),
    (25, 25, 112)
]

def get_sky_color(height):
    stage = min(int((height - 50) / 70), len(sky_colors) - 1)
    return sky_colors[stage]

def draw_instructions():
    lines = [
        "[C] Calm → Grow slowly 🌱",
        "[B] Blink → Water tree 💧",
        "Too many [B] → Stress → Shrink 🌿",
        "[ESC] Quit"
    ]
    for i, text in enumerate(lines):
        render = font.render(text, True, (255, 255, 255))
        screen.blit(render, (10, 10 + i * 24))

def draw_tree(height):
    # Select appropriate image
    if height <= 120:
        img = tree_small
    elif height <= 220:
        img = tree_medium
    else:
        img = tree_large

    # 🌱 Tiny starting scale: 0.02 → max 0.8
    scale_factor = (height - 50) / 250  # range 0–1
    scale_factor = max(0.02, min(0.8, scale_factor))  # clamp

    width = int(img.get_width() * scale_factor)
    height_scaled = int(img.get_height() * scale_factor)
    img_scaled = pygame.transform.smoothscale(img, (width, height_scaled))

    x = (600 - width) // 2
    y = 400 - height_scaled
    screen.blit(img_scaled, (x, y))



# Leaves animation
class Leaf:
    def __init__(self):
        self.x = random.randint(0, 600)
        self.y = random.randint(-100, -20)
        self.size = random.randint(10, 20)
        self.speed = random.uniform(0.3, 1)

    def update(self):
        self.y += self.speed
        self.x += random.uniform(-0.2, 0.2)
        if self.y > 420:
            self.y = random.randint(-100, -20)
            self.x = random.randint(0, 600)

    def draw(self):
        pygame.draw.ellipse(screen, (34, 139, 34), (self.x, self.y, self.size, self.size // 2))

# Water drops
class WaterDrop:
    def __init__(self, x, y):
        self.x = x + random.randint(-10, 10)
        self.y = y
        self.size = random.randint(5, 10)
        self.speed = random.uniform(2, 4)
        self.alpha = 255
        self.surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA)

    def update(self):
        self.y += self.speed
        self.alpha -= 10
        if self.alpha < 0:
            self.alpha = 0
        self.surface.fill((0, 0, 255, self.alpha))

    def draw(self):
        screen.blit(self.surface, (self.x, self.y))

# Animation lists
leaves = [Leaf() for _ in range(20)]
water_drops = []

# Game loop
running = True
while running:
    screen.fill(get_sky_color(tree_height))
    draw_instructions()
    draw_tree(tree_height)

    for leaf in leaves:
        leaf.update()
        leaf.draw()

    for drop in water_drops[:]:
        drop.update()
        drop.draw()
        if drop.alpha <= 0:
            water_drops.remove(drop)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    current_time = time.time()

    # Remove old blinks (>3 sec ago)
    blink_times = [t for t in blink_times if current_time - t < 3]

    if keys[pygame.K_c]:
        tree_height += 0.4  # Calm growth

    if keys[pygame.K_b]:
        blink_times.append(current_time)
        if len(blink_times) > 4:
            tree_height -= 2.5  # Shrink due to stress
        else:
            tree_height += 3.5  # Watering boost
            if water_sound:
                water_sound.play()
            water_drops.append(WaterDrop(300, 400 - int(tree_height) - 20))

    tree_height = max(50, min(300, tree_height))  # Clamp range

    if keys[pygame.K_ESCAPE]:
        running = False

    pygame.display.flip()
    clock.tick(30)

pygame.quit()

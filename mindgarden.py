import pygame
import os
import time
import random

# Initialize Pygame and mixer
pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("🌱 MindGarden: Relax to Grow")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 28)

# Load static tree images
try:
    tree_small = pygame.image.load("tree_small.png").convert_alpha()
    tree_medium = pygame.image.load("tree_medium.png").convert_alpha()
    tree_large = pygame.image.load("tree_large.png").convert_alpha()
except Exception as e:
    print("Static tree images missing:", e)
    tree_small = tree_medium = tree_large = None

# Load animated frames: frames 34-99 then 1-33 for looping
FRAME_FOLDER = "frames"
animated_frames = []
for i in list(range(34, 100)) + list(range(1, 34)):
    try:
        path = os.path.join(FRAME_FOLDER, f"frame_{i:03}.png")
        animated_frames.append(pygame.image.load(path).convert_alpha())
    except Exception as e:
        print(f"Missing frame {i}: {e}")

# Load background music (optional)
try:
    pygame.mixer.music.load("calm.mp3")
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)
except Exception:
    pass

# Load water sound
try:
    water_sound = pygame.mixer.Sound("water.wav")
    water_sound.set_volume(0.6)
except:
    water_sound = None

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

def draw_instructions(lines):
    for i, text in enumerate(lines):
        render = font.render(text, True, (255, 255, 255))
        screen.blit(render, (10, 10 + i * 24))

def draw_tree_static(height):
    if not tree_small or not tree_medium or not tree_large:
        return

    if height <= 150:
        # Small tree only
        img = tree_small
        scale = 0.6 + (height - 50) / 100 * 0.4  # 0.6 to 1.0
        width = int(img.get_width() * scale)
        height_scaled = int(img.get_height() * scale)
        img_scaled = pygame.transform.smoothscale(img, (width, height_scaled))
        x = (600 - width) // 2
        y = 400 - height_scaled
        screen.blit(img_scaled, (x, y))

    elif 150 < height <= 210:
        # Blend small → medium
        t = (height - 150) / 60  # 0 to 1
        img1 = tree_small
        img2 = tree_medium

        scale1 = 1.0 - t * 0.1       # 1.0 to 0.9
        scale2 = 0.9 + t * 0.1       # 0.9 to 1.0

        width1 = int(img1.get_width() * scale1)
        height1 = int(img1.get_height() * scale1)
        img1_scaled = pygame.transform.smoothscale(img1, (width1, height1))
        img1_scaled.set_alpha(int(255 * (1 - t)))

        width2 = int(img2.get_width() * scale2)
        height2 = int(img2.get_height() * scale2)
        img2_scaled = pygame.transform.smoothscale(img2, (width2, height2))
        img2_scaled.set_alpha(int(255 * t))

        x1 = (600 - width1) // 2
        y1 = 400 - height1
        x2 = (600 - width2) // 2
        y2 = 400 - height2

        screen.blit(img1_scaled, (x1, y1))
        screen.blit(img2_scaled, (x2, y2))

    elif 210 < height <= 280:
        # Blend medium → large
        t = (height - 210) / 70  # 0 to 1
        img1 = tree_medium
        img2 = tree_large

        scale1 = 1.0 - t * 0.1       # 1.0 to 0.9
        scale2 = 0.9 + t * 0.1       # 0.9 to 1.0

        width1 = int(img1.get_width() * scale1)
        height1 = int(img1.get_height() * scale1)
        img1_scaled = pygame.transform.smoothscale(img1, (width1, height1))
        img1_scaled.set_alpha(int(255 * (1 - t)))

        width2 = int(img2.get_width() * scale2)
        height2 = int(img2.get_height() * scale2)
        img2_scaled = pygame.transform.smoothscale(img2, (width2, height2))
        img2_scaled.set_alpha(int(255 * t))

        x1 = (600 - width1) // 2
        y1 = 400 - height1
        x2 = (600 - width2) // 2
        y2 = 400 - height2

        screen.blit(img1_scaled, (x1, y1))
        screen.blit(img2_scaled, (x2, y2))

    else:
        # Large tree only
        img = tree_large
        scale = 1.0
        width = int(img.get_width() * scale)
        height_scaled = int(img.get_height() * scale)
        img_scaled = pygame.transform.smoothscale(img, (width, height_scaled))
        x = (600 - width) // 2
        y = 400 - height_scaled
        screen.blit(img_scaled, (x, y))


def draw_animated_frame(frame_index):
    if not animated_frames:
        return
    frame = animated_frames[frame_index]
    rect = frame.get_rect(center=(300, 300))
    screen.blit(frame, rect)

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

# Water drops animation
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

leaves = [Leaf() for _ in range(20)]
water_drops = []

def show_start_menu():
    selecting = True
    while selecting:
        screen.fill((30, 100, 160))
        lines = [
            "Welcome to 🌿 MindGarden",
            "Choose tree mode:",
            "[1] Static Tree 🌳",
            "[2] Animated Tree 🎞️",
            "[3] Animated Tree + Health Bar 💖",
            "[ESC] Quit"
        ]
        for i, line in enumerate(lines):
            txt = font.render(line, True, (255, 255, 255))
            screen.blit(txt, (50, 60 + i * 40))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "static"
                elif event.key == pygame.K_2:
                    return "animated"
                elif event.key == pygame.K_3:
                    return "health"
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

def reset_game_state():
    global blink_times, tree_height, health, frame_index, water_drops, message_show_time
    blink_times = []
    tree_height = 100
    health = 50
    frame_index = 0
    water_drops.clear()
    message_show_time = 0

mode = show_start_menu()
reset_game_state()

running = True
message_show_time = 0

while running:
    if mode == "static":
        screen.fill(get_sky_color(tree_height))
        draw_instructions([
            "[C] Calm → Grow slowly 🌱",
            "[B] Blink → Water tree 💧",
            "Too many [B] → Stress → Shrink 🌿",
            "[R] Reset",
            "[1,2,3] Change Mode",
            "[ESC] Quit"
        ])
        draw_tree_static(tree_height)

        # Show relax message if fully grown
        if tree_height >= 300:
            if message_show_time == 0:
                message_show_time = time.time()
            elif time.time() - message_show_time < 3:
                txt = font.render("🌟 You are relaxed now! 🌟", True, (255, 255, 0))
                screen.blit(txt, (170, 50))
        else:
            message_show_time = 0

    elif mode == "animated":
        screen.fill((40, 120, 180))
        draw_instructions([
            "[C] Calm → Tree grows",
            "[B] Blink → Tree grows/shrinks",
            "[R] Reset",
            "[1,2,3] Change Mode",
            "[ESC] Quit"
        ])
        draw_animated_frame(frame_index)

        # Relax message
        if frame_index == len(animated_frames) - 1:
            if message_show_time == 0:
                message_show_time = time.time()
            elif time.time() - message_show_time < 3:
                txt = font.render("🌟 You are relaxed now! 🌟", True, (255, 255, 0))
                screen.blit(txt, (170, 50))
        else:
            message_show_time = 0

    elif mode == "health":
        screen.fill((30, 110, 150))
        draw_instructions([
            "[C] Calm → Health +",
            "[B] Blink → Health grows/shrinks",
            "[R] Reset",
            "[1,2,3] Change Mode",
            "[ESC] Quit"
        ])
        draw_animated_frame(frame_index)
        # Draw health bar background
        pygame.draw.rect(screen, (180, 180, 180), (200, 360, 200, 20))
        # Draw current health
        pygame.draw.rect(screen, (0, 255, 0), (200, 360, 2 * health, 20))
        txt = font.render(f"Health: {health}/100", True, (255, 255, 255))
        screen.blit(txt, (240, 330))

        if health >= 100:
            if message_show_time == 0:
                message_show_time = time.time()
            elif time.time() - message_show_time < 3:
                txt = font.render("🌟 You are relaxed now! 🌟", True, (255, 255, 0))
                screen.blit(txt, (170, 50))
        else:
            message_show_time = 0

    # Leaves animation
    for leaf in leaves:
        leaf.update()
        leaf.draw()

    # Water drops animation
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

    # Remove old blink times (>3 sec ago)
    blink_times = [t for t in blink_times if current_time - t < 3]

    if keys[pygame.K_ESCAPE]:
        running = False

    if keys[pygame.K_r]:
        reset_game_state()

    # Mode switching in-game
    if keys[pygame.K_1]:
        mode = "static"
        reset_game_state()
    elif keys[pygame.K_2]:
        mode = "animated"
        reset_game_state()
    elif keys[pygame.K_3]:
        mode = "health"
        reset_game_state()

    # Game logic for each mode

    # Calm always grows
    if keys[pygame.K_c]:
        if mode == "static":
            tree_height += 0.4
        elif mode == "animated":
            if frame_index < len(animated_frames) - 1:
                frame_index += 1
        elif mode == "health":
            if health < 100:
                health += 1
            if frame_index < len(animated_frames) - 1:
                frame_index += 1

    # Blink grows or shrinks based on blink frequency, same logic for all modes
    if keys[pygame.K_b]:
        blink_times.append(current_time)
        if len(blink_times) > 4:
            # Too many blinks → shrink/stress
            if mode == "static":
                tree_height -= 2.5
            elif mode == "animated":
                frame_index = max(0, frame_index - 2)
            elif mode == "health":
                health = max(0, health - 3)
                frame_index = max(0, frame_index - 2)
        else:
            # Moderate blinks → grow/water
            if mode == "static":
                tree_height += 3.5
                if water_sound:
                    water_sound.play()
                water_drops.append(WaterDrop(300, 400 - int(tree_height) - 20))
            elif mode == "animated":
                frame_index = min(len(animated_frames) - 1, frame_index + 2)
                if water_sound:
                    water_sound.play()
                water_drops.append(WaterDrop(300, 400 - frame_index - 20))
            elif mode == "health":
                health = min(100, health + 1)
                frame_index = min(len(animated_frames) - 1, frame_index + 1)
                if water_sound:
                    water_sound.play()
                water_drops.append(WaterDrop(300, 400 - frame_index - 20))

    # Clamp values to valid ranges
    if mode == "static":
        tree_height = max(50, min(300, tree_height))
    elif mode == "animated":
        frame_index = max(0, min(len(animated_frames) - 1, frame_index))
    elif mode == "health":
        health = max(0, min(100, health))
        frame_index = max(0, min(len(animated_frames) - 1, frame_index))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()

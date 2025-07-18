import pygame
import os
import time
import random

# Initialize Pygame and mixer
pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((1100, 700))  # Updated window size
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
    stage = min(int((height - 10) / 8), len(sky_colors) - 1)  # Adjusted for 10-42 range
    return sky_colors[stage]

def get_tree_stage(height):
    if height <= 20:
        return "🌱 Small Tree"
    elif height <= 30:
        return "🌳 Medium Tree"
    else:
        return "🌲 Large Tree"

def get_current_scale(height):
    """Return the current scale factor for the tree at given height"""
    # Original image dimensions:
    # Tree Small: 1417 × 1317 pixels
    # Tree Medium: 283 × 301 pixels  
    # Tree Large: 283 × 269 pixels
    
    if height <= 20:
        # Tree 1: 170×158 to 382×355 pixels
        # Scale range: 0.12 to 0.27 (based on width: 170/1417 to 382/1417)
        progress = (height - 10) / 10
        return 0.12 + progress * 0.15
    elif 20 < height <= 30:
        # Tree 2: 339×361 to 424×551 pixels
        # Scale range: 1.20 to 1.50 (based on width: 339/283 to 424/283)
        progress = (height - 20) / 10
        return 1.20 + progress * 0.30
    else:
        # Tree 3: 432×411 to 631×600 pixels
        # Scale range: 1.53 to 2.23 (based on width: 432/283 to 631/283)
        progress = min((height - 30) / 12, 1.0)
        return 1.53 + progress * 0.70

def draw_instructions(lines):
    for i, text in enumerate(lines):
        render = font.render(text, True, (255, 255, 255))
        screen.blit(render, (10, 10 + i * 24))

def draw_tree_testing(tree_type, scale):
    """Draw individual tree for testing with precise scale control"""
    if tree_type == 1 and tree_small:
        img = tree_small
        # Tree 1 target range: 170×158 to 382×355 pixels
        # Original: 1417 × 1317, so scale range: 0.12 to 0.27
        actual_scale = 0.12 + (scale - 0.5) * 0.3  # Map 0.5-5.5 input to 0.12-0.27
        actual_scale = max(0.05, min(0.5, actual_scale))  # Safety bounds
    elif tree_type == 2 and tree_medium:
        img = tree_medium
        # Tree 2 target range: 339×361 to 424×551 pixels
        # Original: 283 × 301, so scale range: 1.20 to 1.50
        actual_scale = 1.0 + (scale - 0.5) * 0.2  # Map 0.5-5.5 input to 1.0-2.0
        actual_scale = max(0.5, min(3.0, actual_scale))  # Safety bounds
    elif tree_type == 3 and tree_large:
        img = tree_large
        # Tree 3 target range: 432×411 to 631×600 pixels
        # Original: 283 × 269, so scale range: 1.53 to 2.23
        actual_scale = 1.2 + (scale - 0.5) * 0.4  # Map 0.5-5.5 input to 1.2-3.2
        actual_scale = max(0.5, min(4.0, actual_scale))  # Safety bounds
    else:
        return
    
    # Calculate dimensions
    width = int(img.get_width() * actual_scale)
    height_scaled = int(img.get_height() * actual_scale)
    
    # Safety check for screen bounds
    max_width = 800
    max_height = 600
    if width > max_width:
        actual_scale = max_width / img.get_width()
        width = max_width
        height_scaled = int(img.get_height() * actual_scale)
    if height_scaled > max_height:
        actual_scale = max_height / img.get_height()
        width = int(img.get_width() * actual_scale)
        height_scaled = max_height
        
    img_scaled = pygame.transform.smoothscale(img, (width, height_scaled))
    x = (1100 - width) // 2  # Center in window
    y = 400 - height_scaled  # Position above center
    screen.blit(img_scaled, (x, y))
    
    return width, height_scaled, actual_scale

def draw_tree_static(height):
    if not tree_small or not tree_medium or not tree_large:
        return

    # Single tree replacement system with test range 10-42
    # Tree 1 (small): height 10-20 (size 1-5)
    # Tree 2 (medium): height 20-30 (size 6-10) - replaces tree 1
    # Tree 3 (large): height 30-42 (size 11-15) - replaces tree 2
    
    if height <= 20:
        # Show only first tree (small), 170×158 to 382×355 pixels
        img = tree_small
        progress = (height - 10) / 10  # 0 to 1 over height 10-20
        scale = 0.12 + progress * 0.15  # 0.12 to 0.27 scale
        
        # Calculate dimensions
        width = int(img.get_width() * scale)
        height_scaled = int(img.get_height() * scale)
        
        # Safety check for window bounds
        max_width = 1100
        max_height = 750
        if width > max_width:
            scale = max_width / img.get_width()
            width = max_width
            height_scaled = int(img.get_height() * scale)
        if height_scaled > max_height:
            scale = max_height / img.get_height()
            width = int(img.get_width() * scale)
            height_scaled = max_height
            
        img_scaled = pygame.transform.smoothscale(img, (width, height_scaled))
        x = (1100 - width) // 2  # Center in window
        y = 700 - height_scaled
        screen.blit(img_scaled, (x, y))
        
    elif 20 < height <= 30:
        # Show only second tree (medium), 339×361 to 424×551 pixels
        img = tree_medium
        progress = (height - 20) / 10  # 0 to 1 over height 20-30
        scale = 1.20 + progress * 0.30  # 1.20 to 1.50 scale
        
        # Calculate dimensions
        width = int(img.get_width() * scale)
        height_scaled = int(img.get_height() * scale)
        
        # Safety check for window bounds
        max_width = 1100
        max_height = 750
        if width > max_width:
            scale = max_width / img.get_width()
            width = max_width
            height_scaled = int(img.get_height() * scale)
        if height_scaled > max_height:
            scale = max_height / img.get_height()
            width = int(img.get_width() * scale)
            height_scaled = max_height
            
        img_scaled = pygame.transform.smoothscale(img, (width, height_scaled))
        x = (1100 - width) // 2  # Center in window
        y = 700 - height_scaled
        screen.blit(img_scaled, (x, y))
        
    else:  # height > 30
        # Show only third tree (large), 432×411 to 631×600 pixels
        img = tree_large
        progress = min((height - 30) / 12, 1.0)  # 0 to 1, height 30-42
        scale = 1.53 + progress * 0.70  # 1.53 to 2.23 scale
        
        # Calculate dimensions
        width = int(img.get_width() * scale)
        height_scaled = int(img.get_height() * scale)
        
        # Safety check for window bounds
        max_width = 1050
        max_height = 680
        if width > max_width:
            scale = max_width / img.get_width()
            width = max_width
            height_scaled = int(img.get_height() * scale)
        if height_scaled > max_height:
            scale = max_height / img.get_height()
            width = int(img.get_width() * scale)
            height_scaled = max_height
            
        img_scaled = pygame.transform.smoothscale(img, (width, height_scaled))
        x = (1100 - width) // 2  # Center in window
        y = 700 - height_scaled
        screen.blit(img_scaled, (x, y))


def draw_animated_frame(frame_index):
    if not animated_frames:
        return
    frame = animated_frames[frame_index]
    rect = frame.get_rect(center=(550, 350))  # Center in window
    screen.blit(frame, rect)

# Leaves animation
class Leaf:
    def __init__(self):
        self.x = random.randint(0, 1100)  # Window width
        self.y = random.randint(-100, -20)
        self.size = random.randint(10, 20)
        self.speed = random.uniform(0.3, 1)

    def update(self):
        self.y += self.speed
        self.x += random.uniform(-0.2, 0.2)
        if self.y > 720:  # Window height
            self.y = random.randint(-100, -20)
            self.x = random.randint(0, 1100)

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
            "[4] 🔧 Tree Testing Mode",
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
                elif event.key == pygame.K_4:
                    return "testing"
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

def reset_game_state():
    global blink_times, tree_height, health, frame_index, water_drops, message_show_time
    global test_tree_type, test_scale  # Add testing variables
    blink_times = []
    tree_height = 10  # Start at minimum height for testing (10-42 range)
    health = 50
    frame_index = 0
    water_drops.clear()
    message_show_time = 0
    test_tree_type = 1  # Start with tree 1
    test_scale = 0.5    # Start with small scale

mode = show_start_menu()
reset_game_state()

# Initialize testing variables
test_tree_type = 1
test_scale = 0.5

running = True
message_show_time = 0

while running:
    if mode == "static":
        screen.fill(get_sky_color(tree_height))
        draw_instructions([
            "[C] Calm → Grow tree slowly 🌱",
            "[B] Blink → Water tree 💧",
            "Too many [B] → Stress → Shrink 🌿",
            "Tree evolves: Small→Medium→Large",
            f"Current stage: {get_tree_stage(tree_height)}",
            f"🔢 Height: {tree_height:.1f} / 42",
            f"📏 Scale: {get_current_scale(tree_height):.1f}x",
            "[R] Reset",
            "[1,2,3] Change Mode",
            "[ESC] Quit"
        ])
        draw_tree_static(tree_height)
        
        # Show tree size testing info
        current_scale = get_current_scale(tree_height)
        if tree_small:  # Estimate tree image size
            estimated_width = int(tree_small.get_width() * current_scale)
            estimated_height = int(tree_small.get_height() * current_scale)
        else:
            estimated_width = int(200 * current_scale)  # Default estimate
            estimated_height = int(250 * current_scale)
            
        # Draw size info box
        info_lines = [
            f"🔍 TREE SIZE TESTING",
            f"Height: {tree_height:.1f} / 42",
            f"Scale: {current_scale:.1f}x",
            f"Size: {estimated_width}×{estimated_height}px",
            f"Stage: {get_tree_stage(tree_height)}"
        ]
        
        # Draw background for info box
        pygame.draw.rect(screen, (0, 0, 0, 128), (800, 10, 290, 140))
        for i, line in enumerate(info_lines):
            txt = font.render(line, True, (255, 255, 0))
            screen.blit(txt, (810, 20 + i * 25))
            
        # Draw growth progress bar
        pygame.draw.rect(screen, (50, 50, 50), (800, 160, 290, 30))
        progress_width = int(290 * (tree_height - 10) / 32)  # 32 = total range (42-10)
        color = (0, 255, 0) if tree_height < 20 else (255, 165, 0) if tree_height < 30 else (255, 0, 0)
        pygame.draw.rect(screen, color, (800, 160, progress_width, 30))
        
        # Progress labels
        progress_text = f"Progress: {((tree_height - 10) / 32 * 100):.0f}%"
        txt = font.render(progress_text, True, (255, 255, 255))
        screen.blit(txt, (810, 200))

        # Show relax message if fully evolved (largest tree at max size)
        if tree_height >= 42:
            if message_show_time == 0:
                message_show_time = time.time()
            elif time.time() - message_show_time < 3:
                txt = font.render("🌟 Your tree has fully evolved! 🌟", True, (255, 255, 0))
                screen.blit(txt, (160, 50))
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
        pygame.draw.rect(screen, (180, 180, 180), (450, 660, 200, 20))  # Adjusted for smaller window
        # Draw current health
        pygame.draw.rect(screen, (0, 255, 0), (450, 660, 2 * health, 20))
        txt = font.render(f"Health: {health}/100", True, (255, 255, 255))
        screen.blit(txt, (490, 630))

        if health >= 100:
            if message_show_time == 0:
                message_show_time = time.time()
            elif time.time() - message_show_time < 3:
                txt = font.render("🌟 You are relaxed now! 🌟", True, (255, 255, 0))
                screen.blit(txt, (170, 50))
        else:
            message_show_time = 0

    elif mode == "testing":
        screen.fill((20, 20, 40))  # Dark background for testing
        
        # Draw testing instructions
        draw_instructions([
            "🔧 TREE TESTING MODE",
            f"Current: Tree {test_tree_type} ({'Small' if test_tree_type==1 else 'Medium' if test_tree_type==2 else 'Large'})",
            f"Scale: {test_scale:.1f}x",
            "[Q/A] Change Tree Type (1/2/3)",
            "[W/S] Scale +/- 0.1",
            "[E/D] Scale +/- 0.5", 
            "[R] Reset to defaults",
            "[1,2,3,4] Change Mode",
            "[ESC] Quit"
        ])
        
        # Draw the current test tree
        tree_info = draw_tree_testing(test_tree_type, test_scale)
        if tree_info:
            width, height, actual_scale = tree_info
            
            # Draw detailed testing info
            info_lines = [
                f"🔍 TREE {test_tree_type} TESTING",
                f"Input Scale: {test_scale:.1f}x",
                f"Actual Scale: {actual_scale:.2f}x",
                f"Size: {width}×{height}px",
                f"Tree Type: {'Small' if test_tree_type==1 else 'Medium' if test_tree_type==2 else 'Large'}"
            ]
            
            # Draw info box
            pygame.draw.rect(screen, (0, 0, 0, 200), (20, 250, 350, 150))
            for i, line in enumerate(info_lines):
                txt = font.render(line, True, (255, 255, 0))
                screen.blit(txt, (30, 260 + i * 25))

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
    elif keys[pygame.K_4]:
        mode = "testing"
        reset_game_state()

    # Testing mode controls
    if mode == "testing":
        if keys[pygame.K_q]:
            test_tree_type = max(1, test_tree_type - 1)
            time.sleep(0.1)  # Prevent rapid changes
        elif keys[pygame.K_a]:
            test_tree_type = min(3, test_tree_type + 1)
            time.sleep(0.1)
        elif keys[pygame.K_w]:
            test_scale += 0.1
            time.sleep(0.1)
        elif keys[pygame.K_s]:
            test_scale = max(0.1, test_scale - 0.1)
            time.sleep(0.1)
        elif keys[pygame.K_e]:
            test_scale += 0.5
            time.sleep(0.1)
        elif keys[pygame.K_d]:
            test_scale = max(0.1, test_scale - 0.5)
            time.sleep(0.1)

    # Game logic for each mode

    # Calm always grows
    if keys[pygame.K_c]:
        if mode == "static":
            tree_height += 0.5  # Slower, more gradual growth (2 by 2 steps)
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
                tree_height -= 0.5  # Slower shrinking too
            elif mode == "animated":
                frame_index = max(0, frame_index - 2)
            elif mode == "health":
                health = max(0, health - 3)
                frame_index = max(0, frame_index - 2)
        else:
            # Moderate blinks → grow/water
            if mode == "static":
                tree_height += 0.7  # Slightly faster than calm, but still gradual
                if water_sound:
                    water_sound.play()
                water_drops.append(WaterDrop(550, 700 - int(tree_height) - 20))  # Center of window
            elif mode == "animated":
                frame_index = min(len(animated_frames) - 1, frame_index + 2)
                if water_sound:
                    water_sound.play()
                water_drops.append(WaterDrop(550, 700 - frame_index - 20))  # Center of window
            elif mode == "health":
                health = min(100, health + 1)
                frame_index = min(len(animated_frames) - 1, frame_index + 1)
                if water_sound:
                    water_sound.play()
                water_drops.append(WaterDrop(550, 700 - frame_index - 20))  # Center of window

    # Clamp values to valid ranges
    if mode == "static":
        tree_height = max(10, min(42, tree_height))  # Test range 10-42
    elif mode == "animated":
        frame_index = max(0, min(len(animated_frames) - 1, frame_index))
    elif mode == "health":
        health = max(0, min(100, health))
        frame_index = max(0, min(len(animated_frames) - 1, frame_index))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()

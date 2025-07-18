import pygame
import os
import time
import random

# Initialize Pygame and mixer
pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((1100, 700))  # Updated window size
pygame.display.set_caption("MindGarden: Relax to Grow")
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
        return "Small Tree"
    elif height <= 30:
        return "Medium Tree"
    else:
        return "Large Tree"

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
    device_connected = False  # Simulate device connection status
    
    while selecting:
        # Gradient background
        screen.fill((15, 25, 50))
        
        # Draw gradient effect
        for y in range(700):
            color_factor = y / 700
            color = (
                int(15 + color_factor * 25),
                int(25 + color_factor * 75), 
                int(50 + color_factor * 110)
            )
            pygame.draw.line(screen, color, (0, y), (1100, y))
        
        # Title section with larger, styled text
        title_font = pygame.font.SysFont(None, 64)
        subtitle_font = pygame.font.SysFont(None, 32)
        
        # Main title with shadow effect
        shadow_text = title_font.render("* MindGarden *", True, (20, 20, 20))
        main_text = title_font.render("* MindGarden *", True, (120, 255, 120))
        screen.blit(shadow_text, (552, 82))
        screen.blit(main_text, (550, 80))
        
        # Subtitle
        subtitle = subtitle_font.render("Brain-Controlled Relaxation Experience", True, (180, 220, 180))
        subtitle_rect = subtitle.get_rect(center=(550, 130))
        screen.blit(subtitle, subtitle_rect)
        
        # Decorative elements
        pygame.draw.circle(screen, (80, 150, 80, 100), (200, 200), 40, 2)
        pygame.draw.circle(screen, (80, 150, 80, 100), (900, 250), 30, 2)
        pygame.draw.circle(screen, (80, 150, 80, 100), (150, 400), 25, 2)
        
        # Device status panel
        status_y = 180
        panel_rect = pygame.Rect(350, status_y - 10, 400, 80)
        pygame.draw.rect(screen, (40, 60, 90, 180), panel_rect)
        pygame.draw.rect(screen, (100, 150, 200), panel_rect, 2)
        
        # Device status with icon
        if device_connected:
            status_icon = "[ON]"
            status_text = "EEG Device: Connected"
            status_color = (100, 255, 100)
            detail_text = "Ready for brain-computer interface"
        else:
            status_icon = "[OFF]"
            status_text = "EEG Device: Not Connected"
            status_color = (255, 120, 120)
            detail_text = "Using keyboard simulation mode"
        
        status_full = f"{status_icon} {status_text}"
        status_render = subtitle_font.render(status_full, True, status_color)
        status_rect = status_render.get_rect(center=(550, status_y + 15))
        screen.blit(status_render, status_rect)
        
        detail_render = font.render(detail_text, True, (200, 200, 200))
        detail_rect = detail_render.get_rect(center=(550, status_y + 40))
        screen.blit(detail_render, detail_rect)
        
        # Mode selection section
        mode_y = 320
        mode_title = subtitle_font.render("Select Experience Mode:", True, (220, 220, 220))
        mode_rect = mode_title.get_rect(center=(550, mode_y))
        screen.blit(mode_title, mode_rect)
        
        # Mode options with boxes
        modes = [
            ("1", ">> Static Tree Evolution", "Watch your tree grow through mindful breathing"),
            ("2", ">> Animated Meditation", "Interactive animation responds to your calm state"),
            ("3", ">> Health & Wellness", "Track your relaxation progress with health metrics")
        ]
        
        for i, (key, title, desc) in enumerate(modes):
            y_pos = mode_y + 60 + i * 80
            
            # Mode box
            box_rect = pygame.Rect(200, y_pos - 25, 700, 60)
            pygame.draw.rect(screen, (30, 50, 80, 150), box_rect)
            pygame.draw.rect(screen, (120, 180, 220), box_rect, 2)
            
            # Key indicator
            key_circle = pygame.Rect(220, y_pos - 15, 40, 40)
            pygame.draw.circle(screen, (80, 120, 180), key_circle.center, 20)
            key_text = subtitle_font.render(key, True, (255, 255, 255))
            key_rect = key_text.get_rect(center=key_circle.center)
            screen.blit(key_text, key_rect)
            
            # Mode title and description
            title_render = font.render(title, True, (255, 255, 255))
            screen.blit(title_render, (280, y_pos - 10))
            
            desc_render = pygame.font.SysFont(None, 20).render(desc, True, (180, 180, 180))
            screen.blit(desc_render, (280, y_pos + 10))
        
        # Control panel
        control_y = 580
        control_panel = pygame.Rect(250, control_y - 20, 600, 100)
        pygame.draw.rect(screen, (20, 30, 50, 200), control_panel)
        pygame.draw.rect(screen, (80, 120, 160), control_panel, 2)
        
        controls = [
            f"[D] {'Disconnect' if device_connected else 'Connect'} EEG Device (Demo)",
            "[ESC] Exit Application"
        ]
        
        for i, control in enumerate(controls):
            if "[D]" in control:
                color = (255, 255, 100)  # Yellow for device control
            else:
                color = (200, 200, 200)
            
            control_render = font.render(control, True, color)
            control_rect = control_render.get_rect(center=(550, control_y + i * 25))
            screen.blit(control_render, control_rect)
        
        # Footer
        footer_text = "Developed for Brain-Computer Interface Research | Part 1: Software Prototype"
        footer_render = pygame.font.SysFont(None, 18).render(footer_text, True, (120, 120, 120))
        footer_rect = footer_render.get_rect(center=(550, 680))
        screen.blit(footer_render, footer_rect)
        
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "static", device_connected
                elif event.key == pygame.K_2:
                    return "animated", device_connected
                elif event.key == pygame.K_3:
                    return "health", device_connected
                elif event.key == pygame.K_d:
                    device_connected = not device_connected  # Toggle demo connection
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
    
    return "static", False  # Default return

def reset_game_state():
    global blink_times, tree_height, health, frame_index, water_drops, message_show_time
    blink_times = []
    tree_height = 10  # Start at minimum height for testing (10-42 range)
    health = 50
    frame_index = 0
    water_drops.clear()
    message_show_time = 0

mode, device_connected = show_start_menu()
reset_game_state()

running = True
message_show_time = 0

while running:
    if mode == "static":
        screen.fill(get_sky_color(tree_height))
        draw_instructions([
            "[C] Calm -> Grow tree slowly +",
            "[B] Blink -> Water tree ~",
            "Too many [B] -> Stress -> Shrink !",
            "Tree evolves: Small->Medium->Large",
            f"Current stage: {get_tree_stage(tree_height)}",
            f"Device: {'Connected' if device_connected else 'Keyboard Mode'}",
            "[R] Reset",
            "[1,2,3] Change Mode",
            "[ESC] Quit"
        ])
        draw_tree_static(tree_height)

        # Show relax message if fully evolved (largest tree at max size)
        if tree_height >= 42:
            if message_show_time == 0:
                message_show_time = time.time()
            elif time.time() - message_show_time < 7:
                txt = font.render("*** Your tree is fully grown! You are relaxed now! ***", True, (255, 255, 0))
                screen.blit(txt, (120, 50))
        else:
            message_show_time = 0

    elif mode == "animated":
        screen.fill((40, 120, 180))
        draw_instructions([
            "[C] Calm -> Tree grows +",
            "[B] Blink -> Tree grows/shrinks *", 
            f"Device: {'Connected' if device_connected else 'Keyboard Mode'}",
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
                txt = font.render("*** You are relaxed now! ***", True, (255, 255, 0))
                screen.blit(txt, (170, 50))
        else:
            message_show_time = 0

    elif mode == "health":
        screen.fill((30, 110, 150))
        draw_instructions([
            "[C] Calm -> Health + +",
            "[B] Blink -> Health grows/shrinks *",
            f"Device: {'Connected' if device_connected else 'Keyboard Mode'}",
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

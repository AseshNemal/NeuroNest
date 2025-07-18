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

# Sky color stages - Enhanced with more vibrant colors
sky_colors = [
    (135, 206, 250),  # Light sky blue
    (100, 149, 237),  # Cornflower blue
    (70, 130, 180),   # Steel blue
    (25, 25, 112),    # Midnight blue
    (15, 15, 80)      # Deep night blue
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
        # Enhanced leaf rendering with better colors and shape variation
        leaf_colors = [
            (34, 139, 34),   # Forest green
            (50, 205, 50),   # Lime green
            (144, 238, 144), # Light green
            (107, 142, 35),  # Olive drab
            (85, 107, 47)    # Dark olive green
        ]
        color = leaf_colors[hash(str(self.x + self.y)) % len(leaf_colors)]
        
        # Draw leaf with slight rotation effect
        leaf_points = [
            (self.x, self.y),
            (self.x + self.size, self.y + self.size // 3),
            (self.x + self.size // 2, self.y + self.size),
            (self.x - self.size // 3, self.y + self.size // 2)
        ]
        pygame.draw.polygon(screen, color, leaf_points)
        # Add a subtle highlight
        pygame.draw.polygon(screen, (min(255, color[0] + 30), min(255, color[1] + 30), min(255, color[2] + 30)), leaf_points, 1)

# Water drops animation
class WaterDrop:
    def __init__(self, x, y):
        self.x = x + random.randint(-15, 15)  # Wider spread
        self.y = y
        self.size = random.randint(8, 15)  # Larger drops
        self.speed = random.uniform(1.5, 3.5)  # Slightly slower for better visibility
        self.alpha = 255
        self.surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        self.color_variant = random.choice([
            (0, 150, 255),    # Bright blue
            (50, 200, 255),   # Light blue
            (100, 220, 255),  # Sky blue
            (0, 180, 255)     # Deep blue
        ])

    def update(self):
        self.y += self.speed
        self.alpha -= 6  # Slower fade for longer visibility
        if self.alpha < 0:
            self.alpha = 0
        
        # Create drop with glow effect
        self.surface.fill((0, 0, 0, 0))  # Clear surface
        
        # Draw outer glow
        if self.alpha > 50:
            glow_size = self.size + 3
            pygame.draw.circle(self.surface, (*self.color_variant, max(0, self.alpha // 4)), 
                             (self.size, self.size), glow_size)
        
        # Draw main drop
        pygame.draw.circle(self.surface, (*self.color_variant, self.alpha), 
                         (self.size, self.size), self.size)
        
        # Draw highlight for 3D effect
        if self.alpha > 100:
            highlight_size = max(2, self.size // 3)
            pygame.draw.circle(self.surface, (255, 255, 255, min(255, self.alpha)), 
                             (self.size - self.size//3, self.size - self.size//3), highlight_size)

    def draw(self):
        screen.blit(self.surface, (self.x - self.size, self.y - self.size))

leaves = [Leaf() for _ in range(20)]
water_drops = []

def show_start_menu():
    selecting = True
    device_connected = False  # Simulate device connection status
    
    while selecting:
        # Enhanced gradient background with more depth
        screen.fill((5, 15, 30))
        
        # Draw multi-layer gradient effect for more depth
        for y in range(700):
            color_factor = y / 700
            # Create a more complex gradient with multiple color zones
            if y < 200:
                # Top section - darker to lighter blue
                factor = y / 200
                color = (
                    int(5 + factor * 20),
                    int(15 + factor * 40),
                    int(30 + factor * 60)
                )
            elif y < 400:
                # Middle section - rich blue transition
                factor = (y - 200) / 200
                color = (
                    int(25 + factor * 15),
                    int(55 + factor * 35),
                    int(90 + factor * 50)
                )
            else:
                # Bottom section - deeper blues
                factor = (y - 400) / 300
                color = (
                    int(40 + factor * 10),
                    int(90 + factor * 20),
                    int(140 + factor * 20)
                )
            pygame.draw.line(screen, color, (0, y), (1100, y))
        
        # Add subtle animated background elements
        time_offset = time.time() * 0.5
        for i in range(8):
            x = (i * 150 + int(time_offset * 20) % 300) % 1100
            y = 100 + i * 80
            radius = 30 + int(10 * (0.5 + 0.5 * abs(((time_offset + i) % 4) - 2)))
            # Create circle surface with alpha
            circle_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            alpha = 30 + int(20 * (0.5 + 0.5 * abs(((time_offset * 0.7 + i) % 4) - 2)))
            pygame.draw.circle(circle_surface, (50, 100, 150, alpha), (radius, radius), radius, 1)
            screen.blit(circle_surface, (x - radius, y - radius))
        
        # Title section with larger, styled text
        title_font = pygame.font.SysFont(None, 64)
        subtitle_font = pygame.font.SysFont(None, 32)
        
        # Main title with shadow effect - Enhanced colors
        shadow_text = title_font.render("* MindGarden *", True, (0, 0, 0))
        main_text = title_font.render("* MindGarden *", True, (100, 255, 100))
        screen.blit(shadow_text, (552, 82))
        screen.blit(main_text, (550, 80))
        
        # Subtitle - Better color
        subtitle = subtitle_font.render("Brain-Controlled Relaxation Experience", True, (150, 255, 150))
        subtitle_rect = subtitle.get_rect(center=(550, 130))
        screen.blit(subtitle, subtitle_rect)
        
        # Decorative elements - Enhanced with pulsing effect
        pulse = 0.5 + 0.5 * abs(((time.time() * 2) % 4) - 2)  # Pulsing from 0.5 to 1.0
        # Create circle surfaces with alpha for proper transparency
        circle1_surface = pygame.Surface((int(40 + 10 * pulse) * 2 + 6, int(40 + 10 * pulse) * 2 + 6), pygame.SRCALPHA)
        color1 = (min(255, int(100 * pulse)), min(255, int(200 * pulse)), min(255, int(100 * pulse)))
        pygame.draw.circle(circle1_surface, color1, (int(40 + 10 * pulse) + 3, int(40 + 10 * pulse) + 3), int(40 + 10 * pulse), 3)
        screen.blit(circle1_surface, (200 - int(40 + 10 * pulse) - 3, 200 - int(40 + 10 * pulse) - 3))
        
        circle2_surface = pygame.Surface((int(30 + 8 * pulse) * 2 + 6, int(30 + 8 * pulse) * 2 + 6), pygame.SRCALPHA)
        color2 = (min(255, int(120 * pulse)), min(255, int(220 * pulse)), min(255, int(120 * pulse)))
        pygame.draw.circle(circle2_surface, color2, (int(30 + 8 * pulse) + 3, int(30 + 8 * pulse) + 3), int(30 + 8 * pulse), 3)
        screen.blit(circle2_surface, (900 - int(30 + 8 * pulse) - 3, 250 - int(30 + 8 * pulse) - 3))
        
        circle3_surface = pygame.Surface((int(25 + 6 * pulse) * 2 + 6, int(25 + 6 * pulse) * 2 + 6), pygame.SRCALPHA)
        color3 = (min(255, int(80 * pulse)), min(255, int(180 * pulse)), min(255, int(80 * pulse)))
        pygame.draw.circle(circle3_surface, color3, (int(25 + 6 * pulse) + 3, int(25 + 6 * pulse) + 3), int(25 + 6 * pulse), 3)
        screen.blit(circle3_surface, (150 - int(25 + 6 * pulse) - 3, 400 - int(25 + 6 * pulse) - 3))
        
        # Add floating particles
        particle_time = time.time() * 0.3
        for i in range(15):
            x = 50 + (i * 70 + int(particle_time * 30 + i * 20)) % 1000
            y = 50 + int(30 * abs(((particle_time + i * 0.5) % 4) - 2)) + i * 40
            size = 2 + int(3 * (0.5 + 0.5 * abs(((particle_time * 1.5 + i) % 4) - 2)))
            # Create particle surface with alpha
            particle_surface = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            alpha = 80 + int(40 * (0.5 + 0.5 * abs(((particle_time * 0.8 + i) % 4) - 2)))
            pygame.draw.circle(particle_surface, (150, 200, 255, alpha), (size, size), size)
            screen.blit(particle_surface, (x - size, y - size))
        
        # Device status panel - Enhanced colors
        status_y = 180
        panel_rect = pygame.Rect(350, status_y - 10, 400, 80)
        pygame.draw.rect(screen, (30, 50, 80, 200), panel_rect)
        pygame.draw.rect(screen, (120, 180, 240), panel_rect, 2)
        
        # Device status with icon - Improved colors
        if device_connected:
            status_icon = "[ON]"
            status_text = "EEG Device: Connected"
            status_color = (50, 255, 50)   # Brighter green
            detail_text = "Ready for brain-computer interface"
        else:
            status_icon = "[OFF]"
            status_text = "EEG Device: Not Connected"
            status_color = (255, 100, 100)  # Softer red
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
            
            # Mode box - Enhanced colors
            box_rect = pygame.Rect(200, y_pos - 25, 700, 60)
            pygame.draw.rect(screen, (20, 40, 70, 180), box_rect)
            pygame.draw.rect(screen, (100, 150, 255), box_rect, 2)
            
            # Key indicator - Better colors
            key_circle = pygame.Rect(220, y_pos - 15, 40, 40)
            pygame.draw.circle(screen, (60, 120, 200), key_circle.center, 20)
            key_text = subtitle_font.render(key, True, (255, 255, 255))
            key_rect = key_text.get_rect(center=key_circle.center)
            screen.blit(key_text, key_rect)
            
            # Mode title and description
            title_render = font.render(title, True, (255, 255, 255))
            screen.blit(title_render, (280, y_pos - 10))
            
            desc_render = pygame.font.SysFont(None, 20).render(desc, True, (180, 180, 180))
            screen.blit(desc_render, (280, y_pos + 10))
        
        # Control panel - Enhanced colors
        control_y = 580
        control_panel = pygame.Rect(250, control_y - 20, 600, 100)
        pygame.draw.rect(screen, (15, 25, 45, 220), control_panel)
        pygame.draw.rect(screen, (100, 140, 200), control_panel, 2)
        
        controls = [
            f"[D] {'Disconnect' if device_connected else 'Connect'} EEG Device (Demo)",
            "[ESC] Exit Application"
        ]
        
        for i, control in enumerate(controls):
            if "[D]" in control:
                color = (255, 255, 50)  # Brighter yellow for device control
            else:
                color = (220, 220, 220)  # Brighter white for other controls
            
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
        # Enhanced dynamic sky background
        sky_color = get_sky_color(tree_height)
        screen.fill(sky_color)
        
        # Add atmospheric layers for depth
        for layer in range(3):
            layer_alpha = 30 - layer * 8
            layer_offset = layer * 15
            overlay_color = (
                max(0, sky_color[0] - layer_offset),
                max(0, sky_color[1] - layer_offset),
                min(255, sky_color[2] + layer_offset),
                layer_alpha
            )
            # Create atmospheric bands
            for band in range(0, 700, 50):
                band_height = 25 + layer * 5
                pygame.draw.rect(screen, overlay_color[:3], (0, band + layer * 10, 1100, band_height))
        
        # Add subtle cloud-like effects
        cloud_time = time.time() * 0.2
        for i in range(6):
            x = (i * 200 + int(cloud_time * 40 + i * 30)) % 1200 - 100
            y = 50 + i * 100 + int(20 * abs(((cloud_time + i * 0.3) % 4) - 2))
            width = 80 + int(40 * (0.5 + 0.5 * abs(((cloud_time * 0.7 + i) % 4) - 2)))
            height = 30 + int(15 * (0.5 + 0.5 * abs(((cloud_time * 1.1 + i) % 4) - 2)))
            # Create cloud surface with alpha
            cloud_surface = pygame.Surface((width, height), pygame.SRCALPHA)
            cloud_alpha = 20 + int(15 * (0.5 + 0.5 * abs(((cloud_time * 0.9 + i) % 4) - 2)))
            pygame.draw.ellipse(cloud_surface, (255, 255, 255, cloud_alpha), (0, 0, width, height))
            screen.blit(cloud_surface, (x, y))
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
                txt = font.render("*** Your tree is fully grown! You are relaxed now! ***", True, (255, 255, 50))
                txt_rect = txt.get_rect(center=(550, 50))
                screen.blit(txt, txt_rect)
        else:
            message_show_time = 0

    elif mode == "animated":
        # Enhanced animated background with dynamic elements
        base_color = (30, 100, 160)
        screen.fill(base_color)
        
        # Add animated wave pattern
        wave_time = time.time() * 2
        for y in range(0, 700, 20):
            wave_offset = int(30 * abs(((wave_time + y * 0.01) % 8) - 4))
            # Create wave surface with alpha
            wave_surface = pygame.Surface((1100, 10), pygame.SRCALPHA)
            wave_alpha = 20 + int(10 * (0.5 + 0.5 * abs(((wave_time * 0.5 + y * 0.005) % 4) - 2)))
            pygame.draw.rect(wave_surface, (50, 150, 200, wave_alpha), (0, 0, 1100, 10))
            screen.blit(wave_surface, (wave_offset, y))
        
        # Add floating energy orbs
        orb_time = time.time() * 1.5
        for i in range(8):
            angle = orb_time + i * 0.8
            x = 550 + int(200 * abs(((angle * 0.3) % 4) - 2) - 200)
            y = 350 + int(150 * abs(((angle * 0.7) % 4) - 2) - 150)
            radius = 15 + int(10 * (0.5 + 0.5 * abs(((orb_time + i * 0.5) % 4) - 2)))
            # Create orb surface with alpha
            orb_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            alpha = 40 + int(30 * (0.5 + 0.5 * abs(((orb_time * 1.2 + i) % 4) - 2)))
            pygame.draw.circle(orb_surface, (100, 200, 255, alpha), (radius, radius), radius, 2)
            screen.blit(orb_surface, (x - radius, y - radius))
        draw_instructions([
            "[C] Calm -> Tree grows +",
            "[B] Blink -> Tree grows/shrinks *", 
            f"Device: {'Connected' if device_connected else 'Keyboard Mode'}",
            "[R] Reset",
            "[1,2,3] Change Mode",
            "[ESC] Quit"
        ])
        
        # Add white circular fade area around the animated image
        if animated_frames:
            frame = animated_frames[frame_index]
            frame_rect = frame.get_rect(center=(550, 350))
            
            # Create circular white fade effect
            circle_center = (550, 350)
            max_radius = 200  # Maximum radius of the white circle
            
            # Draw multiple circles with decreasing alpha to create fade effect
            for radius in range(max_radius, 0, -10):
                # Calculate alpha based on distance from center (closer = more white)
                alpha = int(255 * (max_radius - radius) / max_radius * 0.3)  # 0.3 controls fade intensity
                if alpha > 0:
                    # Create circle surface with alpha
                    circle_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
                    pygame.draw.circle(circle_surface, (255, 255, 255, alpha), (radius, radius), radius)
                    screen.blit(circle_surface, (circle_center[0] - radius, circle_center[1] - radius))
        
        draw_animated_frame(frame_index)

        # Relax message
        if frame_index == len(animated_frames) - 1:
            if message_show_time == 0:
                message_show_time = time.time()
            elif time.time() - message_show_time < 3:
                txt = font.render("*** You are relaxed now! ***", True, (255, 255, 50))
                txt_rect = txt.get_rect(center=(550, 50))
                screen.blit(txt, txt_rect)
        else:
            message_show_time = 0

    elif mode == "health":
        # Enhanced health mode background with wellness theme
        base_color = (20, 80, 120)
        screen.fill(base_color)
        
        # Add health-themed gradient overlay
        health_factor = health / 100.0
        for y in range(700):
            gradient_factor = y / 700
            # Health influences the background color
            health_influence = int(health_factor * 50)
            color = (
                base_color[0] + int(gradient_factor * 20) + health_influence // 3,
                base_color[1] + int(gradient_factor * 30) + health_influence // 2,
                base_color[2] + int(gradient_factor * 40) + health_influence
            )
            # Ensure colors don't exceed 255
            color = (min(255, color[0]), min(255, color[1]), min(255, color[2]))
            pygame.draw.line(screen, color, (0, y), (1100, y))
        
        # Add health pulse visualization
        pulse_time = time.time() * 3
        pulse_intensity = 0.5 + 0.5 * (pulse_time % 2)
        heart_beat = int(30 * pulse_intensity * health_factor)
        
        # Pulse rings emanating from center
        for ring in range(4):
            ring_radius = 50 + ring * 40 + heart_beat
            ring_alpha = int((40 - ring * 8) * health_factor)
            if ring_alpha > 0:
                # Create ring surface with alpha
                ring_surface = pygame.Surface((ring_radius * 2, ring_radius * 2), pygame.SRCALPHA)
                pygame.draw.circle(ring_surface, (255, 100 + heart_beat, 100, ring_alpha), (ring_radius, ring_radius), ring_radius, 3)
                screen.blit(ring_surface, (550 - ring_radius, 350 - ring_radius))
        
        # Add wellness sparkles based on health level
        sparkle_time = time.time() * 2
        num_sparkles = int(health_factor * 12)
        for i in range(num_sparkles):
            angle = sparkle_time + i * 0.5
            distance = 100 + int(50 * abs(((angle * 0.3) % 4) - 2))
            x = 550 + int(distance * abs(((angle * 0.7) % 4) - 2) - distance)
            y = 350 + int(distance * abs(((angle * 1.1) % 4) - 2) - distance)
            sparkle_size = 2 + int(3 * (0.5 + 0.5 * abs(((sparkle_time + i * 0.3) % 4) - 2)))
            alpha = int(100 * health_factor * (0.5 + 0.5 * abs(((sparkle_time * 1.5 + i) % 4) - 2)))
            if alpha > 0:
                # Create sparkle surface with alpha
                sparkle_surface = pygame.Surface((sparkle_size * 2, sparkle_size * 2), pygame.SRCALPHA)
                pygame.draw.circle(sparkle_surface, (255, 255, 100, alpha), (sparkle_size, sparkle_size), sparkle_size)
                screen.blit(sparkle_surface, (x - sparkle_size, y - sparkle_size))
        draw_instructions([
            "[C] Calm -> Health + +",
            "[B] Blink -> Health grows/shrinks *",
            f"Device: {'Connected' if device_connected else 'Keyboard Mode'}",
            "[R] Reset",
            "[1,2,3] Change Mode",
            "[ESC] Quit"
        ])
        
        # Add white circular fade area around the animated image
        if animated_frames:
            frame = animated_frames[frame_index]
            frame_rect = frame.get_rect(center=(550, 350))
            
            # Create circular white fade effect
            circle_center = (550, 350)
            max_radius = 200  # Maximum radius of the white circle
            
            # Draw multiple circles with decreasing alpha to create fade effect
            for radius in range(max_radius, 0, -10):
                # Calculate alpha based on distance from center (closer = more white)
                alpha = int(255 * (max_radius - radius) / max_radius * 0.3)  # 0.3 controls fade intensity
                if alpha > 0:
                    # Create circle surface with alpha
                    circle_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
                    pygame.draw.circle(circle_surface, (255, 255, 255, alpha), (radius, radius), radius)
                    screen.blit(circle_surface, (circle_center[0] - radius, circle_center[1] - radius))
        
        draw_animated_frame(frame_index)
        # Draw health bar background - Enhanced colors
        pygame.draw.rect(screen, (100, 100, 100), (450, 660, 200, 20))  # Darker gray background
        # Draw current health - Gradient health bar
        if health > 75:
            health_color = (0, 255, 0)      # Bright green when high
        elif health > 50:
            health_color = (255, 255, 0)    # Yellow when medium
        elif health > 25:
            health_color = (255, 165, 0)    # Orange when low
        else:
            health_color = (255, 0, 0)      # Red when very low
        
        pygame.draw.rect(screen, health_color, (450, 660, 2 * health, 20))
        txt = font.render(f"Health: {health}/100", True, (255, 255, 255))
        screen.blit(txt, (490, 630))

        if health >= 100:
            if message_show_time == 0:
                message_show_time = time.time()
            elif time.time() - message_show_time < 3:
                txt = font.render("*** You are relaxed now! ***", True, (255, 255, 50))
                txt_rect = txt.get_rect(center=(550, 50))
                screen.blit(txt, txt_rect)
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
                # Create multiple water drops for better visual effect
                for i in range(3):
                    water_drops.append(WaterDrop(550 + i * 20 - 20, 700 - int(tree_height) - 20))  # Center of window
            elif mode == "animated":
                frame_index = min(len(animated_frames) - 1, frame_index + 2)
                if water_sound:
                    water_sound.play()
                # Create multiple water drops for better visual effect
                for i in range(3):
                    water_drops.append(WaterDrop(550 + i * 20 - 20, 700 - frame_index - 20))  # Center of window
            elif mode == "health":
                health = min(100, health + 1)
                frame_index = min(len(animated_frames) - 1, frame_index + 1)
                if water_sound:
                    water_sound.play()
                # Create multiple water drops for better visual effect
                for i in range(3):
                    water_drops.append(WaterDrop(550 + i * 20 - 20, 700 - frame_index - 20))  # Center of window

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

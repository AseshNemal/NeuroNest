#!/usr/bin/env python3
import pygame
import sys

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("🔍 Tree Scaling Test")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)

# Load tree images
try:
    tree_small = pygame.image.load("tree_small.png").convert_alpha()
    tree_medium = pygame.image.load("tree_medium.png").convert_alpha() 
    tree_large = pygame.image.load("tree_large.png").convert_alpha()
    print(f"✅ Tree images loaded:")
    print(f"   Small: {tree_small.get_width()}x{tree_small.get_height()}")
    print(f"   Medium: {tree_medium.get_width()}x{tree_medium.get_height()}")
    print(f"   Large: {tree_large.get_width()}x{tree_large.get_height()}")
except Exception as e:
    print(f"❌ Error loading tree images: {e}")
    pygame.quit()
    sys.exit(1)

def draw_tree_test(height):
    """Test function identical to the main app"""
    if height <= 80:
        img = tree_small
        progress = (height - 40) / 40
        scale = 0.3 + progress * 0.5  # 0.3 to 0.8
        tree_type = "Small"
    elif 80 < height <= 120:
        img = tree_medium
        progress = (height - 80) / 40
        scale = 0.8 + progress * 0.5  # 0.8 to 1.3
        tree_type = "Medium"
    else:  # height > 120
        img = tree_large
        progress = min((height - 120) / 40, 1.0)
        scale = 1.3 + progress * 0.6  # 1.3 to 1.9
        tree_type = "Large"
    
    # Calculate dimensions
    width = int(img.get_width() * scale)
    height_scaled = int(img.get_height() * scale)
    
    # Draw the tree
    img_scaled = pygame.transform.smoothscale(img, (width, height_scaled))
    x = (600 - width) // 2
    y = 400 - height_scaled
    screen.blit(img_scaled, (x, y))
    
    return tree_type, scale, width, height_scaled

# Test different heights
test_height = 40
running = True

print("\n🌳 INTERACTIVE TREE SCALING TEST")
print("Controls:")
print("  [UP] Increase tree height")
print("  [DOWN] Decrease tree height") 
print("  [ESC] Quit")
print("\nWatch the tree size change as you press UP/DOWN!")

while running:
    screen.fill((135, 206, 235))  # Sky blue
    
    # Draw test tree
    tree_type, scale, width, height_scaled = draw_tree_test(test_height)
    
    # Show info
    info_lines = [
        f"Height: {test_height:.1f}",
        f"Tree: {tree_type}",
        f"Scale: {scale:.2f}",
        f"Size: {width}x{height_scaled}",
        "",
        "Press UP/DOWN to change size",
        "ESC to quit"
    ]
    
    for i, line in enumerate(info_lines):
        color = (255, 255, 255) if line else (255, 255, 255)
        txt = font.render(line, True, color)
        screen.blit(txt, (10, 10 + i * 25))
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_UP:
                test_height = min(160, test_height + 2)
                print(f"Height: {test_height} → {tree_type} tree, Scale: {scale:.2f}, Size: {width}x{height_scaled}")
            elif event.key == pygame.K_DOWN:
                test_height = max(40, test_height - 2)
                print(f"Height: {test_height} → {tree_type} tree, Scale: {scale:.2f}, Size: {width}x{height_scaled}")
    
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
print("\nTest completed!")

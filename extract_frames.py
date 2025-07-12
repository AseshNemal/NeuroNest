from PIL import Image
import os

# Path to the gif file
gif_path = "../../../Downloads/tenor.gif"
# Output directory for frames
output_dir = "frames"

# Create frames directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Open the gif file
with Image.open(gif_path) as im:
    frame_number = 0
    try:
        while True:
            # Save frame as PNG
            frame_path = os.path.join(output_dir, f"frame_{frame_number:03}.png")
            im.save(frame_path, format="PNG")
            frame_number += 1
            im.seek(frame_number)
    except EOFError:
        pass

print(f"Extracted {frame_number} frames from {gif_path} to {output_dir}")

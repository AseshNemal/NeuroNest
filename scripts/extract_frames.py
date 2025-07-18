from PIL import Image
import os
import sys

def extract_frames(gif_path, output_dir="frames"):
    """Extract frames from a GIF file to PNG images."""
    # Create frames directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Check if gif file exists
    if not os.path.exists(gif_path):
        print(f"Error: GIF file '{gif_path}' not found!")
        return False

    try:
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
        return True
    except Exception as e:
        print(f"Error extracting frames: {e}")
        return False

if __name__ == "__main__":
    # Default path (can be overridden by command line argument)
    default_gif_path = "../../../Downloads/tenor.gif"
    
    # Use command line argument if provided, otherwise use default
    if len(sys.argv) > 1:
        gif_path = sys.argv[1]
    else:
        gif_path = default_gif_path
        print(f"No GIF path provided, using default: {gif_path}")
    
    # Optional: specify output directory as second argument
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "frames"
    
    extract_frames(gif_path, output_dir)

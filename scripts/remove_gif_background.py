from PIL import Image
import os

def remove_background_from_frames(frames_dir):
    for filename in os.listdir(frames_dir):
        if filename.endswith(".png"):
            frame_path = os.path.join(frames_dir, filename)
            try:
                with Image.open(frame_path) as img:
                    img = img.convert("RGBA")
                    datas = img.getdata()

                    # Get background color from top-left pixel
                    bg_color = img.getpixel((0, 0))
                    
                    # Ensure bg_color is a tuple with at least 3 elements
                    if not isinstance(bg_color, (tuple, list)) or len(bg_color) < 3:
                        print(f"Warning: Skipping {filename} - invalid background color format")
                        continue

                    new_data = []
                    for item in datas:
                        # Ensure item is a tuple/list with at least 3 elements
                        if not isinstance(item, (tuple, list)) or len(item) < 3:
                            new_data.append(item)  # Keep original if format is unexpected
                            continue
                            
                        # Change all pixels that match the background color to transparent
                        if item[:3] == bg_color[:3]:
                            new_data.append((255, 255, 255, 0))
                        else:
                            new_data.append(item)

                    img.putdata(new_data)
                    img.save(frame_path)
                    print(f"Processed {filename} - background removed")
            except Exception as e:
                print(f"Error processing {filename}: {e}")

if __name__ == "__main__":
    frames_directory = "frames"
    remove_background_from_frames(frames_directory)
    print("Background removal completed for all frames.")

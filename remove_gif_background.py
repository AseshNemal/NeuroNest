from PIL import Image
import os

def remove_background_from_frames(frames_dir):
    for filename in os.listdir(frames_dir):
        if filename.endswith(".png"):
            frame_path = os.path.join(frames_dir, filename)
            with Image.open(frame_path) as img:
                img = img.convert("RGBA")
                datas = img.getdata()

                # Get background color from top-left pixel
                bg_color = img.getpixel((0, 0))

                new_data = []
                for item in datas:
                    # Change all pixels that match the background color to transparent
                    if item[:3] == bg_color[:3]:
                        new_data.append((255, 255, 255, 0))
                    else:
                        new_data.append(item)

                img.putdata(new_data)
                img.save(frame_path)
                print(f"Processed {filename} - background removed")

if __name__ == "__main__":
    frames_directory = "frames"
    remove_background_from_frames(frames_directory)
    print("Background removal completed for all frames.")

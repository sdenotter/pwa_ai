from PIL import Image

def convert_and_resize(jpeg_path, output_dir):
    """Converts a JPEG image to PNG and resizes it to 192x192 and 512x512.

    Args:
        jpeg_path: Path to the input JPEG image.
        output_dir: Directory to save the output PNG images.
    """

    try:
        img = Image.open(jpeg_path)
        img = img.convert("RGBA") # Ensure alpha channel for better icon compatibility

        # Resize and save 192x192
        img_192 = img.resize((192, 192), Image.LANCZOS) # LANCZOS for high-quality downscaling
        img_192.save(f"{output_dir}/icon_192.png")

        # Resize and save 512x512
        img_512 = img.resize((512, 512), Image.LANCZOS)
        img_512.save(f"{output_dir}/icon_512.png")

        print("Images converted and resized successfully!")

    except FileNotFoundError:
        print(f"Error: JPEG image not found at {jpeg_path}")
    except Exception as e:
        print(f"An error occurred: {e}")


# Example usage:
jpeg_file = "/home/sd/hh/static/images/necro.jpg"  # Replace with your JPEG file path
output_folder = "output_icons"  # Replace with your desired output folder

# Create the output directory if it doesn't exist
import os
print(os.listdir())
os.makedirs(output_folder, exist_ok=True)

convert_and_resize(jpeg_file, output_folder)
import os
from PIL import Image

def get_distinct_image_sizes(folder_path):
    image_sizes = set()
    valid_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp')

    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(valid_extensions):
                file_path = os.path.join(root, file)
                with Image.open(file_path) as img:
                    image_sizes.add(img.size)

    return image_sizes

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python script.py folder_path")
        sys.exit(1)

    folder_path = sys.argv[1]

    if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
        print("Invalid folder path.")
        sys.exit(1)

    distinct_sizes = get_distinct_image_sizes(folder_path)
    if not distinct_sizes:
        print("No images found in the specified folder.")
    else:
        print("Distinct image sizes:")
        for size in distinct_sizes:
            print(f"{size[0]}x{size[1]}")

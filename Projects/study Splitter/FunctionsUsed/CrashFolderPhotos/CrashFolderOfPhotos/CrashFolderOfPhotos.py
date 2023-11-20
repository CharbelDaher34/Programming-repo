import os
import shutil

def copy_photos(source_folder, destination_folder):
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    for root, dirs, files in os.walk(source_folder):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                source_file_path = os.path.join(root, file)
                destination_file_path = os.path.join(destination_folder, file)

                # Check if the file already exists in the destination folder, and avoid overwriting it
                if not os.path.exists(destination_file_path):
                    shutil.copy2(source_file_path, destination_file_path)
                    print(f"Copying '{file}' to '{destination_folder}'")

if __name__ == "__main__":
    input1_folder = "C:\\Users\\user\\Pictures"
    input2_folder = "C:\\Users\\user\\Desktop\\ComputerVisionProject\Data"

    copy_photos(input1_folder, input2_folder)


import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import shutil

def move_image(image_path, liked):
    if liked:
        folder_name = '1'
    else:
        folder_name = '0'
    
    destination_folder = os.path.join(os.path.dirname(image_path), folder_name)
    os.makedirs(destination_folder, exist_ok=True)

    # Get the file name without the extension
    file_name = os.path.splitext(os.path.basename(image_path))[0]
    # Create a new name by appending an increasing counter to the file name
    new_file_name = f"{file_name}"
    counter = 1
    while os.path.exists(os.path.join(destination_folder, f"{new_file_name}.jpg")):
        new_file_name = f"{file_name}_{counter}"
        counter += 1

    # Move the file to the destination folder with the new name
    destination_path = os.path.join(destination_folder, f"{new_file_name}.jpg")
    shutil.move(image_path, destination_path)

    # Show next image or close the main window if all images are processed
    if current_image_idx < len(image_paths):
        show_next_image()
    else:
        root.destroy()

# Function to display the next image
def show_next_image():
    global current_image_idx

    if current_image_idx < len(image_paths):
        img_path = image_paths[current_image_idx]

        try:
            img = Image.open(img_path)
            img = img.resize((400, 400))  # Resize the image for display
            img_tk = ImageTk.PhotoImage(img)
            image_label.config(image=img_tk)
            image_label.image = img_tk
            current_image_idx += 1
        except IOError:
            print(f"Error opening image: {img_path}")
            current_image_idx += 1
            show_next_image()
    else:
        root.destroy()

# Function to handle the like button (liked = 1)
def like_image():
    move_image(image_paths[current_image_idx - 1], liked=True)

# Function to handle the dislike button (liked = 0)
def dislike_image():
    move_image(image_paths[current_image_idx - 1], liked=False)

# Function to handle the window close event
def on_closing():
    # Handle the case when the user closes the main window
    if current_image_idx >= len(image_paths):
        root.destroy()

# Initialize the GUI
root = tk.Tk()
root.title("Image Liker")
root.geometry("500x500")

# Choose the directory containing the images
image_directory = filedialog.askdirectory(title="Select Image Directory")
if not image_directory:
    root.destroy()
    exit()

# Get all image file paths from the selected directory
image_paths = [os.path.join(image_directory, filename) for filename in os.listdir(image_directory)
               if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]

if not image_paths:
    root.destroy()
    print("No image files found in the selected directory.")
    exit()

# Create folders for liked and disliked images
os.makedirs(os.path.join(image_directory, '0'), exist_ok=True)
os.makedirs(os.path.join(image_directory, '1'), exist_ok=True)

current_image_idx = 0

# Display the first image
img = Image.open(image_paths[current_image_idx])
img = img.resize((400, 400))  # Resize the image for display
img_tk = ImageTk.PhotoImage(img)
image_label = tk.Label(root, image=img_tk)
image_label.pack()

# Create like and dislike buttons
like_button = tk.Button(root, text="dares (1)", command=like_image, width=20)
dislike_button = tk.Button(root, text="msh dares (0)", command=dislike_image, width=20)

like_button.pack(pady=10)
dislike_button.pack(pady=10)

# Handle the window close event
root.protocol("WM_DELETE_WINDOW", on_closing)

# Run the main loop
root.mainloop()


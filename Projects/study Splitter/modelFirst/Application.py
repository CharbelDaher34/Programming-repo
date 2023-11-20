import os
import shutil
from PIL import Image
import tensorflow as tf

# Load the pre-trained model
architecture_file = 'model_architecture.json'
weights_file = 'model_architecture_and_weights.h5'
with open(architecture_file, 'r') as f:
    model_architecture = f.read()
loaded_model = tf.keras.models.model_from_json(model_architecture)
loaded_model.load_weights(weights_file)

# Directory containing the images
image_directory = 'C:\\Users\\user\\Desktop\\New folder'

# Get all image file paths from the selected directory
image_paths = [os.path.join(image_directory, filename) for filename in os.listdir(image_directory)
               if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]

# Create folders for liked and disliked images
os.makedirs(os.path.join(image_directory, '0'), exist_ok=True)
os.makedirs(os.path.join(image_directory, '1'), exist_ok=True)

# Loop through each image and classify
for image_path in image_paths:
    img = Image.open(image_path)
    img = img.resize((480, 480))  # Resize the image to match the input size of the model
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)  # Add batch dimension

    # Predict the class (0 or 1) using the loaded model
    predictions = loaded_model.predict(img_array)
    predicted_class = int(predictions[0][0] + 0.5)  # Convert probability to class

    # Move the image to the appropriate folder
    if predicted_class == 1:
        destination_folder = os.path.join(image_directory, '1')
    else:
        destination_folder = os.path.join(image_directory, '0')

    # Get the file name without the extension
    file_name = os.path.splitext(os.path.basename(image_path))[0]
    destination_path = os.path.join(destination_folder, f"{file_name}.jpg")

    shutil.move(image_path, destination_path)

print("Image classification and moving completed.")

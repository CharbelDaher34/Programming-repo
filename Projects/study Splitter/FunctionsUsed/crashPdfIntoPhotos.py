import fitz  # PyMuPDF
import os
from PIL import Image

def convert_pdf_to_images(pdf_folder, output_folder, target_size):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Loop through each PDF file in the input folder
    for pdf_file in os.listdir(pdf_folder):
        if pdf_file.lower().endswith('.pdf'):
            pdf_path = os.path.join(pdf_folder, pdf_file)

            # Open the PDF file
            pdf_document = fitz.open(pdf_path)
            
            # Loop through each page in the PDF
            for page_num in range(pdf_document.page_count):
                page = pdf_document[page_num]
                
                # Convert the page to an image
                image = page.get_pixmap(matrix=fitz.Matrix(300/72, 300/72))  # You can adjust the resolution here

                # Convert PyMuPDF image to Pillow image
                image_pil = Image.frombytes("RGB", [image.width, image.height], image.samples)

                # Resize the image to the target size using LANCZOS resampling
                image_resized = image_pil.resize(target_size, Image.LANCZOS)
                
                # Save the resized image
                image_path = os.path.join(output_folder, f"{pdf_file}_page_{page_num + 1}.png")
                image_resized.save(image_path)

            # Close the PDF document
            pdf_document.close()

if __name__ == "__main__":
    input_folder = "C:\Users\user\Desktop\New folder"  # Provide the path to the input folder containing PDFs
    output_folder = "C:\Users\user\Desktop\New folder"  # Provide the path to the output folder where images will be saved
    target_size = (640, 640)  # Desired image size
    print("Started")
    convert_pdf_to_images(input_folder, output_folder, target_size)
    print('finished')

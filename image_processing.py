import os
import cv2

def process_images(dataset_path, pixelation_function, output_path):
    # Check if the output directory exists, if not, create it
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # Loop through the images in the dataset
    for filename in os.listdir(dataset_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            # Construct the full path to the image
            image_path = os.path.join(dataset_path, filename)

            # Load the image
            image = cv2.imread(image_path)

            # Apply the pixelation function
            processed_image = pixelation_function(image)

            # Construct the output path
            output_image_path = os.path.join(output_path, filename)

            # Save the processed image
            cv2.imwrite(output_image_path, processed_image)

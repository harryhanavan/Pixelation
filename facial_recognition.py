import face_recognition
import cv2
import os
import csv
import logging
import config

passes = 0
errors = 0

# Get the list of images to process
image_files = [f for f in os.listdir(config.output_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]
total_images = len(image_files)

# Set the maximum value of the progress bar
    

error_array = []
if config.evaluation_folder is None:
    os.makedirs("Evaluation", exist_ok=True)
    config.evaluation_folder = "Evaluation"
csv_file_path = os.path.join(config.evaluation_folder, "recognition_results.csv")

with open(csv_file_path, mode='w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["Original Image", "Pixelated Image", "Pixelation Type", "Parameters", "Recognition Result", "Distance"])

    # Iterate through pixelated images in the Output folder
    for pixelated_filename in os.listdir("Output"):
        # Parse the original image ID from the pixelated image filename
        parts = pixelated_filename.split('-')
        base_id = parts[0]
        pixelation_type = parts[1]
        parameters = "-".join(parts[2:])  # This will re-join the parameters correctly
        parameters = parameters.replace(".jpg", "")  # Removes the file extension
        parameters = parameters.replace("_", ", ")  # Replaces underscores with comma and space for CSV
        original_filename = f"{base_id}.jpg"
        original_image_path = os.path.join("Input".replace('/', os.sep), original_filename)
        pixelated_image_path = os.path.join("Output".replace('/', os.sep), pixelated_filename)
        
        print(f"Checking: {original_image_path}")
        print(f"Exists: {os.path.exists(original_image_path)}")
        print(f"Checking: {pixelated_image_path}")
        print(f"Exists: {os.path.exists(pixelated_image_path)}")
        logging.info(f"Checking: {original_image_path}")
        logging.info(f"Exists: {os.path.exists(original_image_path)}")
        logging.info(f"Checking: {pixelated_image_path}")
        logging.info(f"Exists: {os.path.exists(pixelated_image_path)}")


        # Read the original and pixelated images
        original_image = cv2.imread(original_image_path)
        pixelated_image = cv2.imread(pixelated_image_path)
        print(f"Original image size: {original_image.shape}")  # Prints the dimensions of the image
        print(f"Pixelated image size: {pixelated_image.shape}")  # Prints the dimensions of the image
        logging.info(f"Original image size: {original_image.shape}")  # Prints the dimensions of the image
        logging.info(f"Pixelated image size: {pixelated_image.shape}") # Prints the dimensions of the image

        try:
            # Check if images are read correctly
            if original_image is not None and pixelated_image is not None:
                original_encoding = face_recognition.face_encodings(original_image)[0]
                pixelated_encoding = face_recognition.face_encodings(pixelated_image)[0]

                results = face_recognition.compare_faces([original_encoding], pixelated_encoding)
                distance = face_recognition.face_distance([original_encoding], pixelated_encoding)[0]

                # Write the results to CSV with the new fields for pixelation type and parameters
                csv_writer.writerow([original_filename, pixelated_filename, pixelation_type, f'"{parameters}"', results[0], distance])
                print(f"Processed {original_filename}: Recognition Result={results[0]}, Distance={distance}")
                logging.info(f"Processed {original_filename}: Recognition Result={results[0]}, Distance={distance}")
                passes += 1
            else:
                print(f"Could not read {original_image_path} or {pixelated_image_path}. Skipping...")
                logging.error(f"Could not read {original_image_path} or {pixelated_image_path}. Skipping...")
                errors += 1
                error_array.append(f"Error with {original_image_path} or {pixelated_image_path}")



        except Exception as e:
            logging.error(f"An error occurred: {e}")

    print(f"Recognition results saved in {csv_file_path}")
    logging.info(f"Recognition results saved in {csv_file_path}")
    logging.info(f"Passed: {passes}. Errors occurred: {errors}")
    print(f"Passed: {passes}. Errors occurred: {errors}")

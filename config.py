import os
import sys
import logging
# Check if the application is running as a script or frozen executable
if getattr(sys, 'frozen', False):
    script_directory = os.path.dirname(sys.executable)
else:
    script_directory = os.path.dirname(os.path.realpath(__file__))


# Construct absolute paths for the input and output folders
    # Global variables for folder paths
if os.path.exists(os.path.join(script_directory, "Input")):
    input_folder = os.path.join(script_directory, "Input")
    logging.info("Input folder found")
else:
    input_folder = os.mkdir(os.path.join(script_directory, "Input"))
    logging.info("Input folder created")
if os.path.exists(os.path.join(script_directory, "Output")):
    output_folder = os.path.join(script_directory, "Output")
    logging.info("Output folder found")
else:
    output_folder = os.mkdir(os.path.join(script_directory, "Output"))
    logging.info("Output folder created")
if os.path.exists(os.path.join(script_directory, "Evaluation")):
    evaluation_folder = os.path.join(script_directory, "Evaluation")
    logging.info("Evaluation folder found")
else:
    evaluation_folder = os.mkdir(os.path.join(script_directory, "Evaluation"))
    logging.info("Evaluation folder created")
input_folder_label = None
output_folder_label = None
evaluation_folder_label = None
input_listbox = None
params = None
selected_method = None
description_text = None

tooltip_labels = {
    "basic_pixelation": {
        "block_size": "Suggested default: 10 pixels\nRange: 1 to 50 pixels\nAdjust the block size to control the level of pixelation. Larger blocks create a more pixelated effect."
    },
    "gaussian_blur": {
        "kernel_size": "Suggested default: 5x5\nRange: 3x3 to 21x21[MUST BE ODD]\nAdjust the kernel size to control the blur intensity. Larger values result in a smoother, more blended appearance."
    },
    "adaptive_pixelation": {
        "min_block_size": "Suggested default: 5 pixels\nRange: 2 to 10 pixels\nSet the minimum block size for pixelation. Smaller values retain more detail in high-variance areas.",
        "max_block_size": "Suggested default: 15 pixels\nRange: 10 to 50 pixels\nSet the maximum block size for pixelation. Larger values create stronger pixelation in low-variance areas.",
        "variance_threshold": "Suggested default: 50\nRange: 10 to 100\nAdjust the threshold for variance. Higher values increase the areas pixelated with the maximum block size."
    },
    "clustering_with_pixelation": {
        "num_clusters": "Suggested default: 5\nRange: 2 to 20\nSet the number of color clusters. More clusters capture finer color details.",
        "block_size": "Suggested default: 10 pixels\nRange: 1 to 50 pixels\nAdjust the block size to control the level of pixelation. Larger blocks create a more pixelated effect."
    }
}
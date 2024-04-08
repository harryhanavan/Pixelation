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
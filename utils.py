from config import input_folder, output_folder, evaluation_folder, input_folder_label, output_folder_label, evaluation_folder_label
import config
import os
import sys
import subprocess
import tkinter as tk
from tkinter import filedialog
import logging

def open_file():
    try:
        filename = filedialog.askopenfilename(title="Select an Image", filetypes=(("JPEG files", "*.jpg"), ("PNG files", "*.png")))
        return filename
    except Exception as e:
        logging.error(f"An error occurred: {e}")

def upload_file():
    try:
        filename = filedialog.askopenfilename(title="Select an Image to Upload", filetypes=(("JPEG files", "*.jpg"), ("PNG files", "*.png")))
        if filename:
            basename = os.path.basename(filename)
            destination = os.path.join(config.input_folder, basename)
            os.rename(filename, destination)
            return basename
        return None
    except Exception as e:
        logging.error(f"An error occurred: {e}")

def refresh_input_folder_list(listbox):
    try:
        listbox.delete(0, tk.END)
        for file in os.listdir(config.input_folder):
            listbox.insert(tk.END, file)
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        
def open_input_folder():
    try:
        if os.path.exists(input_folder):
            if os.name == 'posix':
                subprocess.run(['open', input_folder])
            else:  # Windows
                subprocess.run(['explorer', os.path.normpath(config.input_folder)])
    except Exception as e:
        logging.error(f"An error occurred: {e}")

def open_output_folder():
    try:
        if os.path.exists(output_folder):
            if os.name == 'posix':
                subprocess.run(['open', output_folder])
            else:  # Windows
                subprocess.run(['explorer', os.path.normpath(config.output_folder)])
    except Exception as e:
        logging.error(f"An error occurred: {e}")

def select_input_folder(input_listbox, input_label):
    try:
        selected_folder = filedialog.askdirectory(title="Select Input Folder")
        if selected_folder:
            config.input_folder = selected_folder
            refresh_input_folder_list(input_listbox)
            input_label.config(text=f"Input Folder: {config.input_folder}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

def select_output_folder(output_label):
    try:
        selected_folder = filedialog.askdirectory(title="Select Output Folder")
        if selected_folder:
            config.output_folder = selected_folder
            output_label.config(text=f"Output Folder: {config.output_folder}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

def revert_folders(input_folder_label, output_folder_label, evaluation_folder_label, input_listbox):
    try:
        # Check if the application is running as a script or frozen executable
        if getattr(sys, 'frozen', False):
            script_directory = os.path.dirname(sys.executable)
        else:
            script_directory = os.path.dirname(os.path.realpath(__file__))
        config.input_folder = os.path.join(script_directory, "Input")
        config.output_folder = os.path.join(script_directory, "Output")
        config.evaluation_folder = os.path.join(script_directory, "Evaluation")
        input_folder_label.config(text=f"Input Folder: {config.input_folder}")
        output_folder_label.config(text=f"Output Folder: {config.output_folder}")
        evaluation_folder_label.config(text=f"Evaluation Folder: {config.evaluation_folder}")
        refresh_input_folder_list(input_listbox)
    except Exception as e:
        logging.error(f"An error occurred: {e}")

def select_evaluation_folder(evaluation_folder_label):
    try:
        folder = filedialog.askdirectory()
        if folder:
            config.evaluation_folder = folder
            evaluation_folder_label.config(text=f"Evaluation Folder: {config.evaluation_folder}")
            
    except Exception as e:
        logging.error(f"An error occurred: {e}")

def open_evaluation_folder():
    try:
        os.startfile(config.evaluation_folder)
    except Exception as e:
        logging.error(f"An error occurred: {e}")

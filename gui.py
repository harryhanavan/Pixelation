import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import os
import subprocess
import cv2
import csv
from pixelation_methods import apply_basic_pixelization, apply_clustering_with_pixelization, apply_gaussian_blur, apply_adaptive_pixelation
from evaluation_metrics import calculate_psnr, calculate_ssim
from utils import open_file, upload_file, refresh_input_folder_list, open_input_folder, open_output_folder, select_input_folder, select_output_folder, revert_folders, select_evaluation_folder, open_evaluation_folder
from config import input_folder, output_folder, evaluation_folder, input_folder_label, output_folder_label, evaluation_folder_label, input_listbox, params, selected_method, description_text
import config
import logging

def update_params(frame, method):
    config.params = {}
    config.params.clear()  # Clear the params dictionary to remove previous entries
    """
    Update the parameters section of the GUI based on the selected pixelation method.

    Parameters:
        frame: The frame where the parameter widgets are placed.
        method: The selected pixelation method.
    """
    for widget in frame.winfo_children():
        widget.destroy()


    try:
        if method == "Basic Pixelization":
            block_size_label = tk.Label(frame, text="Block Size:")
            block_size_label.grid(row=0, column=0, padx=5, pady=5)
            block_size_entry = tk.Entry(frame)
            block_size_entry.grid(row=0, column=1, padx=5, pady=5)
            question_mark = tk.Label(frame, text="?", font=("Arial", 10, "bold"), fg="blue", cursor="hand2")
            question_mark.grid(row=0, column=2, padx=5, pady=5)
            ToolTip(question_mark, text=config.tooltip_labels["basic_pixelation"]["block_size"])
            config.params["block_size"] = block_size_entry
            config.description_text.delete(1.0, tk.END)
            config.description_text.insert(tk.END, "Basic Pixelization:\nThis method divides the image into uniform square blocks and replaces each block with a solid color representing the average color of the pixels within that block. The 'Block Size' parameter determines the size of these blocks. A smaller block size results in finer pixelation, preserving more details, while a larger block size creates a more abstract, mosaic-like effect.")

        elif method == "Gaussian Blur":
            kernel_size_label = tk.Label(frame, text="Kernel Size:")
            kernel_size_label.grid(row=0, column=0, padx=5, pady=5)
            kernel_size_entry = tk.Entry(frame)
            kernel_size_entry.grid(row=0, column=1, padx=5, pady=5)
            question_mark = tk.Label(frame, text="?", font=("Arial", 10, "bold"), fg="blue", cursor="hand2")
            question_mark.grid(row=0, column=2, padx=5, pady=5)
            ToolTip(question_mark, text= config.tooltip_labels["gaussian_blur"]["kernel_size"])
            config.params["kernel_size"] = kernel_size_entry
            config.description_text.delete(1.0, tk.END)
            config.description_text.insert(tk.END, "Gaussian Blur:\nThis method applies a Gaussian blur to the image, creating a smooth, blurred effect. The 'Kernel Size' parameter determines the size of the kernel used for blurring. A larger kernel size results in a stronger blur effect, making the image more blurry, while a smaller kernel size retains more of the image's details. The kernel size should be an odd number to ensure a symmetric blur effect.")

        elif method == "Adaptive Pixelization":
            min_block_size_label = tk.Label(frame, text="Min Block Size:")
            min_block_size_label.grid(row=0, column=0, padx=5, pady=5)
            min_block_size_entry = tk.Entry(frame)
            min_block_size_entry.grid(row=0, column=1, padx=5, pady=5)
            question_mark = tk.Label(frame, text="?", font=("Arial", 10, "bold"), fg="blue", cursor="hand2")
            question_mark.grid(row=0, column=2, padx=5, pady=5)
            ToolTip(question_mark, text= config.tooltip_labels["adaptive_pixelation"]["min_block_size"])
            config.params["min_block_size"] = min_block_size_entry

            max_block_size_label = tk.Label(frame, text="Max Block Size:")
            max_block_size_label.grid(row=1, column=0, padx=5, pady=5)
            max_block_size_entry = tk.Entry(frame)
            max_block_size_entry.grid(row=1, column=1, padx=5, pady=5)
            question_mark = tk.Label(frame, text="?", font=("Arial", 10, "bold"), fg="blue", cursor="hand2")
            question_mark.grid(row=1, column=2, padx=5, pady=5)
            ToolTip(question_mark, text= config.tooltip_labels["adaptive_pixelation"]["max_block_size"])
            config.params["max_block_size"] = max_block_size_entry

            variance_threshold_label = tk.Label(frame, text="Variance Threshold:")
            variance_threshold_label.grid(row=2, column=0, padx=5, pady=5)
            variance_threshold_entry = tk.Entry(frame)
            variance_threshold_entry.grid(row=2, column=1, padx=5, pady=5)
            question_mark = tk.Label(frame, text="?", font=("Arial", 10, "bold"), fg="blue", cursor="hand2")
            question_mark.grid(row=2, column=2, padx=5, pady=5)
            ToolTip(question_mark, text= config.tooltip_labels["adaptive_pixelation"]["variance_threshold"])
            config.params["variance_threshold"] = variance_threshold_entry
            config.description_text.delete(1.0, tk.END)
            config.description_text.insert(tk.END, "Adaptive Pixelization:\nThis method adjusts the pixelization block size based on the local variance of the image. Areas with higher variance (more detail or texture) are pixelized with smaller blocks, while areas with lower variance (more uniform) use larger blocks. 'Min Block Size' sets the smallest block size used for high-variance areas, while 'Max Block Size' sets the largest block size for low-variance areas. 'Variance Threshold' determines the level of variance at which the block size changes. A lower threshold means that more areas will be considered high-variance and pixelized with smaller blocks.")

        elif method == "Clustering with Pixelization":
            num_clusters_label = tk.Label(frame, text="Number of Clusters:")
            num_clusters_label.grid(row=0, column=0, padx=5, pady=5)
            num_clusters_entry = tk.Entry(frame)
            num_clusters_entry.grid(row=0, column=1, padx=5, pady=5)
            question_mark = tk.Label(frame, text="?", font=("Arial", 10, "bold"), fg="blue", cursor="hand2")
            question_mark.grid(row=0, column=2, padx=5, pady=5)
            ToolTip(question_mark, text= config.tooltip_labels["clustering_with_pixelation"]["num_clusters"])
            config.params["num_clusters"] = num_clusters_entry

            block_size_label = tk.Label(frame, text="Block Size:")
            block_size_label.grid(row=1, column=0, padx=5, pady=5)
            block_size_entry = tk.Entry(frame)
            block_size_entry.grid(row=1, column=1, padx=5, pady=5)
            question_mark = tk.Label(frame, text="?", font=("Arial", 10, "bold"), fg="blue", cursor="hand2")
            question_mark.grid(row=1, column=2, padx=5, pady=5)
            ToolTip(question_mark, text= config.tooltip_labels["clustering_with_pixelation"]["block_size"])
            config.params["block_size"] = block_size_entry
            config.description_text.delete(1.0, tk.END)
            config.description_text.insert(tk.END, "Clustering with Pixelization:\nThis method combines k-means clustering with pixelization. First, k-means clustering groups similar pixels into clusters based on their color values. Then, basic pixelization is applied to each cluster separately. 'Number of Clusters' determines how many clusters are created; a higher number results in more clusters and a more detailed image, while a lower number creates fewer clusters and a more abstract image. 'Block Size' sets the size of the pixelization blocks, with the same effects as in basic pixelization.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

method_descriptions = {
    "Basic Pixelization": "Basic Pixelization description...\n\nBlock Size: Description of block size parameter...",
    "Gaussian Blur": "Gaussian Blur description...\n\nKernel Size: Description of kernel size parameter...",
    "Adaptive Pixelization": "Adaptive Pixelization description...\n\nMin Block Size: Description...\nMax Block Size: Description...\nVariance Threshold: Description...",
}

def apply_pixelation(pixelation_method, method_name, input_folder, output_folder, progress_bar):
    if input_folder is None:
        os.makedirs("Input", exist_ok=True)
        config.input_folder = "Input"
    if output_folder is None:
        os.makedirs("Output", exist_ok=True)
        config.output_folder = "Output"
    print(f"Applying {method_name} to images in {input_folder} to {output_folder}")
        # Get the list of images to process
    image_files = [f for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f))]
    total_images = len(image_files)

    # Set the maximum value of the progress bar
    progress_bar["maximum"] = total_images
    errors = 0
    passes = 0
    params_dict = {key: entry.get() for key, entry in config.params.items()}
    # Convert parameters to their expected data types
    int_params = ['block_size', 'kernel_size', 'min_block_size', 'max_block_size', 'num_clusters', 'variance_threshold']
    for param in int_params:
        if param in params_dict:
            try:
                params_dict[param] = int(params_dict[param])
            except ValueError as e:
                messagebox.showerror("Error", f"{param.replace('_', ' ').capitalize()} must be an integer.")
                logging.error(f"{param.replace('_', ' ').capitalize()} must be an integer.")
                return

    for filename in os.listdir(input_folder):
        
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            print(f"Applying {method_name} with parameters {params_dict} to {filename}")
            logging.info(f"Applying {method_name} with parameters {params_dict} to {filename}")
            image_path = os.path.join(input_folder, filename)
            image = cv2.imread(image_path)
            try:
                processed_image = pixelation_method(image, **params_dict)
                passes += 1  # Increment passes counter
                base_id = filename.split('.')[0]
                parameters = "_".join(f"{key}-{value}" for key, value in params_dict.items())
                output_filename = f"{base_id}-{method_name}-{parameters}.jpg"
                output_path = os.path.join(output_folder, output_filename)
                cv2.imwrite(output_path, processed_image)
            except Exception as e:
                logging.error(f"An error occurred: {e}")
                messagebox.showerror("Error", f"An error occurred while processing {filename}.")
                errors += 1
            # Update the progress bar
            progress_bar["value"] += 1
            progress_bar.update()
            # progress_status = tk.Label(root, text=f"Progress: {progress_bar['value']} / {total_images}")
        else:
            logging.info(f"Skipping non-image file: {filename}")
            errors += 1      
    # Reset the progress bar when done
    progress_bar["value"] = 0
    # progress_status = tk.Label(root, text=f"Progress: Done")
    logging.info(f"Pixelation applied successfully to all images in {input_folder}, with {passes} successful and {errors} errors.")
    messagebox.showinfo("Pixelation Complete", f"Pixelation applied successfully to all images in {input_folder}, with {passes} successful and {errors} errors.")

def evaluate_images(progress_bar):
    # Get the list of images to process
    image_files = [f for f in os.listdir(config.output_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]
    total_images = len(image_files)

    # Set the maximum value of the progress bar
    progress_bar["maximum"] = total_images
    errors = 0
    passes = 0
    error_array = []
    if config.evaluation_folder is None:
        os.makedirs("Evaluation", exist_ok=True)
        config.evaluation_folder = "Evaluation"
    csv_file_path = os.path.join(config.evaluation_folder, "evaluation_results.csv")

    with open(csv_file_path, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Original Image", "Pixelated Image", "Pixelation Type", "Parameters", "SSIM", "PSNR"])

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
                    ssim_value = calculate_ssim(original_image, pixelated_image)
                    psnr_value = calculate_psnr(original_image, pixelated_image)

                    # Write the results to CSV with the new fields for pixelation type and parameters
                    csv_writer.writerow([original_filename, pixelated_filename, pixelation_type, f'"{parameters}"', ssim_value, psnr_value])
                    print(f"Processed {original_filename}: SSIM={ssim_value}, PSNR={psnr_value}")
                    logging.info(f"Processed {original_filename}: SSIM={ssim_value}, PSNR={psnr_value}")
                    passes += 1
                else:
                    print(f"Could not read {original_image_path} or {pixelated_image_path}. Skipping...")
                    logging.error(f"Could not read {original_image_path} or {pixelated_image_path}. Skipping...")
                    errors += 1
                    error_array.append(f"Error with {original_image_path} or {pixelated_image_path}")
                # Update the progress bar
                progress_bar["value"] += 1
                progress_bar.update()


            except Exception as e:
                logging.error(f"An error occurred: {e}")

        print(f"Evaluation results saved in {csv_file_path}")
        logging.info(f"Evaluation results saved in {csv_file_path}")
        logging.info(f"Passed: {passes}. Errors occurred: {errors}")
        messagebox.showinfo(
        "Evaluation Complete",
        f"Image evaluation completed. Results saved in {csv_file_path}.\n\n"
        f"Passed: {passes}. Errors occurred: {errors}\n\n"
        "Error List:\n" + "\n".join(error_array)
        )
        progress_bar["value"] = 0
        



def add_tooltip_labels(gui_code, tooltip_labels):
    """
    Adds tooltip labels to the GUI code for each parameter of the pixelation methods.
    
    Parameters:
        gui_code (str): The original GUI code as a string.
        tooltip_labels (dict): A dictionary containing the tooltip labels for each parameter.
    
    Returns:
        str: The updated GUI code with tooltip labels added.
    """
    # Iterate through each pixelation method and its parameters
    for method, params in tooltip_labels.items():
        for param, tooltip in params.items():
            # Find the line where the parameter entry box is created
            search_pattern = f'self.{param}_entry = tk.Entry'
            start_index = gui_code.find(search_pattern)

            if start_index != -1:
                # Find the end of the line
                end_index = gui_code.find('\n', start_index)

                # Insert the tooltip label creation code after the entry box line
                tooltip_code = f'\n        self.{param}_tooltip = tk.Label(self, text="{tooltip}", wraplength=200)\n        self.{param}_tooltip.grid(row=, column=)'
                gui_code = gui_code[:end_index + 1] + tooltip_code + gui_code[end_index + 1:]

    return gui_code

# Define the tooltip labels for each pixelation method


class ToolTip(object):

    """
    Create a tooltip for a given widget.
    """
    def __init__(self, widget, text='widget info'):
        self.waittime = 500     # Pause time before showing tooltip
        self.wraplength = 180   # Maximum line width for the text
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.id = None
        self.tw = None

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event=None):
        x, y, cx, cy = self.widget.bbox("insert")   # Get widget's bounding box
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        # Create a toplevel window; use topmost attribute to ensure it appears above all other windows
        self.tw = tk.Toplevel(self.widget)
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(self.tw, text=self.text, justify='left',
                         background="#ffffe0", relief='solid', borderwidth=1,
                         wraplength = self.wraplength)
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw= None
        if tw:
            tw.destroy()

def create_gui():
    try:
        root = tk.Tk()
        root.title("Pixelation Project")

        selected_method = tk.StringVar(value="Basic Pixelization")
        pixelation_methods = {
            "Basic Pixelization": apply_basic_pixelization,
            "Gaussian Blur": apply_gaussian_blur,
            "Adaptive Pixelization": apply_adaptive_pixelation,
            "Clustering with Pixelization": apply_clustering_with_pixelization
        }
        logging.info("Current input folder: " + config.input_folder)
        logging.info("Current output folder: " + config.output_folder)
        logging.info("Current evaluation folder: " + config.evaluation_folder)
        params = {}  # Initialize params dictionary

        # Frame for file operations
        file_frame = tk.Frame(root)
        file_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        btn_upload = tk.Button(file_frame, text="Upload Image", command=lambda: upload_file())
        btn_upload.grid(row=0, column=0, padx=5, pady=5)

        btn_refresh = tk.Button(file_frame, text="Refresh Input Folder", command=lambda: refresh_input_folder_list(input_listbox))
        btn_refresh.grid(row=0, column=1, padx=5, pady=5)

        btn_select_input = tk.Button(file_frame, text="Select Input Folder", command=lambda: select_input_folder(input_listbox, input_folder_label))
        btn_select_input.grid(row=0, column=2, padx=5, pady=5)

        btn_select_output = tk.Button(file_frame, text="Select Output Folder", command=lambda: select_output_folder(output_folder_label))
        btn_select_output.grid(row=0, column=3, padx=5, pady=5)

        btn_revert_folders = tk.Button(file_frame, text="Revert to Default Folders", command=lambda: revert_folders(input_folder_label, output_folder_label, evaluation_folder_label, input_listbox))
        btn_revert_folders.grid(row=0, column=4, padx=5, pady=5)

        btn_open_input = tk.Button(file_frame, text="Open Input Folder", command=lambda: open_input_folder())
        btn_open_input.grid(row=0, column=5, padx=5, pady=5)

        btn_open_output = tk.Button(file_frame, text="Open Output Folder", command=lambda: open_output_folder())
        btn_open_output.grid(row=0, column=6, padx=5, pady=5)

        input_folder_label = tk.Label(file_frame, text=f"Input Folder: {config.input_folder}")
        input_folder_label.grid(row=1, column=0, columnspan=4, padx=5, pady=5)

        output_folder_label = tk.Label(file_frame, text=f"Output Folder: {config.output_folder}")
        output_folder_label.grid(row=1, column=4, columnspan=3, padx=5, pady=5)
        # Frame for evaluation folder operations
        evaluation_frame = tk.Frame(root)
        evaluation_frame.grid(row=4, column=0, padx=10, pady=10, sticky="ew")

        btn_select_evaluation = tk.Button(evaluation_frame, text="Select Evaluation Folder", command=lambda: select_evaluation_folder(evaluation_folder_label))
        btn_select_evaluation.grid(row=0, column=0, padx=5, pady=5)

        btn_open_evaluation = tk.Button(evaluation_frame, text="Open Evaluation Folder", command=lambda: open_evaluation_folder())
        btn_open_evaluation.grid(row=0, column=1, padx=5, pady=5)

        evaluation_folder_label = tk.Label(evaluation_frame, text=f"Evaluation Folder: {config.evaluation_folder}")
        evaluation_folder_label.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        # Frame for input folder listbox
        input_frame = tk.Frame(root)
        input_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        input_listbox = tk.Listbox(input_frame)
        input_listbox.pack(fill="both", expand=True)
        # Frame for description
        description_frame = tk.Frame(root)
        description_frame.grid(row=1, column=1, rowspan=2, padx=10, pady=10, sticky="nsew")  # Extend the frame to span two rows

        config.description_text = tk.Text(description_frame, wrap=tk.WORD, height=15, width=40)  # Increase the height
        config.description_text.pack(fill="both", expand=True)

        # Configure the grid to allocate extra space to the description frame's row
        root.grid_rowconfigure(1, weight=1)

        # Frame for pixelation options
        pixelation_frame = tk.Frame(root)
        pixelation_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        pixelation_menu = ttk.Combobox(pixelation_frame, textvariable=selected_method, values=list(pixelation_methods.keys()), state="readonly")
        pixelation_menu.grid(row=0, column=0, padx=5, pady=5)

        params_frame = tk.Frame(pixelation_frame)
        params_frame.grid(row=1, column=0, padx=5, pady=5)
        update_params(params_frame, selected_method.get())  # Initialize params for the selected method

        def on_method_change(event):
            update_params(params_frame, selected_method.get())  # Update params when the method is changed
        pixelation_menu.bind("<<ComboboxSelected>>", on_method_change)
        
        # Create the progress bar
        progress_bar = ttk.Progressbar(root, length=5, mode='determinate')
        progress_bar.grid(row=3, column=1, columnspan=5, padx=5, pady=10, sticky="ew")

        # progress_status = tk.Label(root, text="Progress:")
        # progress_status.grid(row=4, column=0, padx=5, pady=5)

        # Pass the progress bar to the apply_pixelation function
        btn_apply = tk.Button(pixelation_frame, text="Apply Pixelation", command=lambda: apply_pixelation(pixelation_methods[selected_method.get()], selected_method.get(), config.input_folder, config.output_folder, progress_bar))
        btn_apply.grid(row=2, column=0, padx=5, pady=5)



        # Frame for evaluation
        evaluation_frame = tk.Frame(root)
        evaluation_frame.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

        btn_evaluate = tk.Button(evaluation_frame, text="Evaluate Images", command=lambda: evaluate_images(progress_bar))
        btn_evaluate.pack()

        root.mainloop()
    except Exception as e:
        logging.error(f"An error occurred: {e}")
 
if __name__ == "__main__":
    create_gui()
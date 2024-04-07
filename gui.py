import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import os
import subprocess
import cv2
import csv
from pixelation_methods import apply_basic_pixelization, apply_clustering_with_pixelization, apply_gaussian_blur, apply_adaptive_pixelation
from evaluation_metrics import calculate_psnr, calculate_ssim


# Global variables for folder paths
input_folder = "Input"
output_folder = "Output"
evaluation_folder = "Evaluation"
input_folder_label = None
output_folder_label = None
evaluation_folder_label = None
input_listbox = None
params = None
selected_method = None
description_text = None


def open_file():
    filename = filedialog.askopenfilename(title="Select an Image", filetypes=(("JPEG files", "*.jpg"), ("PNG files", "*.png")))
    return filename

def update_params(frame, method):
    """
    Update the parameters section of the GUI based on the selected pixelation method.
    
    Parameters:
        frame: The frame where the parameter widgets are placed.
        method: The selected pixelation method.
    """
    for widget in frame.winfo_children():
        widget.destroy()

    description_text.delete('1.0', tk.END)  # Clear the description text

    if method == "Basic Pixelization":
        block_size_label = tk.Label(frame, text="Block Size:")
        block_size_label.grid(row=0, column=0, padx=5, pady=5)
        block_size_entry = tk.Entry(frame)
        block_size_entry.grid(row=0, column=1, padx=5, pady=5)
        params["block_size"] = block_size_entry

        description_text.insert(tk.END, "Basic Pixelization:\nThis method divides the image into uniform square blocks and replaces each block with a solid color representing the average color of the pixels within that block. The 'Block Size' parameter determines the size of these blocks. A smaller block size results in finer pixelation, preserving more details, while a larger block size creates a more abstract, mosaic-like effect.")

    elif method == "Gaussian Blur":
        kernel_size_label = tk.Label(frame, text="Kernel Size:")
        kernel_size_label.grid(row=0, column=0, padx=5, pady=5)
        kernel_size_entry = tk.Entry(frame)
        kernel_size_entry.grid(row=0, column=1, padx=5, pady=5)
        params["kernel_size"] = kernel_size_entry

        description_text.insert(tk.END, "\n\nGaussian Blur:\nThis method applies a Gaussian blur to the image, creating a smooth, blurred effect. The 'Kernel Size' parameter determines the size of the kernel used for blurring. A larger kernel size results in a stronger blur effect, making the image more blurry, while a smaller kernel size retains more of the image's details. The kernel size should be an odd number to ensure a symmetric blur effect.")

    elif method == "Adaptive Pixelization":
        min_block_size_label = tk.Label(frame, text="Min Block Size:")
        min_block_size_label.grid(row=0, column=0, padx=5, pady=5)
        min_block_size_entry = tk.Entry(frame)
        min_block_size_entry.grid(row=0, column=1, padx=5, pady=5)
        params["min_block_size"] = min_block_size_entry

        max_block_size_label = tk.Label(frame, text="Max Block Size:")
        max_block_size_label.grid(row=1, column=0, padx=5, pady=5)
        max_block_size_entry = tk.Entry(frame)
        max_block_size_entry.grid(row=1, column=1, padx=5, pady=5)
        params["max_block_size"] = max_block_size_entry

        variance_threshold_label = tk.Label(frame, text="Variance Threshold:")
        variance_threshold_label.grid(row=2, column=0, padx=5, pady=5)
        variance_threshold_entry = tk.Entry(frame)
        variance_threshold_entry.grid(row=2, column=1, padx=5, pady=5)
        params["variance_threshold"] = variance_threshold_entry

        description_text.insert(tk.END, "\n\nAdaptive Pixelization:\nThis method adjusts the pixelization block size based on the local variance of the image. Areas with higher variance (more detail or texture) are pixelized with smaller blocks, while areas with lower variance (more uniform) use larger blocks. 'Min Block Size' sets the smallest block size used for high-variance areas, while 'Max Block Size' sets the largest block size for low-variance areas. 'Variance Threshold' determines the level of variance at which the block size changes. A lower threshold means that more areas will be considered high-variance and pixelized with smaller blocks.")

    elif method == "Clustering with Pixelization":
        num_clusters_label = tk.Label(frame, text="Number of Clusters:")
        num_clusters_label.grid(row=0, column=0, padx=5, pady=5)
        num_clusters_entry = tk.Entry(frame)
        num_clusters_entry.grid(row=0, column=1, padx=5, pady=5)
        params["num_clusters"] = num_clusters_entry

        block_size_label = tk.Label(frame, text="Block Size:")
        block_size_label.grid(row=1, column=0, padx=5, pady=5)
        block_size_entry = tk.Entry(frame)
        block_size_entry.grid(row=1, column=1, padx=5, pady=5)
        params["block_size"] = block_size_entry

        description_text.insert(tk.END, "\n\nClustering with Pixelization:\nThis method combines k-means clustering with pixelization. First, k-means clustering groups similar pixels into clusters based on their color values. Then, basic pixelization is applied to each cluster separately. 'Number of Clusters' determines how many clusters are created; a higher number results in more clusters and a more detailed image, while a lower number creates fewer clusters and a more abstract image. 'Block Size' sets the size of the pixelization blocks, with the same effects as in basic pixelization.")

method_descriptions = {
    "Basic Pixelization": "Basic Pixelization description...\n\nBlock Size: Description of block size parameter...",
    "Gaussian Blur": "Gaussian Blur description...\n\nKernel Size: Description of kernel size parameter...",
    "Adaptive Pixelization": "Adaptive Pixelization description...\n\nMin Block Size: Description...\nMax Block Size: Description...\nVariance Threshold: Description...",
}

def upload_file():
    global input_folder
    filename = filedialog.askopenfilename(title="Select an Image to Upload", filetypes=(("JPEG files", "*.jpg"), ("PNG files", "*.png")))
    if filename:
        basename = os.path.basename(filename)
        destination = os.path.join(input_folder, basename)
        os.rename(filename, destination)
        return basename
    return None

def refresh_input_folder_list(listbox):
    global input_folder
    listbox.delete(0, tk.END)
    for file in os.listdir(input_folder):
        listbox.insert(tk.END, file)
        
def open_input_folder():
    global input_folder
    if os.path.exists(input_folder):
        if os.name == 'posix':
            subprocess.run(['open', input_folder])
        else:  # Windows
            subprocess.run(['explorer', os.path.normpath(input_folder)])

def open_output_folder():
    global output_folder
    if os.path.exists(output_folder):
        if os.name == 'posix':
            subprocess.run(['open', output_folder])
        else:  # Windows
            subprocess.run(['explorer', os.path.normpath(output_folder)])

def apply_pixelation(pixelation_method, method_name):
    global input_folder, output_folder
    params_dict = {key: entry.get() for key, entry in params.items()}
    
    # Convert parameters to appropriate types
    if method_name == "Basic Pixelization":
        params_dict["block_size"] = int(params_dict["block_size"])

    for filename in os.listdir(input_folder):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            print(f"Applying {method_name} with parameters {params_dict} to {filename}")
            image_path = os.path.join(input_folder, filename)
            image = cv2.imread(image_path)
            processed_image = pixelation_method(image, **params_dict)
            output_path = os.path.join(output_folder, f"{method_name}_{filename}")
            cv2.imwrite(output_path, processed_image)


    messagebox.showinfo("Pixelation Complete", f"Pixelation applied successfully to all images in {input_folder}")

def evaluate_images():
    evaluation_folder = "Evaluation"
    os.makedirs(evaluation_folder, exist_ok=True)
    csv_file_path = os.path.join(evaluation_folder, "evaluation_results.csv")

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
            original_image_path = os.path.join("Input", original_filename)
            pixelated_image_path = os.path.join("Output", pixelated_filename)
            
            print(f"Checking: {original_image_path}")
            print(f"Exists: {os.path.exists(original_image_path)}")
            print(f"Checking: {pixelated_image_path}")
            print(f"Exists: {os.path.exists(pixelated_image_path)}")

            # Read the original and pixelated images
            original_image = cv2.imread(original_image_path)
            pixelated_image = cv2.imread(pixelated_image_path)
            print(f"Original image size: {original_image.shape}")  # Prints the dimensions of the image
            print(f"Pixelated image size: {pixelated_image.shape}")  # Prints the dimensions of the image

            # Check if images are read correctly
            if original_image is not None and pixelated_image is not None:
                ssim_value = calculate_ssim(original_image, pixelated_image)
                psnr_value = calculate_psnr(original_image, pixelated_image)

                # Write the results to CSV with the new fields for pixelation type and parameters
                csv_writer.writerow([original_filename, pixelated_filename, pixelation_type, f'"{parameters}"', ssim_value, psnr_value])
                print(f"Processed {original_filename}: SSIM={ssim_value}, PSNR={psnr_value}")
            else:
                print(f"Could not read {original_image_path} or {pixelated_image_path}. Skipping...")

        print(f"Evaluation results saved in {csv_file_path}")

def select_input_folder(input_listbox):
    global input_folder, input_folder_label
    selected_folder = filedialog.askdirectory(title="Select Input Folder")
    if selected_folder:
        input_folder = selected_folder
        refresh_input_folder_list(input_listbox)
        input_folder_label.config(text=f"Input Folder: {input_folder}")  # Update the input folder label

def select_output_folder():
    global output_folder, output_folder_label
    selected_folder = filedialog.askdirectory(title="Select Output Folder")
    if selected_folder:
        output_folder = selected_folder
        output_folder_label.config(text=f"Output Folder: {output_folder}")  # Update the output folder label

def revert_folders():
    global input_folder, output_folder, evaluation_folder
    input_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Input')
    output_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Output')
    evaluation_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Evaluation')
    input_folder_label.config(text=f"Input Folder: {input_folder}")
    output_folder_label.config(text=f"Output Folder: {output_folder}")
    evaluation_folder_label.config(text=f"Evaluation Folder: {evaluation_folder}")
    refresh_input_folder_list()

def select_evaluation_folder():
    global evaluation_folder
    folder = filedialog.askdirectory()
    if folder:
        evaluation_folder = folder
        evaluation_folder_label.config(text=f"Evaluation Folder: {evaluation_folder}")

def open_evaluation_folder():
    os.startfile(evaluation_folder)

def create_gui():
    global input_folder_label, output_folder_label, input_listbox, evaluation_folder_label, params, selected_method, description_text
    root = tk.Tk()
    root.title("Pixelation Project")

    selected_method = tk.StringVar(value="Basic Pixelization")
    pixelation_methods = {
        "Basic Pixelization": apply_basic_pixelization,
        "Gaussian Blur": apply_gaussian_blur,
        "Adaptive Pixelization": apply_adaptive_pixelation,
        "Clustering with Pixelization": apply_clustering_with_pixelization
    }
    
    params = {}  # Initialize params dictionary

    # Frame for file operations
    file_frame = tk.Frame(root)
    file_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

    btn_upload = tk.Button(file_frame, text="Upload Image", command=lambda: upload_file())
    btn_upload.grid(row=0, column=0, padx=5, pady=5)

    btn_refresh = tk.Button(file_frame, text="Refresh Input Folder", command=lambda: refresh_input_folder_list(input_listbox))
    btn_refresh.grid(row=0, column=1, padx=5, pady=5)

    btn_select_input = tk.Button(file_frame, text="Select Input Folder", command=lambda: select_input_folder(input_listbox))
    btn_select_input.grid(row=0, column=2, padx=5, pady=5)

    btn_select_output = tk.Button(file_frame, text="Select Output Folder", command=select_output_folder)
    btn_select_output.grid(row=0, column=3, padx=5, pady=5)

    btn_revert_folders = tk.Button(file_frame, text="Revert to Default Folders", command=revert_folders)
    btn_revert_folders.grid(row=0, column=4, padx=5, pady=5)

    btn_open_input = tk.Button(file_frame, text="Open Input Folder", command=open_input_folder)
    btn_open_input.grid(row=0, column=5, padx=5, pady=5)

    btn_open_output = tk.Button(file_frame, text="Open Output Folder", command=open_output_folder)
    btn_open_output.grid(row=0, column=6, padx=5, pady=5)

    input_folder_label = tk.Label(file_frame, text=f"Input Folder: {input_folder}")
    input_folder_label.grid(row=1, column=0, columnspan=4, padx=5, pady=5)

    output_folder_label = tk.Label(file_frame, text=f"Output Folder: {output_folder}")
    output_folder_label.grid(row=1, column=4, columnspan=3, padx=5, pady=5)
    # Frame for evaluation folder operations
    evaluation_frame = tk.Frame(root)
    evaluation_frame.grid(row=4, column=0, padx=10, pady=10, sticky="ew")

    btn_select_evaluation = tk.Button(evaluation_frame, text="Select Evaluation Folder", command=select_evaluation_folder)
    btn_select_evaluation.grid(row=0, column=0, padx=5, pady=5)

    btn_open_evaluation = tk.Button(evaluation_frame, text="Open Evaluation Folder", command=open_evaluation_folder)
    btn_open_evaluation.grid(row=0, column=1, padx=5, pady=5)

    evaluation_folder_label = tk.Label(evaluation_frame, text=f"Evaluation Folder: {evaluation_folder}")
    evaluation_folder_label.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

    # Frame for input folder listbox
    input_frame = tk.Frame(root)
    input_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

    input_listbox = tk.Listbox(input_frame)
    input_listbox.pack(fill="both", expand=True)
    # Frame for description
    description_frame = tk.Frame(root)
    description_frame.grid(row=1, column=1, rowspan=2, padx=10, pady=10, sticky="nsew")  # Extend the frame to span two rows

    description_text = tk.Text(description_frame, wrap=tk.WORD, height=15, width=40)  # Increase the height
    description_text.pack(fill="both", expand=True)

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

    btn_apply = tk.Button(pixelation_frame, text="Apply Pixelation", command=lambda: apply_pixelation(pixelation_methods[selected_method.get()], selected_method.get()))
    btn_apply.grid(row=2, column=0, padx=5, pady=5)

    # Frame for evaluation
    evaluation_frame = tk.Frame(root)
    evaluation_frame.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

    btn_evaluate = tk.Button(evaluation_frame, text="Evaluate Images", command=evaluate_images)
    btn_evaluate.pack()

    root.mainloop()
 
if __name__ == "__main__":
    create_gui()


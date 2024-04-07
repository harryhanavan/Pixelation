import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import os
import subprocess
import cv2
import csv
from image_processing import process_images
from pixelation_methods import apply_basic_pixelization, apply_clustering_with_pixelization, apply_gaussian_blur, apply_adaptive_pixelation
from evaluation_metrics import calculate_psnr, calculate_ssim


# Global variables for folder paths
input_folder = "Input"
output_folder = "Output"
input_folder_label = None
output_folder_label = None
input_listbox = None
params = None
selected_method = None

def open_file():
    filename = filedialog.askopenfilename(title="Select an Image", filetypes=(("JPEG files", "*.jpg"), ("PNG files", "*.png")))
    return filename

def update_params(frame, method):
    global params
    for widget in frame.winfo_children():
        widget.destroy()

    if method == "Basic Pixelization":
        block_size = tk.IntVar(value=10)
        tk.Label(frame, text="Block Size:").pack()
        tk.Entry(frame, textvariable=block_size).pack()
        params = {"block_size": block_size}

    elif method == "Adaptive Pixelization":
        base_block_size = tk.IntVar(value=10)
        detail_threshold = tk.IntVar(value=30)
        tk.Label(frame, text="Base Block Size:").pack()
        tk.Entry(frame, textvariable=base_block_size).pack()
        tk.Label(frame, text="Detail Threshold:").pack()
        tk.Entry(frame, textvariable=detail_threshold).pack()
        params = {"base_block_size": base_block_size, "detail_threshold": detail_threshold}

    elif method == "Clustering with Pixelization":
        num_clusters = tk.IntVar(value=8)
        block_size = tk.IntVar(value=10)
        tk.Label(frame, text="Number of Clusters:").pack()
        tk.Entry(frame, textvariable=num_clusters).pack()
        tk.Label(frame, text="Block Size:").pack()
        tk.Entry(frame, textvariable=block_size).pack()
        params = {"num_clusters": num_clusters, "block_size": block_size}

    elif method == "Gaussian Blur":
        kernel_size = tk.IntVar(value=15)
        tk.Label(frame, text="Kernel Size:").pack()
        tk.Entry(frame, textvariable=kernel_size).pack()
        params = {"kernel_size": kernel_size}

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
    global input_folder, output_folder, params  # Declare params as a global variable here
    if params is None:
        messagebox.showerror("Error", "Parameters not set. Please select a pixelation method and set its parameters.")
        return
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            input_path = os.path.join(input_folder, filename)
            image = cv2.imread(input_path)

            params_dict = {key: var.get() for key, var in params.items()}
            print(f"Applying {method_name} with parameters {params_dict} to {filename}")

            # Call the pixelation function with the selected parameters and filename
            processed_image = pixelation_method(image, **params_dict)

            # Format the output filename
            name, ext = os.path.splitext(filename)
            params_str = "_".join([f"{k}{v}" for k, v in params_dict.items()])
            output_filename = f"{name}_{method_name}_{params_str}{ext}"

            # Save the processed image to the Output folder
            output_path = os.path.join(output_folder, output_filename)
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
            parts = pixelated_filename.split('_')
            base_id = parts[0]
            # Extract the pixelation type and parameters from the filename
            pixelation_type = parts[1]
            parameters = "_".join(parts[2:-1])
            # Assume original filename structure: {id}.jpg
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
                csv_writer.writerow([original_filename, pixelated_filename, pixelation_type, parameters, ssim_value, psnr_value])
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
    global input_folder, output_folder, input_listbox
    input_folder = "Input"
    output_folder = "Output"
    refresh_input_folder_list(input_listbox)
    input_folder_label.config(text=f"Input Folder: {input_folder}")  # Update the input folder label
    output_folder_label.config(text=f"Output Folder: {output_folder}")  # Update the output folder label

def create_gui():
    global input_folder_label, output_folder_label, input_listbox, params, selected_method
    root = tk.Tk()
    root.title("Pixelation Project")

    selected_method = tk.StringVar(value="Basic Pixelization")
    pixelation_methods = {
        "Basic Pixelization": apply_basic_pixelization,
        "Gaussian Blur": apply_gaussian_blur,
        "Adaptive Pixelization": apply_adaptive_pixelation,
        "Clustering with Pixelization": apply_clustering_with_pixelization
    }

    # Upload button
    btn_upload = tk.Button(root, text="Upload Image", command=lambda: upload_file())
    btn_upload.pack()

    # Listbox for input folder
    input_listbox = tk.Listbox(root)
    input_listbox.pack()
    refresh_input_folder_list(input_listbox)  # Initially populate the listbox with the contents of the input folder

    # Refresh button for input folder list
    btn_refresh = tk.Button(root, text="Refresh Input Folder", command=lambda: refresh_input_folder_list())
    btn_refresh.pack()

    # Dropdown menu for selecting pixelation method
    pixelation_menu = ttk.Combobox(root, textvariable=selected_method, values=list(pixelation_methods.keys()), state="readonly")
    pixelation_menu.pack()

    # Frame for parameters
    params_frame = tk.Frame(root)
    params_frame.pack()
    update_params(params_frame, selected_method.get())  # Initialize params for the selected method

    def on_method_change(event):
        update_params(params_frame, selected_method.get())  # Update params when the method is changed
    pixelation_menu.bind("<<ComboboxSelected>>", on_method_change)

    # Buttons for folder selection and reverting
    btn_select_input = tk.Button(root, text="Select Input Folder", command=lambda: select_input_folder(input_listbox))
    btn_select_input.pack()

    btn_select_output = tk.Button(root, text="Select Output Folder", command=select_output_folder)
    btn_select_output.pack()

    btn_revert_folders = tk.Button(root, text="Revert to Default Folders", command=revert_folders)
    btn_revert_folders.pack()

    # Buttons to open folders
    btn_open_input = tk.Button(root, text="Open Input Folder", command=open_input_folder)
    btn_open_input.pack()

    btn_open_output = tk.Button(root, text="Open Output Folder", command=open_output_folder)
    btn_open_output.pack()

    # Button to apply pixelation
    btn_apply = tk.Button(root, text="Apply Pixelation", command=lambda: apply_pixelation(pixelation_methods[selected_method.get()], selected_method.get()))
    btn_apply.pack()

    # Labels to display the current folder paths
    input_folder_label = tk.Label(root, text=f"Input Folder: {input_folder}")
    input_folder_label.pack()

    output_folder_label = tk.Label(root, text=f"Output Folder: {output_folder}")
    output_folder_label.pack()

    # Button to trigger the evaluation
    btn_evaluate = tk.Button(root, text="Evaluate Images", command=evaluate_images)
    btn_evaluate.pack()

    root.mainloop()



if __name__ == "__main__":
    create_gui()

from image_processing import process_images
from pixelation_methods import apply_basic_pixelization, apply_adaptive_pixelation, apply_clustering_with_pixelization
from gui import create_gui

def main():
    # Path to the WebFace dataset
    dataset_path = "Input"

    # Output path for processed images
    output_path = "Output"

    create_gui()


if __name__ == "__main__":
    main()

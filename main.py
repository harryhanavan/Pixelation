from image_processing import process_images
from pixelation_methods import apply_basic_pixelization
from pixelation_methods import apply_adaptive_pixelization
from pixelation_methods import apply_clustering_with_pixelization


def main():
    # Path to the WebFace dataset
    dataset_path = "Input"

    # Output path for processed images
    output_path = "Output"

        # Process the images in the dataset
    #process_images(dataset_path, lambda img: apply_basic_pixelization(img, block_size=10), output_path)
        # Process the images in the dataset with adaptive pixelization
    #process_images(dataset_path, lambda img: apply_adaptive_pixelization(img, base_block_size=10, detail_threshold=30), output_path)
        # Process the images in the dataset with clustering and pixelization
    #process_images(dataset_path, lambda img: apply_clustering_with_pixelization(img, num_clusters=8, block_size=10), output_path)



if __name__ == "__main__":
    main()

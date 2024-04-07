import cv2
import numpy as np
from sklearn.cluster import KMeans # For clustering


def apply_basic_pixelization(image, block_size=10):
    """
    Apply basic pixelization to an image.
    
    Parameters:
        image: The input image as a NumPy array.
        block_size: The size of each block for pixelization.
        
    Returns:
        The pixelized image as a NumPy array.
    """
    # Get the dimensions of the image
    height, width, _ = image.shape

    # Create a copy of the image to modify
    pixelized_image = np.copy(image)

    # Loop through the image in steps of block_size
    for y in range(0, height, block_size):
        for x in range(0, width, block_size):
            # Define the coordinates of the current block
            y1, y2 = y, min(y + block_size, height)
            x1, x2 = x, min(x + block_size, width)

            # Calculate the average color of the block
            block = image[y1:y2, x1:x2]
            average_color = np.mean(block, axis=(0, 1)).astype(int)

            # Set the color of the block to the average color
            pixelized_image[y1:y2, x1:x2] = average_color

    return pixelized_image

def apply_gaussian_blur(image, kernel_size):
    # Ensure kernel_size is a tuple
    kernel_size = (kernel_size, kernel_size)
    return cv2.GaussianBlur(image, kernel_size, 0)

def apply_adaptive_pixelation(image, min_block_size=5, max_block_size=15, variance_threshold=50):
    """
    Applies adaptive pixelation to an image based on local variance.

    :param image: Input image.
    :param min_block_size: Minimum block size for pixelation.
    :param max_block_size: Maximum block size for pixelation.
    :param variance_threshold: Threshold for variance to decide block size.
    :return: Pixelated image.
    """
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Initialize the output image
    output = np.zeros_like(image)

    # Define the step size for processing blocks
    step_size = min_block_size

    # Iterate over the image in blocks
    for y in range(0, gray.shape[0], step_size):
        for x in range(0, gray.shape[1], step_size):
            # Compute the local variance
            block = gray[y:y+step_size, x:x+step_size]
            local_variance = np.var(block)

            # Determine the block size based on variance
            if local_variance < variance_threshold:
                block_size = max_block_size
            else:
                block_size = min_block_size

            # Ensure the block size does not exceed the image boundaries
            block_size = min(block_size, gray.shape[0] - y, gray.shape[1] - x)

            # Pixelate the block in the output image
            color = np.mean(image[y:y+block_size, x:x+block_size], axis=(0, 1), dtype=int)
            output[y:y+block_size, x:x+block_size] = color

    return output   



def apply_clustering_with_pixelization(image, num_clusters=8, block_size=10):
    """
    Applies pixelation using k-means clustering to group similar pixels.
    
    :param image: Input image.
    :param num_clusters: Number of clusters for k-means.
    :param block_size: Size of the blocks for pixelation.
    :return: Pixelated image.
    """
    # Reshape the image to a 2D array of pixels
    pixel_values = image.reshape((-1, 3))
    pixel_values = np.float32(pixel_values)

    # Apply k-means clustering
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
    _, labels, centers = cv2.kmeans(pixel_values, num_clusters, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    # Convert centers to uint8 and reshape to the original image shape
    centers = np.uint8(centers)
    clustered_image = centers[labels.flatten()]
    clustered_image = clustered_image.reshape(image.shape)

    # Apply basic pixelation to the clustered image
    return apply_basic_pixelization(clustered_image, block_size)



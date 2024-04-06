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

def apply_adaptive_pixelization(image, base_block_size=10, detail_threshold=30):
    """
    Apply adaptive pixelization to an image.
    
    Parameters:
        image: The input image as a NumPy array.
        base_block_size: The base size of each block for pixelization.
        detail_threshold: The threshold for the standard deviation to determine detailed areas.
        
    Returns:
        The pixelized image as a NumPy array.
    """
    # Get the dimensions of the image
    height, width, _ = image.shape

    # Create a copy of the image to modify
    pixelized_image = np.copy(image)

    # Loop through the image in steps of base_block_size
    for y in range(0, height, base_block_size):
        for x in range(0, width, base_block_size):
            # Define the coordinates of the current block
            y1, y2 = y, min(y + base_block_size, height)
            x1, x2 = x, min(x + base_block_size, width)

            # Calculate the standard deviation of the block
            block = image[y1:y2, x1:x2]
            std_dev = np.std(block)

            # Determine the block size based on the detail threshold
            if std_dev > detail_threshold:
                block_size = base_block_size // 2  # More detailed pixelization
            else:
                block_size = base_block_size

            # Apply pixelization with the determined block size
            for sub_y in range(y1, y2, block_size):
                for sub_x in range(x1, x2, block_size):
                    sub_y1, sub_y2 = sub_y, min(sub_y + block_size, y2)
                    sub_x1, sub_x2 = sub_x, min(sub_x + block_size, x2)
                    sub_block = image[sub_y1:sub_y2, sub_x1:sub_x2]
                    average_color = np.mean(sub_block, axis=(0, 1)).astype(int)
                    pixelized_image[sub_y1:sub_y2, sub_x1:sub_x2] = average_color

    return pixelized_image



def apply_clustering_with_pixelization(image, num_clusters=8, block_size=10):
    """
    Apply clustering with pixelization to an image.
    
    Parameters:
        image: The input image as a NumPy array.
        num_clusters: The number of clusters for the k-means algorithm.
        block_size: The size of each block for pixelization.
        
    Returns:
        The pixelized image as a NumPy array.
    """
    # Reshape the image for clustering
    reshaped_image = image.reshape((-1, 3))

    # Apply k-means clustering
    kmeans = KMeans(n_clusters=num_clusters, random_state=0).fit(reshaped_image)
    clustered_image = kmeans.cluster_centers_[kmeans.labels_].reshape(image.shape).astype(int)

    # Get the dimensions of the clustered image
    height, width, _ = clustered_image.shape

    # Create a copy of the clustered image to modify
    pixelized_image = np.copy(clustered_image)

    # Loop through the image in steps of block_size
    for y in range(0, height, block_size):
        for x in range(0, width, block_size):
            # Define the coordinates of the current block
            y1, y2 = y, min(y + block_size, height)
            x1, x2 = x, min(x + block_size, width)

            # Calculate the average color of the block
            block = clustered_image[y1:y2, x1:x2]
            average_color = np.mean(block, axis=(0, 1)).astype(int)

            # Set the color of the block to the average color
            pixelized_image[y1:y2, x1:x2] = average_color

    return pixelized_image


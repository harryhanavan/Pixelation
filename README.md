# Pixelation Project

This project implements various pixelation techniques for image processing. Each method offers different approaches to pixelating an image, allowing for customization based on the desired outcome.

## Pixelation Methods

### 1. Basic Pixelation

- **Description:** Divides the image into equal-sized blocks and replaces each block with a single color, typically the average color of the original block.
- **Parameters:**
  - `block_size`: Size of the blocks for pixelation. Larger values result in more pronounced pixelation.
- **Reference:** [PyImageSearch](https://pyimagesearch.com/2020/04/06/blur-and-anonymize-faces-with-opencv-and-python/)

### 2. Adaptive Pixelation

- **Description:** Adjusts the pixelation block size based on the local variance of the image. Areas with higher variance (more details) are pixelated less, while areas with lower variance are pixelated more.
- **Parameters:**
  - `min_block_size`: Minimum block size for pixelation.
  - `max_block_size`: Maximum block size for pixelation.
  - `variance_threshold`: Threshold for variance to decide the block size. Lower values result in more adaptive pixelation.
- **Concepts and References:**
  - **Adaptive Homomorphic Filtering:** Used for denoising laser imaging by adapting to the characteristics of the image. This concept can be extended to adaptive pixelation by adjusting the filtering based on local features ([MDPI](https://www.mdpi.com/2304-6732/6/2/45)).
  - **Adaptive Gamma Correction (AGC):** A method for dynamically determining intensity transformation functions based on the input image characteristics. AGC can be incorporated into an adaptive pixelation process to ensure good contrast and brightness ([EURASIP Journal on Image and Video Processing](https://jivp-eurasipjournals.springeropen.com/articles/10.1186/s13640-019-0495-5)).
  - **Spatially Adaptive Support:** Involves adapting the support or window size for image filtering based on local image properties. For adaptive pixelation, this could mean varying the pixelation block size based on local image content ([LASIP - Local Approximations in Signal and Image Processing](https://webpages.tuni.fi/lasip/pub/Katkovnik_08_WITMSE.pdf)).

### 3. Clustering with Pixelization (K-means Clustering)

- **Description:** Uses k-means clustering to group similar pixels and applies pixelation within each cluster, aiming to preserve more structural information in the image.
- **Parameters:**
  - `num_clusters`: Number of clusters for k-means.
  - `block_size`: Size of the blocks for pixelation within each cluster.
- **Reference:** [OpenCV Documentation](https://docs.opencv.org/3.4/d1/d5c/tutorial_py_kmeans_opencv.html)

### 4. Gaussian Blur

- **Description:** Applies Gaussian blur to the image, which is not strictly pixelation but can be used for anonymizing faces in images.
- **Parameters:**
  - `kernel_size`: Size of the Gaussian kernel. Larger values result in more blurring.
- **Reference:** [GitHub - BlurFaceDetection](https://github.com/dvirk-kiner/BlurFaceDetection/blob/main/BlurFaces.py)

### 5. Face Morphing (Experimental)

- **Description:** A more complex technique that involves warping and blending multiple face images. Not strictly a form of pixelation.
- **Reference:** [Medium - Face Morphing Using OpenCV](https://medium.com/@thakuravnish2313/face-morphing-using-opencv-a-fun-experiment-with-python-81cf791fe464)

## Usage

To use these pixelation methods, import the desired function from the `pixelation_methods.py` file and apply it to your image. For example:

```python
from pixelation_methods import apply_basic_pixelization
import cv2

image = cv2.imread('path/to/image.jpg')
pixelated_image = apply_basic_pixelization(image, block_size=10)
cv2.imshow('Pixelated Image', pixelated_image)
cv2.waitKey(0)
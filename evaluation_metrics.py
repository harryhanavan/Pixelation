import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim


def calculate_psnr(original_image, pixelated_image):
    """
    Calculates the Peak Signal-to-Noise Ratio (PSNR) between the original and pixelated images.

    :param original_image: Original image.
    :param pixelated_image: Pixelated image.
    :return: PSNR value.
    """
    mse = np.mean((original_image - pixelated_image) ** 2)
    if mse == 0:
        return 100
    max_pixel = 255.0
    psnr = 20 * np.log10(max_pixel / np.sqrt(mse))
    return psnr


def calculate_ssim(original_image, pixelated_image):
    # Convert images to grayscale as SSIM comparison is done on one channel
    grayA = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(pixelated_image, cv2.COLOR_BGR2GRAY)

    # Use OpenCV to compute SSIM between two images
    score, diff = cv2.quality.QualitySSIM_compute(grayA, grayB)

    # The score returned is a mean SSIM score for all channels.
    return score[0]

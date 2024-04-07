import cv2

def calculate_ssim_opencv(image1, image2):
    # Convert images to grayscale
    grayA = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

    # Compute SSIM between two images
    (score, diff) = cv2.quality.QualitySSIM_compute(grayA, grayB)
    
    # The score returned is a mean SSIM score for all channels.
    return score[0]

# Read images
image1 = cv2.imread(r'C:\Users\harry\Documents\GitHub\Pixelation\Input\000001.jpg')
image2 = cv2.imread(r'C:\Users\harry\Documents\GitHub\Pixelation\Output\000001_Basic Pixelization_block_size10.jpg')

# Calculate SSIM
ssim_value = calculate_ssim_opencv(image1, image2)
print(f"SSIM value: {ssim_value}")
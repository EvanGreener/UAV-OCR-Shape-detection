import cv2 
import pytesseract
import numpy as np
from preprocessing_utils import get_grayscale, deskew, thresholding, remove_noise
from PIL import Image
from blur_detection import detect_blur_fft

# Page segmentation mode 
# --psm 10 = Treat image as a single character
single_char_config = r'--oem 3 --psm 10'

capture = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = capture.read()
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    # Detect if image is a not blurred
    (mean, blurry) = detect_blur_fft(frame)
    if not blurry:
        # Preprocessing
        frame = deskew(frame)
        frame = remove_noise(frame)
        frame = get_grayscale(frame)
        frame = thresholding(frame)
        # Display the resulting frame
        results = pytesseract.image_to_string(frame)
    
    if cv2.waitKey(1) == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()



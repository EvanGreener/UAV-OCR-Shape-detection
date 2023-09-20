import cv2 
import pytesseract
import numpy as np
import preprocessing_utils as ppu
from PIL import Image

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
    # Our operations on the frame come here
    frame = ppu.deskew(frame)
    frame = ppu.remove_noise(frame)
    frame = ppu.get_grayscale(frame)
    frame = ppu.thresholding(frame)

    # Display the resulting frame
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()



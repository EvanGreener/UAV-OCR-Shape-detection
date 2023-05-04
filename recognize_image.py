from tesserocr import get_languages, tesseract_version, PyTessBaseAPI, PSM
import cv2
import numpy as np
import imutils
from string import ascii_letters

# Taken from https://pyimagesearch.com/2021/11/22/improving-ocr-results-with-basic-image-processing/
def preProcess(frame):
    # Grayscale the image
    gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # threshold the image using Otsu's thresholding method
    thresh = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    # Distance transform to remove noise 
    dist = cv2.distanceTransform(thresh, cv2.DIST_L2, 5)
    dist = cv2.normalize(dist, dist, 0, 1.0, cv2.NORM_MINMAX)
    dist = (dist * 255).astype("uint8")
    # threshold image again
    dist = cv2.threshold(dist, 0, 255,
        cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    # apply an "opening" morphological operation to disconnect components
    # in the image
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
    opening = cv2.morphologyEx(dist, cv2.MORPH_OPEN, kernel)
    # find contours in the opening image, then initialize the list of
    # contours which belong to actual characters that we will be OCR'ing
    cnts = cv2.findContours(opening.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    chars = []
    # loop over the contours
    for c in cnts:
        # compute the bounding box of the contour
        (x, y, w, h) = cv2.boundingRect(c)
        # check if contour is at least 35px wide and 100px tall, and if
        # so, consider the contour a digit
        if w >= 35 and h >= 100:
            chars.append(c)
    # compute the convex hull of the characters
    chars = np.vstack([chars[i] for i in range(0, len(chars))])
    hull = cv2.convexHull(chars)
    # allocate memory for the convex hull mask, draw the convex hull on
    # the image, and then enlarge it via a dilation
    mask = np.zeros(frame.shape[:2], dtype="uint8")
    cv2.drawContours(mask, [hull], -1, 255, -1)
    mask = cv2.dilate(mask, None, iterations=2)
    cv2.imshow("Mask", mask)
    # take the bitwise of the opening image and the mask to reveal *just*
    # the characters in the image
    return cv2.bitwise_and(opening, opening, mask=mask)

def main():
    vid = cv2.VideoCapture(0)
    with PyTessBaseAPI(path='/usr/share/tessdata', psm=PSM.OSD_ONLY) as api:
        frame_count = 0
        while(True):
            if frame_count < 10:
                # Capture the video frame
                # by frame
                ret, frame = vid.read()
            
                # Display the resulting frame
                #cv2.imshow('frame', frame)

                final = preProcess(frame)

                # Read characters only
                api.SetVariable('tessedit_char_whitelist', ascii_letters)
                api.SetImageFile(final)
                # Get characters from image
                print(api.GetUTF8Text())

            # the 'q' button is set as the
            # quitting button you may use any
            # desired button of your choice
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    # After the loop release the cap object
    vid.release()
    # Destroy all the windows
    cv2.destroyAllWindows()


if __name__ == "__main__":
    print(tesseract_version())
    print(get_languages('/usr/share/tessdata'))
    # main()
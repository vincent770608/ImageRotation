import statistics
import numpy as np
import glob
import cv2

def RotateImage(image_process):
    ret, contours, hierarchy = cv2.findContours(image_process, 1, 2)
    height = np.size(image_process, 0)
    width = np.size(image_process, 1)
    angles = []
    for cnt in contours:

        if cv2.contourArea(cnt) > 1000:
            rect = cv2.minAreaRect(cnt)

            angle = rect[2]
            if angle < -45:
                angle += 90

            angles.append(angle)

    finalangle = statistics.median(angles)
    print(" Image's angle:", finalangle)
    # return finalangle

    if finalangle != 0.0 or finalangle != -0.0:

        center = (width / 2, height / 2)
        # Size of the upright rectangle bounding the rotated rectangle
        size = (width, height)

        M = cv2.getRotationMatrix2D((size[0] / 2, size[1] / 2), finalangle, 1.0)
        # Cropped upright rectangle
        cropped = cv2.getRectSubPix(image, size, center)
        cropped = cv2.warpAffine(cropped, M, size)
        croppedW = height if height > width else width
        croppedH = height if height < width else width

        cv2.getRectSubPix(cropped, (int(croppedW), int(croppedH)), (size[0] / 2, size[1] / 2))
        # return cropped, True
        return cropped, True
    else:
        print("no need to rotate")
        return None, False

def DetectEdge(image_process):
    v = np.median(image_process)
    # apply automatic Canny edge detection using the computed median
    lower = int(max(0, (1.0 - 0.33) * v))
    upper = int(min(255, (1.0 + 0.33) * v))

    print(" lower =", str(lower), ",upper = ", str(upper))

    image_process = cv2.Canny(image_process, lower, upper)

    tupelem = (6, 6)
    print(" Dilate structure:", tupelem)
    element = cv2.getStructuringElement(cv2.MORPH_RECT, tupelem)
    image_process = cv2.dilate(image_process, element)
    return image_process

if __name__=='__main__':
    imname = "form-sample.JPG"

    for imagePath in glob.glob("images/input/"+imname):
        image = cv2.imread(imagePath)
        print("Load image",imagePath)
        image_process = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image_process = DetectEdge(image_process)

        cropped , boo= RotateImage(image_process)
        if boo == True:
            cv2.imwrite("images/output/rotated_"+str(imname),cropped)


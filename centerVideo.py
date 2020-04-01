import imutils
import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import math
import time

def display_contours(image, c, cX, cY):
    # draw the contour and center of the shape on the image
    s_display = "({}, {})".format(cX, cY)
    cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
    cv2.circle(image, (cX, cY), 7, (255, 255, 255), -1)
    cv2.putText(
        image,
        s_display,
        (cX - 20, cY - 20),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (255, 255, 255),
        2,
    )

def get_average_position(positions):
    sX = 0
    sY = 0
    for cXY in positions:
        sX += cXY[0]
        sY += cXY[1]
    l = len(positions)

    return (int(sX/l), int(sY/l))

def get_distance(cX1, cY1, cX2, cY2):
    return math.sqrt((cX2-cX1)**2 + (cY2-cY1)**2)

def init_camera():
    


    cam = PiCamera()
    cam.resolution = (640, 480)
    cam.framerate = 26
    cam.iso = 800
    cam.exposure_mode = "auto"
    cam.awb_mode = "off"
    cam.awb_gains = (1.1, 1.6)
    cam.rotation = 180
    rawCapture = PiRGBArray(cam, size=(640, 480))
    print("Camera is starting...")

    time.sleep(2)
    cam.exposure_mode = "off"
    cam.shutter_speed = 12000
    
    return (cam, rawCapture)
    

def get_target_position(cam, rawCapture, verbose, display, iteration = 52): 
    MIN_AREA = 400

    iteration_cpt = 0  
        # Range for upper range
    lower_green = np.array([47, 10, 10])
    upper_green = np.array([65, 255, 255]) 
    target_coord_list = []
    for frame in cam.capture_continuous(
        rawCapture, format="bgr", use_video_port=True
    ):
        image = frame.array
        imageCP = image
        #cv2.imshow("In", image)

        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        blurred = cv2.GaussianBlur(hsv, (5, 5), 0)
        mask = cv2.inRange(hsv, lower_green, upper_green)

        if display:
            cv2.imshow("Mask", mask)

        # find contours in the thresholded image
        cnts = cv2.findContours(
            mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        cnts = imutils.grab_contours(cnts)

        # loop over the contours
        closer_point = (10000, 10000)
        closer_point_distance = 10000000
        for c in cnts:
            if cv2.contourArea(c) < MIN_AREA:
                continue

            # compute the center of the contour
            M = cv2.moments(c)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            if not len(target_coord_list):
                print(f'Selected target at : ~({cX}, {cY})')
                target_coord_list.append((cX,cY))
            else:
                last_point_added = target_coord_list[-1]
                temp_dist = get_distance(cX, cY, last_point_added[0], last_point_added[1])
                if temp_dist < closer_point_distance:
                    closer_point = (cX,cY)
                    closer_point_distance = temp_dist

            if display:
                display_contours(image, c, cX, cY)

        if closer_point[0] != 10000:
            target_coord_list.append(closer_point)
            cv2.circle(image, closer_point, 5, (0, 0, 255), -1)

        if display:
            # show the image
            cv2.imshow("Out", image)
            cv2.moveWindow("Out", 700, 20)

        cv2.waitKey(1)
        rawCapture.truncate(0)
        if len(target_coord_list) > iteration:
            if verbose:
                print("Image analysis terminated")
            image = frame.array
            avr = get_average_position(target_coord_list)
            cv2.circle(imageCP, avr, 5, (255, 0, 0), -1)
            cv2.imshow("Average", imageCP)
            cv2.moveWindow("Average", 350, 100)
            cv2.waitKey(0)
            return avr

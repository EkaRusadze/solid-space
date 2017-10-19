import cv2
import numpy as np


class detector:
    def __init__(self, colorConfig, name):
        self.name = name
        f = open(colorConfig)
        self.minhue = int(f.readline())
        self.minsat = int(f.readline())
        self.minint = int(f.readline())
        self.maxhue = int(f.readline())
        self.maxsat = int(f.readline())
        self.maxint = int(f.readline())
        f.close()

    def detect(self, cap):
        cx = -1
        cy = -1
        _, frame = cap.read()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        # Threshold the HSV image to get only necessary colors
        lowerColor = np.array([self.minhue, self.minsat, self.minint])
        upperColor = np.array([self.maxhue, self.maxsat, self.maxint])
        mask = cv2.inRange(hsv, lowerColor, upperColor)
        # Bitwise-AND mask and original image
        res = cv2.bitwise_and(frame, frame, mask=mask)
        im2, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) != 0:

            # find the biggest area
            c = max(contours, key=cv2.contourArea)
            M = cv2.moments(c)

            area = cv2.minAreaRect(c)
            try:
                known_dist = 0.15
                known_width = 0.04
                focal_length = 649
                distance = known_width * focal_length / area[1][0]
                #   print(distance)

                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])
                cv2.circle(res, (cx, cy), 5, (0, 255, 0), -1)
            except:
                M = 0
                cx = -1
                cy = -1
            x, y, w, h = cv2.boundingRect(c)
            # draw the book contour (in green)
            cv2.rectangle(res, (x, y), (x + w, y + h), (0, 255, 0), 2)
        return res, mask, cx, cy

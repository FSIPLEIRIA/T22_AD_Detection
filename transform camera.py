# import necessary libraries

import cv2
import numpy as np

# Turn on Laptop's webcam
cap = cv2.VideoCapture(0)
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
print(width, height)
while True:

    ret, frame = cap.read()

    # Locate points of the documents
    # or object which you want to transform
    pts1 = np.float32([[320, 520], [960, 520],
                       [0, 720], [1280, 720]])
    pts2 = np.float32([[0, 0], [1280, 0],
                       [0, 720], [1280, 720]])

    # Apply Perspective Transform Algorithm
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    result = cv2.warpPerspective(frame, matrix, (1280, 720))

    # Wrap the transformed image
    image = cv2.circle(frame, (320, 520), radius=6, color=(0, 0, 255), thickness=-1)
    image = cv2.circle(frame, (960, 520), radius=6, color=(0, 0, 255), thickness=-1)
    image = cv2.circle(frame, (0, 720), radius=6, color=(0, 0, 255), thickness=-1)
    image = cv2.circle(frame, (1280, 720), radius=6, color=(0, 0, 255), thickness=-1)

    cv2.imshow('frame', frame)  # Initial Capture
    cv2.imshow('frame1', result)  # Transformed Capture

    if cv2.waitKey(24) == 27:
        break

cap.release()
cv2.destroyAllWindows()


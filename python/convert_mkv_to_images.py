import numpy as np
import cv2

mov = 'target.mkv'
cap = cv2.VideoCapture(mov)
fps = cap.get(cv2.CAP_PROP_FPS)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)

count = 0
while(cap.isOpened()):
    ret, frame = cap.read()
    if ret:
        count += 1
        output = 'mkv2img/{:05}.jpg'.format(count)
        print(output)
        cv2.imwrite(output, frame)
    else:
        break

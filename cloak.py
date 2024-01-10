'''
to detect red
lower are 150H, 90S, 0V
upper are max
'''

import cv2
import numpy as np

def create_mask(frame, lower_hsv, upper_hsv, kernel_size=3):
	inspect = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	mask = cv2.inRange(inspect, lower_hsv, upper_hsv)
	mask = cv2.medianBlur(mask, 3)
	kernel = np.ones((kernel_size, kernel_size), np.uint8)
	mask = cv2.dilate(mask, kernel, iterations=5)

	return mask

def create_trackbars():
	cv2.createTrackbar("lower_hue", "bars", 68, 180, nothing)
	cv2.createTrackbar("lower_saturation", "bars", 55, 255, nothing)
	cv2.createTrackbar("lower_value", "bars", 54, 255, nothing)
	cv2.createTrackbar("upper_hue", "bars", 110, 180, nothing)
	cv2.createTrackbar("upper_saturation", "bars", 255, 255, nothing)
	cv2.createTrackbar("upper_value", "bars", 255, 255, nothing)

def get_trackbar_values():
	lower_value = cv2.getTrackbarPos("lower_value", "bars")
	lower_hue = cv2.getTrackbarPos("lower_hue", "bars")
	lower_saturation = cv2.getTrackbarPos("lower_saturation", "bars")
	upper_hue = cv2.getTrackbarPos("upper_hue",  "bars")
	upper_saturation = cv2.getTrackbarPos("upper_saturation",  "bars")
	upper_value = cv2.getTrackbarPos("upper_value",  "bars")

	return lower_hue, lower_saturation, lower_value, upper_hue, upper_saturation, upper_value

def nothing(x):
	pass

cap = cv2.VideoCapture(0)
bars = cv2.namedWindow("bars")

create_trackbars()

# Capture the initial frame for creating the background
while True:
	cv2.waitKey(1000)
	ret, init_frame = cap.read()
	if ret:
		break

while True:
	ret, frame = cap.read()

	lower_hue, lower_saturation, lower_value, upper_hue, upper_saturation, upper_value = get_trackbar_values()
	lower_hsv = np.array([lower_hue, lower_saturation, lower_value])
	upper_hsv = np.array([upper_hue, upper_saturation, upper_value])

	mask = create_mask(frame, lower_hsv, upper_hsv)

	mask_inv = 255 - mask

	# Bitwise operations to get the final frame
	frame_inv = cv2.bitwise_and(frame, frame, mask=mask_inv)

	# Bitwise operations to get the blanket area
	blanket_area = cv2.bitwise_and(init_frame, init_frame, mask=mask)

	# Combine the two frames
	final = cv2.bitwise_or(frame_inv, blanket_area)

	cv2.imshow("Cloak Cam", final)

	if cv2.waitKey(3) == ord('q'):
		break

cv2.destroyAllWindows()
cap.release()
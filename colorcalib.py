#import packages to run the color calibration
#from  imutils.video.pivideostream import PiVideoStream
#import imutils
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np

def nothing(x):
	pass

#usual IR
#numpyL = np.array([0,0,150])
#numpyH = np.array([130,255,255])

#yellow
numpyL = np.array([15,100,100])
numpyH = np.array([45,255,255])
#we should have these read from a file
print("I am soupy")
file=open("color.txt","r")
list_of_things=file.readlines()
#should return a list like [0,3,25] etc

print("I am not soupy anymore :(")
cv2.namedWindow("Calibration", 0)
cv2.createTrackbar("Lower: H", "Calibration", numpyL[0], 179, nothing)
cv2.createTrackbar("Upper: H", "Calibration", numpyH[0], 179, nothing)
cv2.createTrackbar("Lower: S", "Calibration", numpyL[1], 255, nothing)
cv2.createTrackbar("Upper: S", "Calibration", numpyH[1], 255, nothing)
cv2.createTrackbar("Lower: V", "Calibration", numpyL[2], 255, nothing)
cv2.createTrackbar("Upper: V", "Calibration", numpyH[2], 255, nothing)
cv2.moveWindow("Calibration", 0,0)

print("lemmedie")
#vs=PiVideoStream().start()
#oh I don't need params :))))
camera = PiCamera()
camera.resolution=(640,480)
camera.framerate=50
rawCapture=PiRGBArray(camera,size=(640,480))
time.sleep(1.0)

while True:
	image = vs.read()
	hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
	
	mask = cv2.inRange(hsv, numpyL, numpyH)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=4)

	LH = cv2.getTrackbarPos("Lower: H", "Calibration")
	UH = cv2.getTrackbarPos("Upper: H", "Calibration")
	LS = cv2.getTrackbarPos("Lower: S", "Calibration")
	US = cv2.getTrackbarPos("Upper: S", "Calibration")
	LV = cv2.getTrackbarPos("Lower: V", "Calibration")
	UV = cv2.getTrackbarPos("Upper: V", "Calibration")
	numpyL = np.array([LH, LS, LV])
	numpyH = np.array([UH, US, UV])

	cv2.imshow("Frame",image)
	cv2.imshow("Mask", mask)
	key = cv2.waitKey(1) & 0xFF
	if key==ord('q'):
		break

vs.stop()
cv2.destroyAllWindows()

#import packages to run the color calibration
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np
import sys

last_track = "Lower: H"
def last(x):
	pass
#I need to get the name of the trackbar last used, possible to achieve
#without having to use different functions for all?
#use last_track to enable the [ and ] feature

#usual IR
#numpyL = np.array([0,0,150])
#numpyH = np.array([130,255,255])

#yellow
numpyL = np.array([0,0,0])
numpyH = np.array([0,0,0])
#we should have these read from a file

print("I am soupy")
file=open("color.txt","r")
list_of_things=file.readlines()
n1=list_of_things[0].split()
n2=list_of_things[1].split()
for i in range(3):
	numpyL[i]=int(n1[i])
	numpyH[i]=int(n2[i])
file.close()
#should return a list like [0,3,25] etc
print(numpyL)
print(numpyH)
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
print("before camera")
camera = PiCamera()
camera.resolution=(640,480)
camera.framerate=32
rawCapture=PiRGBArray(camera,size=(640,480))
time.sleep(1.0)
print("after cam before loop")

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
#while True:
	#image = vs.read()
	print("before frame hi")
	image = frame.array
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
	rawCapture.truncate(0)
	key = cv2.waitKey(1) & 0xFF

	if key==ord('q'):
		break
	elif key==ord('['):
		#make it go down 5?
		#make it for the last uh--bar selected
	elif key==ord(']'):
		#make it go up 5
print("after loop")
#vs.stop()
cv2.destroyAllWindows()
open("color.txt","w").close() #supposed to clear out the file but idk?
working_file=open("color.txt","w")
working_file.write("%d %d %d\n"%(numpyL[0],numpyL[1],numpyL[2]))
working_file.write("%d %d %d\n"%(numpyH[0],numpyH[1],numpyH[2]))
working_file.close()

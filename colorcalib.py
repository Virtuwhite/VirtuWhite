#import packages to run the color calibration
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np
import sys

#last_track = "Lower: H"
#incomplete function, as of now it just passes because a function was needed
#to be passed into cv2.createTrackBar
#ideally the idea was it would keep track of the last trackbar touched/editted
#and allow the user to shift the values using the [ and ] keys
def last(x):
	pass

#numpy arrays are quick 2D arrays commonly used in python and image processing
#numpyL and numpyH both store the HSV values (L meaning lower, H meaning higher)
numpyL = np.array([0,0,0])
numpyH = np.array([0,0,0])

#print("I am soupy")
#reads in from a file "color.txt" the previous values stored there
#unsure if this works on new "machines" due to a machine's read/write permissions
file=open("color.txt","r")
list_of_things=file.readlines()
n1=list_of_things[0].split()
n2=list_of_things[1].split()
for i in range(3):
	numpyL[i]=int(n1[i])
	numpyH[i]=int(n2[i])
file.close()

#should return a list like [0,3,25] etc #these are mostly here for testing purposes
#print(numpyL)
#print(numpyH)
#print("I am not soupy anymore :(")

#creates the trackbars which you can use to calibrate the HSV values
cv2.namedWindow("Calibration", 0)
cv2.createTrackbar("Lower: H", "Calibration", numpyL[0], 179, last)
cv2.createTrackbar("Upper: H", "Calibration", numpyH[0], 179, last)
cv2.createTrackbar("Lower: S", "Calibration", numpyL[1], 255, last)
cv2.createTrackbar("Upper: S", "Calibration", numpyH[1], 255, last)
cv2.createTrackbar("Lower: V", "Calibration", numpyL[2], 255, last)
cv2.createTrackbar("Upper: V", "Calibration", numpyH[2], 255, last)
cv2.moveWindow("Calibration", 0,0)

#search "blob detection" to understand the theory behind this
#as it is right now, I am fairly dissatisfied with the performance of the cv2
#simpleblobdetector, it is suggested to find way to fine-tune it or write one
#yourself
params=cv2.SimpleBlobDetector_Params()
params.minThreshold=220
params.maxThreshold=255
params.blobColor=255
params.filterByArea=False
params.filterByCircularity=False
params.filterByConvexity=False
params.filterByInertia=True
params.minInertiaRatio=0.01

#different versions of cv2 have different function calls, but they do the
#same thing
version=(cv2.__version__).split('.')
if int(version[0]) < 3:
	detector=cv2.SimpleBlobDetector(params)
else:
	detector=cv2.SimpleBlobDetector_create(params)

#oh I don't need params :))))
#print("before camera")
camera = PiCamera()
camera.resolution=(320,240)
camera.framerate=32
rawCapture=PiRGBArray(camera,size=(320,240))
#sleeping the camera to help it warm up
time.sleep(1.0)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	image = frame.array
	hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
	
	mask = cv2.inRange(hsv, numpyL, numpyH)
	#eroding and dilating a mask is fairly common practice to reduce noise
	#in an image, however upon testing it has ended up blotting out the pen
	#tip as well
	#mask = cv2.erode(mask, None, iterations=2)
	#mask = cv2.dilate(mask, None, iterations=4)
	keypts=detector.detect(mask)
	#the blob detector is simply to detect whether the normal performance
	#will detect the blobs as well
	if len(keypts) > 0:
		print("number of pts detected: %d" % len(keypts))

	LH = cv2.getTrackbarPos("Lower: H", "Calibration")
	UH = cv2.getTrackbarPos("Upper: H", "Calibration")
	LS = cv2.getTrackbarPos("Lower: S", "Calibration")
	US = cv2.getTrackbarPos("Upper: S", "Calibration")
	LV = cv2.getTrackbarPos("Lower: V", "Calibration")
	UV = cv2.getTrackbarPos("Upper: V", "Calibration")
	numpyL = np.array([LH, LS, LV])
	numpyH = np.array([UH, US, UV])

	cv2.imshow("Frame",image)
	#cv2.imshow("HSV",hsv)
	cv2.imshow("Mask", mask)
	rawCapture.truncate(0)
	key = cv2.waitKey(1) & 0xFF
	
	#you can quit the program by pressing q
	if key==ord('q'):
		break
	#the [ and ] functions are thus far not working/WIP
	'''elif key==ord('['):
		print("[ key pressed!")
		#make it go down 5?
		#make it for the last uh--bar selected
	elif key==ord(']'):
		print("] key pressed!")'''
		#make it go up 5

#print("after loop")
cv2.destroyAllWindows()
#supposed to clear out the file and write to color.txt
open("color.txt","w").close()
working_file=open("color.txt","w")
working_file.write("%d %d %d\n"%(numpyL[0],numpyL[1],numpyL[2]))
working_file.write("%d %d %d\n"%(numpyH[0],numpyH[1],numpyH[2]))
working_file.close()

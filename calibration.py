#still working things out rn hold on
from imutils.video.pivideostream import PiVideoStream
import imutils
import time
import cv2
import numpy as np
from pymouse import PyMouse

#perspective_transform stores the points according to (top left, top right
#	bottom right, bottom left)
open('perspective_transform.txt','w').close()

xd, yd = PyMouse().screen_size()
print("%d %d"%(xd,yd))
#infrared??
#gotta change these to accomodate for the 
print("Soupy appears in calibration! >:D")
#numpyL = np.array([0,0,150])
#numpyH = np.array([130,255,255])
numpyL=np.array([0,0,0])
numpyH=np.array([0,0,0])
file=open("color.txt","r")
list_of_things=file.readlines()
n1=list_of_things[0].split()
n2=list_of_things[1].split()
for i in range(3):
	numpyL[i]=int(n1[i])
	numpyH[i]=int(n2[i])
file.close()
print("Let me rest in peace")

#vs = PiVideoStream(resolution=(640,480)).start()
params=cv2.SimpleBlobDetector_Params()

params.minThreshold=220
params.maxThreshold=255
params.blobColor=255
params.filterByArea=True
params.minArea=5
params.filterByCircularity=False
params.filterByConvexity=False
params.filterByInertia=True
params.minInertiaRatio=0.01

version=(cv2.__version__).split('.')
if int(version[0]) < 3 :
	detector = cv2.SimpleBlobDetector(params)
else:
	detector = cv2.SimpleBlobDetector_create(params)

time.sleep(2.0)

Pts=([[0,0],
	[50,0],
	[0,50],
	[50,50]]) #default points
i = 0

while True:
	if i == 0:
		break
	image = vs.read()
	height, width = image.shape[:2]

	hsv=cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
	mask = cv2.inRange(hsv,numpyL,numpyH)
	#mask=cv2.erode(mask,None,iterations=1)

	keypts=detector.detect(mask)
	numPts = len(keypts)
	if numPts > 0:
		x = keypts[0].pt[0]
		y = keypts[0].py[1]
		#thus x and y and stuff
		Pts[i] = [x,y]
		i+=1
		time.sleep(2.0)

vs.stop()
cv2.destroyAllWindows()
#so Pts should have in the order TL, TR, BR, BL points
#You gotta store these in uhh... a file somewhere
working_file=open('perspective_transform.txt','w')
for i in range(len(Pts)):
	working_file.write("%d %d\n"%(Pts[i][0], Pts[i][1]))

working_file.close()

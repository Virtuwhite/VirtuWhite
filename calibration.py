#imports
#PiVideoStream is the threaded (and higher fps performer)
from imutils.video.pivideostream import PiVideoStream
import imutils
import time
import cv2
import numpy as np
from pymouse import PyMouse

#perspective_transform stores the points according to (top left, top right
#	bottom right, bottom left)
open('perspective_transform.txt','w').close()

#xd, yd = PyMouse().screen_size()
#print("%d %d"%(xd,yd))
#gets the color calibration of the IR pen
#gotta change these to accomodate for the 
numpyL=np.array([0,0,0])
numpyH=np.array([0,0,0])
file=open("color.txt","r")
#basically parsing out the colors from color.txt
list_of_things=file.readlines()
n1=list_of_things[0].split()
n2=list_of_things[1].split()
for i in range(3):
	numpyL[i]=int(n1[i])
	numpyH[i]=int(n2[i])
file.close()
#print("Let me rest in peace")
#print(numpyL)
#print(numpyH)

# Simple instructions displayed on the screen (very particular about the order)
# possible future development(allowing any particular order with proper analysis
# of the inputted points
img=np.zeros((100,600,3),np.uint8)
cv2.putText(img,'Touch in the order: Top Left, Top Right, Bottom Right, Bottom Left of your entire display', (10,50),cv2.FONT_HERSHEY_SIMPLEX,0.4,(255,255,255),1,cv2.LINE_AA)
cv2.imshow("instructions", img)

vs = PiVideoStream().start()#(resolution=(640,480)).start()
params=cv2.SimpleBlobDetector_Params()

params.minThreshold=220
params.maxThreshold=255
params.blobColor=255
params.filterByArea=False
#params.minArea=5
params.filterByCircularity=False
params.filterByConvexity=False
params.filterByInertia=True
params.minInertiaRatio=0.01

#depends on the version of cv2
version=(cv2.__version__).split('.')
if int(version[0]) < 3 :
	detector = cv2.SimpleBlobDetector(params)
else:
	detector = cv2.SimpleBlobDetector_create(params)

#warming up camera
time.sleep(2.0)

Pts=([[0,0],
	[50,0],
	[0,50],
	[50,50]]) #default points
i = 0
#print("made it here")
#print("You want to touch in the order of TL, TR, BR, BL")
#print("Hope to change this in the future, probably with flip commands and such maybe! Look into camera flipping how do")
#this loop is to store the 4 points as the corner points
while i < 4:
	image = vs.read()
	height, width = image.shape[:2]

	hsv=cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
	mask = cv2.inRange(hsv,numpyL,numpyH)
	cv2.imshow("frame",image)
	cv2.imshow("Mask", mask)
	key=cv2.waitKey(1)
	if key==ord("q"):
		break
	keypts=detector.detect(mask)
	numPts = len(keypts)
	if numPts > 0:
		#print("more than 1 keypoint, i = %d" % (i))
		x = keypts[0].pt[0]
		y = keypts[0].pt[1]
		print("x,y: %d %d" % (x,y))
		#thus x and y and stuff
		Pts[i] = [x,y]
		i+=1
		#put to sleep as to prevent a single frame/location to be 
		#read multiple times on accident
		time.sleep(2.0)

vs.stop()
cv2.destroyAllWindows()

#so Pts should have in the order TL, TR, BR, BL points
#You gotta store these in perspective_transform.txt

#so you probably have points stored in TL, TR, BR, BL

#usually with the first 2 points you can figure out the orientation of
#the camera--and thus can shuffle the  points accordingly

#how does hflip and vflip work actually, under the presumption that
#the camera is rotated at some angle, can the camera be resorted
#how do you determine whether something is on the
#same axis as you and not on the diagonal axis???
#you can separate the points into 2 groups, the first 2 & the last 2
#the order the 1st 2 have demonstrate the general axis the 2nd 2 
#should have??
#MAN IDK geometry is hard :(


#stores the points in a file
working_file=open('perspective_transform.txt','w')
for i in range(len(Pts)):
	working_file.write("%d %d\n"%(Pts[i][0], Pts[i][1]))
print("????")
working_file.close()

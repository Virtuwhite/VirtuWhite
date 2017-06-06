#import the necessary packages
#from __future__ import print_function
from imutils.video.pivideostream import PiVideoStream
#from imutils.video import FPS
#from picamera.array import PiRGBArray
#from picamera import PiCamera
import argparse
import imutils
import time
import cv2
import numpy as np
from pymouse import PyMouse

m = PyMouse()
xd, yd = m.screen_size()

def nothing(x):
	pass

print("before soup")
scr=np.array([[0.,0.],[0.,0.],[0.,0.],[0.,0.]],dtype="float32")
loc_file=open("perspective_transform.txt","r")
strang=loc_file.readlines() #this returns a list, like ['0 0', '0 50'...]
#I suppose this takes the first line############################here
p = 0
for i in strang:
	soup=i.split()
	loop=[float(soup[0]), float(soup[1])]
	print(i)
	print(soup)
	print(loop[0]+loop[1]) 
	scr[p][0] += int(soup[0])
	scr[p][1] += int(soup[1])
	p+=1

loc_file.close()
print("aftersoup")
#ordered TL, TR, BL, BR 
#scr = np.array([
#	[168, 78],
#	[259,90],
#	[154,130],
#	[242,134]],dtype="float32")
print(scr)
dst = np.array([
	[0,0],
	[639,0],
	[0,479],
	[639,479]], dtype="float32")
print(dst)
wer = cv2.getPerspectiveTransform(scr,dst)

#numpyL = np.array([0,0,150])
#numpyH = np.array([130,255,255])
	
#yellow
numpyL = np.array([15,100,100])
numpyH = np.array([45,255,255])		

cv2.namedWindow("Calibration", 0)
cv2.createTrackbar("Lower: H", "Calibration", numpyL[0], 179, nothing)
cv2.createTrackbar("Upper: H", "Calibration", numpyH[0], 179, nothing)
cv2.createTrackbar("Lower: S", "Calibration", numpyL[1], 255, nothing)
cv2.createTrackbar("Upper: S", "Calibration", numpyH[1], 255, nothing)
cv2.createTrackbar("Lower: V", "Calibration", numpyL[2], 255, nothing)
cv2.createTrackbar("Upper: V", "Calibration", numpyH[2], 255, nothing)
cv2.moveWindow("Calibration", 0, 0)

def click(x, y, w, h):
	#this is supposed to take a point and translate it into window space
	m.move((x * xd / w),(y * yd / h))

def drag(x,y,w,h):
	m.drag((x * xd / w),(y * yd / h))

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-n", "--num-frames", type=int, default=100,
	help="num of frames to loop over for FPS test")
ap.add_argument("-d", "--display", type=int, default=-1,
	help="Whether or not frames should be displayed")
args = vars(ap.parse_args())
 
# initialize the camera and stream
#camera = PiCamera()
#camera.resolution = (640, 480)
#camera.framerate = 32
#rawCapture = PiRGBArray(camera, size=(640, 480))
#stream = camera.capture_continuous(rawCapture, format="bgr",
#	use_video_port=True)

print("Let's try something!")
vs = PiVideoStream().start()#resolution=(640,480)).start()
print("Is it failing here?")
params = cv2.SimpleBlobDetector_Params()

params.minThreshold = 220
params.maxThreshold = 255
params.blobColor = 255
params.filterByArea = True
params.minArea = 5
#params.maxArea = 20
params.filterByCircularity = False
params.filterByConvexity = False
params.filterByInertia = True
params.minInertiaRatio = 0.01

version = (cv2.__version__).split('.')
if int(version[0]) < 3 :
	detector = cv2.SimpleBlobDetector(params)
else:
	detector = cv2.SimpleBlobDetector_create(params)

time.sleep(2.0)
maus = True #When it's true, cam tracks IR pen, when false, only comp mouse
calibration = False

#detecting whether it is a mouse click or a mouse drag
frame_on = 0

while True:
	#so uh... let's check the PiVideoStream...
	#print("Henlo!")
	image = vs.read()
	height, width = image.shape[:2]
	
	#image = imutils.resize(image, width=640, height=480)
	#print("L: [%d %d %d]" % (numpyL[0], numpyL[1], numpyL[2]))
	hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
	pers = cv2.warpPerspective(image, wer, (640,480))	

	mask = cv2.inRange(hsv, numpyL, numpyH)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=4)
	
	if maus == True:
		keypts = detector.detect(mask)
		bro = len(keypts)
		print("Length of kpts: %d" % bro)
		'''for kp in  keypts:
			cv2.circle(image, (int(kp.pt[0]), int(kp.pt[1])), int(kp.size),(0,0,255))
			print("Locations: (%d, %d)" % (int(kp.pt[0]), int(kp.pt[1])))
			# So with this, I need to determine whether a point is
			# part of a drag or a click
			translate(int(kp.pt[0]),int(kp.pt[1]), width, height)'''
			#drag(int(kp.pt[0]),int(kp.pt[1]), width, height)

		#bro is the number of keypoits there are
		if bro > 0:
			#pt = keypts[0]
			x = keypts[0].pt[0]
			y = keypts[0].pt[1]
			print("%d %d" % (x, y))
			if frame_on == 0:
				click(int(x),int(y),width,height)
				frame_on = frame_on + 1
			else: #frameson > 0
				drag(int(x),int(y),width,height)
				frame_on = frame_on + 1			
			#this means there is a blob compared to last time
		else:
			frame_on = 0

	LH = cv2.getTrackbarPos("Lower: H", "Calibration")
	UH = cv2.getTrackbarPos("Upper: H", "Calibration")
	LS = cv2.getTrackbarPos("Lower: S", "Calibration")
	US = cv2.getTrackbarPos("Upper: S", "Calibration")
	LV = cv2.getTrackbarPos("Lower: V", "Calibration")
	UV = cv2.getTrackbarPos("Upper: V", "Calibration")
	numpyL = np.array([LH,LS,LV])
	numpyH = np.array([UH,US,UV])

	cv2.imshow("Frame", image)
	cv2.imshow("Mask", mask)
	cv2.imshow("warped", pers)
	key = cv2.waitKey(1) & 0xFF
	#print("key: " + key)
	if key == ord('q'):
		break
	elif key == ord('m'):
		maus = not maus
	elif key == ord('c'): #c for calibrate
		#I suppose you enter a calibration state?
		calibration = not calibration

vs.stop()
cv2.destroyAllWindows()

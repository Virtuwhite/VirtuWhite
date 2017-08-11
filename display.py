#import the necessary packages
from imutils.video.pivideostream import PiVideoStream
import argparse
import imutils
import time
import cv2
import numpy as np
from pymouse import PyMouse

#this is to instantiate a mouse click/drag effect
#and to acquire the dimensions of the screen you're working with (helps 
#to transform the points
m = PyMouse()
xd, yd = m.screen_size()

#to be passed into createTrackBar
def nothing(x):
	pass

#print("before soup")
scr=np.array([[0.,0.],[0.,0.],[0.,0.],[0.,0.]],dtype="float32")
loc_file=open("perspective_transform.txt","r")
strang=loc_file.readlines() #this returns a list, like ['0 0', '0 50'...]
#I suppose this takes the first line

#prase the points from perspective_transform.txt
#stored in a numpy array (scr for screen)
p = 0
for i in strang:
	soup=i.split()
	loop=[float(soup[0]), float(soup[1])]
	scr[p][0] += int(soup[0])
	scr[p][1] += int(soup[1])
	p+=1

loc_file.close()
#print("aftersoup")

minx = min(scr[0][0],scr[1][0],scr[2][0],scr[3][0])
maxx = max(scr[0][0],scr[1][0],scr[2][0],scr[3][0])
miny = min(scr[0][1],scr[1][1],scr[2][1],scr[3][1])
maxy = max(scr[0][1],scr[1][1],scr[2][1],scr[3][1])

#print(scr)
dst = np.array([
	[0,0],
	[639,0],
	[639,479],
	[0,479]], dtype="float32")
print(dst)

#constructs the perspective transformation matrix based on the points (scr)
#and the camera dimensions (640, 480 (dst))
wer = cv2.getPerspectiveTransform(scr,dst)

#numpyL = np.array([0,0,150])
#numpyH = np.array([130,255,255])
	
#yellow
#numpyL = np.array([15,100,100])
#numpyH = np.array([45,255,255])		
print("soupy!")
#I'm supposed to read from the file that's it
color_file=open("color.txt","r")
colon_cancer=color_file.readlines() #I want to die?
n1=colon_cancer[0].split()
n2=colon_cancer[1].split()
numpyL=np.array([int(n1[0]),int(n1[1]),int(n1[2])])
numpyH=np.array([int(n2[0]),int(n2[1]),int(n2[2])])
color_file.close()
print("not so soupy :(")
print("-----------------------")
print(numpyL)
print(numpyH)

def click(x, y, w, h):
	#this is supposed to take a point and translate it into window space
	m.click((x * xd / w)/2,(y * yd / h)/2)

def drag(x,y,w,h):
	m.drag((x * xd / w)/2,(y * yd / h)/2)

# construct the argument parse and parse the arguments
'''ap = argparse.ArgumentParser()
ap.add_argument("-n", "--num-frames", type=int, default=100,
	help="num of frames to loop over for FPS test")
ap.add_argument("-d", "--display", type=int, default=-1,
	help="Whether or not frames should be displayed")
args = vars(ap.parse_args())'''
 
# initialize the camera and stream
#camera = PiCamera()
#camera.resolution = (640, 480)
#camera.framerate = 32
#rawCapture = PiRGBArray(camera, size=(640, 480))
#stream = camera.capture_continuous(rawCapture, format="bgr",
#	use_video_port=True)

print("Let's try something!")
params = cv2.SimpleBlobDetector_Params()
params.minThreshold = 220
params.maxThreshold = 255
params.blobColor = 255
params.filterByArea = False
params.filterByCircularity = False
params.filterByConvexity = False
params.filterByInertia = True
params.minInertiaRatio = 0.01

version = (cv2.__version__).split('.')
if int(version[0]) < 3 :
	detector = cv2.SimpleBlobDetector(params)
else:
	detector = cv2.SimpleBlobDetector_create(params)

vs = PiVideoStream().start()#resolution=(640,480)).start()
#warming up camera
time.sleep(2.0)

maus = True #When it's true, cam tracks IR pen, when false, only comp mouse
#this feature is mostly meant for testing purposes but is a feature u should
#be able to turn on and off

#frame_on is meant to help count whether a blob detected should be treated as a
#click or drag depending on the duration it appears in the camera frames
frame_on = 0

while True:
	image = vs.read()
	height, width = image.shape[:2]
	
	hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
	pers = cv2.warpPerspective(image, wer, (640,480))	
	mask = cv2.inRange(hsv, numpyL, numpyH)
	
	if maus == True:
		keypts = detector.detect(mask)
		bro = len(keypts)

		#bro is the number of keypoits there are
		if bro > 0:
			#unfortunately it only takes one point rather than treating
			#2 points as separate valid entities
			x = keypts[0].pt[0]
			y = keypts[0].pt[1]

			#testing if they're within the point bounds defined
			#by the perspective_transform.txt helps avoid several
			#checks and calcualtions
			if x > minx and x < maxx and y > miny and y < maxy:
				#then you can apply the transform
				results=np.array([[int(x),int(y)],[0,0],[0,0]],dtype="float32")
				results=np.array([results])

				bbbb = cv2.perspectiveTransform(results,wer)
				#print "x, y: %d %d" % (bbbb[0][0][0], bbbb[0][0][1])				
				if frame_on == 0:
					#click(int(x),int(y),width,height)
					click(int(bbbb[0][0][0]),int(bbbb[0][0][1]),width,height)
					frame_on = frame_on + 1
				else: #frameson > 0
					#drag(int(x),int(y),width,height)
					drag(int(bbbb[0][0][0]),int(bbbb[0][0][1]),width,height)
					frame_on = frame_on + 1

		else:
			frame_on = 0

	cv2.imshow("Frame", image)
	cv2.imshow("Mask", mask)
	cv2.imshow("warped", pers)
	key = cv2.waitKey(1) & 0xFF
	if key == ord('q'):
		break
	elif key == ord('m'):
		maus = not maus

	#these features do not work
	'''elif key==ord('h'):
		print("horizontal flip!")
		vs.hflip()
	elif key==ord('v'):
		print("vertical flip!")
		vs.vflip()'''

vs.stop()
cv2.destroyAllWindows()

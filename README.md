# VirtuWhite

## Introduction

Welcome to VirtuWhite! An internship project which centered around creating a economical smartboard using 
a Raspberry Pi, a camera and an IR or strongly colored Pen light.

You'll need a couple of libraries to run the present code: 
[OpenCV](http://opencv.org/)
Python 2.7 (It is already built into raspbian)
Numpy
Picamera

## Table of Contents

- [Introduction](#introduction)
- [The Current Setup](#the-current-setup)
    - [Color Calibration](#color-calibration)
    - [Point Calibration](#point-calibration)
    - [Display](#display)
- [Known Issues](#known-issues)
- [Future Development](#future-development)

## The Current Setup

At the moment, this program is consisted of 3 separate python based files to run in the order shown below:
1) [Color calibration](https://github.com/Virtuwhite/VirtuWhite/blob/master/colorcalib.py) 
2) [Point calibration](https://github.com/Virtuwhite/VirtuWhite/blob/master/calibration.py)
3) [The Main Program](https://github.com/Virtuwhite/VirtuWhite/blob/master/display.py)

### Color Calibration

To tinker your color calibration all you have to do is simply run `python colorcalib.py` and adjust the
sliders accordingly. You can see your image as well as the masked image (Within the threshold is
represented by white pixels in the mask). Ideally you would want your pointer source to be the only visible
white pixels in the whole video feed. Once you exit out of the program the HSV values will be written to
`color.txt` this threshold is what is used in both point calibration as well as the main program.

To exit out of the program when you are satisfied with your color calibration, click on one of the open
windows and press `q`, `esc` or `ctrl+C` on the terminal window.

The Theory behind **color calibration** is that you can isolate and mask out certain objects from each 
other using color isolation. This involves masking out certain colors be entering in a certain threshold 
as seen: 
![HSVcolorcalib](https://user-images.githubusercontent.com/14078865/29080083-e168781a-7c2c-11e7-922f-236504d8cd26.png) 

This particular threshold is tuned to the "color" of infrared light from an IR bulb passing through IR 
passing film. However, in theory this can work with any very bold color choice, as long as the color is 
different from the background.
More information about the theory on color separation can be found [here](http://opencv-srf.blogspot.ca/2010/09/object-detection-using-color-seperation.html)

The advantage to using an infrared light as opposed to an object in the visible light spectrum is that 
without the IR pass filter, all colors in the image are considered as potential points. For example, if 
your main object is blue, anything else that appears a similar shade of "blue" will be considered as 
passing within the threshold. 
Using infrared light allows you to put an infrared passing filter over your camera so that no visible 
light is permitted to pass through while infrared can be seen, as shown below: 

![2](https://user-images.githubusercontent.com/14078865/29080679-6cfa3f52-7c2e-11e7-857d-49032a1d23ed.png)![3](https://user-images.githubusercontent.com/14078865/29080685-70610d56-7c2e-11e7-9f46-fbf9d7533815.png) 

Using an infrared passing filter allows isolation of points to be a lot easier, as long as the room is not 
exposed to much infrared light, such as natural light.

### Point Calibration

To adjust your calibration points simply run `python calibration.py`. Using whatever you're using as your pointer
touch the corners of your display in the order: `top left, top right, bottom right, bottom left`. You
must wait 2 seconds after each point to avoid taking in the same point more than once.

This program will automatically exit after you've selected 4 points, but you can also prematurely exit by
selecting a window and typing `q`, `esc`, or entering the command `ctrl+C` in the terminal.

Much like older touchscreens and smartboards (observe Nintendo DS screen calibration as an example) 
sometimes the system is misaligned with the touch point. Due to the fact the picamera is likely not 
calibrated to your screen/projection the likelyhood that you need to point calibrate is 
very high, though this is a step you can skip if you haven't touched your setup since previously.

The reason behind this is that the camera's view captures more than just the screen area in it's field
of view, plus the likelihood that it isn't seeing the screen at a perspective angle is very slim. By using
the 4 points, this program defines the area where you must create your **projection matrix** in relation to
your picamera's video **image size** (ex. 640x480) Any point found inside of the region on the screen
area is then scaled up to your resolution size.

### Display

To run the main portion of the program run `python display.py` and give it a few seconds to warm up. Once
it is up and running, using your pointer on the projection/monitor should reflect approximately the same point as
the same point on your desktop.

Exitting the program is much the same as the other portions right now, by clicking a window and pressing
`q`, `esc`, or entering the command `ctrl+C` in the terminal.

`display.py is the main cut of the program where the transformations and actual interface is performed. It
uses **PiVideoStream.py** for it's video feed, which is a multithreaded image processor to improve FPS and increase
the processing rate of each image taken from the camera. Unfortunately, it has some downsides as well which
will be highlighted in [Known Issues](#known-issues)

((include stuff about blob detection I forgot it))

## Known Issues

Quite frankly, if anyone is seriously considering taking onboard this project I would highly recommend starting
from scratch to polish the program from the ground up, rather than try to build upon a rickety structure.

Some know problems with the current setup however:
Running with the *PiVideoStream* class sometimes brings up an error upon shutting down any program that
utilizes the class to run (ex. display.py) due to a bug involving *Daemon Threads*. Ideally you would want
because I'm utilizing python 2.7, daemon threads are unstable and cause errors upon shutdown where it would
kill system threads before threads that utilize the system. After much searching I have been unable to find
and fix the solution.

Another problem that I am unable to identify is the error where **glib-gobject-critical ** g_object_unref assertion**
appears in the terminal. It does not disrupt the program but I am unable to find the reason why it appears.

There is an obvious trade-off between resolution and framerate and this program is no exception. While the
framerate capture is decent at this point (~30fps) the sensitivity and accuracy of the pen is quite janky.

Blob detection in itself is still a work in progress as I am unsure of the efficiencies of using opencv's
blob detection library (simpleblobdetector) or how effective it is to appropriately capture the pen point,
as there are cases where the pen point is very obvious except it has a circle in the center where it 
does not pass the threshold. And in these cases, it does not register as a blob because of the torus shape.

File creation/reading from the text files can be improved and have no been tested on machines other than
the raspberry pi I've been working with. The program may run into issues with read/write permissions if
on another machine, as I have not tested the issue yet.

## Future Development

Aside from a possible total reworking, some future development can include:
`Creating an executable with a GUI.`
`Capture the highest IR point blobs more accurately.`
`Enable X11 Forwarding.`

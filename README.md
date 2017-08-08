# VirtuWhite

## Introduction

Welcome to VirtuWhite! An internship project which centered around creating a economical smartboard using a Raspberry Pi, a camera and an IR or strongly colored Pen light.

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

The Theory behind **color calibration** is that you can isolate and mask out certain objects from each other using color isolation. This involves masking out certain colors be entering in a certain threshold as seen:
![HSVcolorcalib](https://user-images.githubusercontent.com/14078865/29080083-e168781a-7c2c-11e7-922f-236504d8cd26.png)

This particular threshold is tuned to the "color" of infrared light from an IR bulb passing through IR passing film. However, in theory this can work with any very bold color choice, as long as the color is different from the background.
More information about the theory on color separation can be found [here](http://opencv-srf.blogspot.ca/2010/09/object-detection-using-color-seperation.html)

The advantage to using an infrared light as opposed to an object in the visible light spectrum is that without the IR pass filter, all colors in the image are considered as potential points. For example, if your main object is blue, anything else that appears a similar shade of "blue" will be considered as passing within the threshold.
Using infrared light allows you to put an infrared passing filter over your camera so that no visible light is permitted to pass through while infrared can be seen, as shown below:
![2](https://user-images.githubusercontent.com/14078865/29080679-6cfa3f52-7c2e-11e7-857d-49032a1d23ed.png) ![3](https://user-images.githubusercontent.com/14078865/29080685-70610d56-7c2e-11e7-9f46-fbf9d7533815.png)

### Point Calibration

### Display

## Known Issues

## Future Development


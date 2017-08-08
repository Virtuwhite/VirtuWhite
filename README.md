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
![HSV channels threshold](https://lh6.googleusercontent.com/OvIk4Yaswb8I-XSDHiM1P9IC1Um16zpb5BlYUIvNYRvJo262tJksxN48O0GdwrcmuhwILVnT2hF8NeEwe3njxS1v7-GLH41CYh-W=w2880-h1486)
This particular threshold is tuned to the "color" of infrared light from an IR bulb passing through IR passing film. However, in theory this can work with any very bold color choice, as long as the color is different from the background.
More information about the theory on color separation can be found [here](http://opencv-srf.blogspot.ca/2010/09/object-detection-using-color-seperation.html)

The advantage to using an Infrared light as opposed to

### Point Calibration
### Display

## Known Issues

## Future Development


#!/usr/bin/env python

from __future__ import division
import cv2
import camera
import numpy as np
import numpy
import math
import coordinates
import utils
import time

#SHAPEZ
##################
MORPH = 7
CANNY = 250
##################
_width  = 320
_height = 240
_margin = 0.0
##################

corners = np.array(
	[
		[[  		_margin, _margin 			]],
		[[ 			_margin, _height + _margin  ]],
		[[ _width + _margin, _height + _margin  ]],
		[[ _width + _margin, _margin 			]],
	]
)

pts_dst = np.array( corners, np.float32 )
#END SHAPEZ

_fov           = camera.fov
_meterdiff     = utils.meterdiff

#derived variables
_area    = _width * _height
_middle  = _width / 2
_single  = _width / _fov
_minsize = _area * 0.05

#functions
def process(picture):
	blurred = blur(picture)
#	border = addborder(blurred, 6, [0,0,0])
	hsv = converttohsv(blurred)
	cfilter = filterbycolor(hsv)
	masked = cv2.bitwise_and(blurred,blurred,mask=cfilter)
	contours = findinnercontours(masked)
	rectcont = findmaxrectangle(contours)
	inv = cv2.bitwise_not(blurred,blurred,mask=cfilter)
	if rectcont is not None:
		cX   = findcenter(rectcont)
		diff = finddiff(rectcont)
		#print(str(diff))
		coords = getcoords(cX, diff)
		return directtorect(inv, cX), coords, cX
#		return None, coords, cX
	else:
		return inv, coordinates.Coordinates(), -1

def blur(matrice):
	return cv2.blur(matrice,(5,5))

def sharpen(matrice):
	kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
	return cv2.filter2D(matrice, -1, kernel)

def addborder(matrice, size, color):
	for s in range(0,size):
		for x in range(0,_width-s):
			matrice[0+s,x]=color
			matrice[_height-1-s,x]=color
		for y in range(0,240-s):
			matrice[y,0+s]=color
			matrice[y,_width-1-s]=color
	return matrice

def converttohsv(matrice):
	return cv2.cvtColor(matrice, cv2.COLOR_BGR2HSV)

def filterbycolor(matrice):
	return cv2.inRange(matrice, utils.lower_1, utils.upper_1)
	#mask2 = cv2.inRange(matrice, utils.lower_2, utils.upper_2)
	#return cv2.addWeighted(mask1,1,mask2,1,0)

def medianCanny(matrice, thresh1, thresh2):
	median = numpy.median(matrice)
	matrice = cv2.Canny(matrice, int(thresh1 * median), int(thresh2 * median))
	return matrice

def findinnercontours(matrice):
	blue, green, red = cv2.split(matrice)

	blue_edges = medianCanny(blue, 0.2, 0.3)
	green_edges = medianCanny(green, 0.2, 0.3)
	red_edges = medianCanny(red, 0.2, 0.3)

	edges = blue_edges | green_edges | red_edges
	kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (MORPH, MORPH))
	closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

	hierarchy, contours, _ = cv2.findContours(closed, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
	return contours

def boundcontours(picture, contours):
	for contour in contours:
		if cv2.contourArea(contour) > _minsize:
			rectangle = cv2.boundingRect(contour)
			x,y,w,h = rectangle
			cv2.rectangle(picture,(x,y),(x+w,y+h),(0,255,0),2)

def findmaxrectangle(contours):
	maxrect = None
	maxarea = _minsize

	for contour in contours:
		area  = cv2.contourArea(contour)
		if area >= maxarea:
			arc_len = cv2.arcLength(contour, True)
			approx = cv2.approxPolyDP(contour, 0.1 * arc_len, True)
#			if len(approx) == 4:
			maxrect = contour
			maxarea = area

	return maxrect

def findcenter(contour):
	M  = cv2.moments(contour)
	cX = int(M["m10"] / M["m00"])
	return cX

def finddiff(contour):
	top    = tuple(contour[contour[:, :, 1].argmin()][0])
	bottom = tuple(contour[contour[:, :, 1].argmax()][0])
	return bottom[1] - top[1]

def measureangle(cX):
	return (_middle - cX) / _single

def measuredistance(diff):
	if diff == 0:
		return 0
        return _meterdiff / diff

def getcoords(cX, diff):
	coords          = coordinates.Coordinates()
	coords.angle    = measureangle(cX)
	coords.distance = measuredistance(diff)
	coords.cX = cX
	coords.latest   = time.time()
	return coords

def directtorect(picture, cX):
	if cX == -1:
		return picture
	lines = 32
	perline = int(240 / lines)
	for line in range(0,lines):
		start = perline * line
		end = perline * (line+1)
		if end > 240:
			end = 240
		color = (0,0,0)
		if line%3 == 0:
			color = (255,0,0)
		elif line%3 == 1:
			color = (0,255,0)
		elif line%3 == 2:
			color = (0,0,255)
		cv2.line(picture, (cX, start), (cX, end), color, 2)
	#if cX != -1:
	#	cv2.line(picture, (cX, 0), (cX, 240), (0,255,0), 2)
	return picture

def hidecolor(picture, mask):
	return cv2.bitwise_not(picture,picture,mask=mask)

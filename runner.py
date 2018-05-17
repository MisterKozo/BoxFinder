#!/usr/bin/env python

import cv2
import camera
import worker
import time
import coordinates
import network
import sys
import threading
import utils
import time
import signal

rip = '10.56.35.2'
if len(sys.argv) != 2:
	print("=====ATTENTION=====")
	print("Usage: " + sys.argv[0] + " DRIVERIP")
	print("No IP addresses specified! Defaulting to 10.56.35.69")
	print("=====ATTENTION=====")
	dip = '10.56.35.69'
else:
	dip = sys.argv[1]

print("Launched!")

camera = camera.Camera()

cconn = network.Network(rip, utils.cport)
iconn = network.Network(dip, utils.iport)

def signal_handler(signal, frame):
        print("Exiting safely")
	cconn.halt()
        iconn.halt()
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

coordinates = coordinates.Coordinates()

def run():
	mat = camera.tomat().copy()
	picture,coordinates,_ = worker.process(mat)
	cconn.send(str(coordinates))
	coordinates.latest = time.time()
	matstr = utils.mattostr(worker.directtorect(mat, coordinates.cX))
	iconn.send(matstr)

while True:
	cconn.connect()
	iconn.connect()
	while cconn.alive:
		if camera.latest >= 0 and camera.latest > coordinates.latest:
			run()
	cconn.halt()
	iconn.halt()

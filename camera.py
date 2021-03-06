#!/usr/bin/env python

import numpy as np
import cv2
import time
import threading
import utils

fov=60

class Camera:
	def __init__(self):
		while True:
			try:
				self.capture = cv2.VideoCapture(utils.camera)
				self.capture.set(3, 320)
				self.capture.set(4, 240)
				#self.capture.set(cv2.CAP_PROP_FPS, 25)
				self.latest = -1
				self.mat = None
				self._startthread()
				print("Started camera service")
				break
			except:
				print("Failed to connect to camera! Retrying in 5s...")
				time.sleep(5)

	def _start(self):
		while True:
			time.sleep(utils.delay)
			self.mat    = self.capture.read()[1]
			previous = self.latest
			self.latest = time.time()
			#print(str(self.latest - previous))

	def _startthread(self):
		camera = threading.Thread(target=self._start)
		camera.daemon = True
		camera.start()

	def tomat(self):
		return self.mat

	def tofile(self, *args):
		if (len(args) != 1):
			filename = str(time.time())+".jpg"
		else:
			filename = args[0]
		cv2.imwrite("images/"+filename, self.tomat())
		print("Captured to " + filename)

	def release(self):
		self.capture.release()

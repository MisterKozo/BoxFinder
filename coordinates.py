#!/usr/bin/env python

import time

class Coordinates:

	def __init__(self):
		self.distance = -100
		self.angle    = -100
		self.cX       = -100
		self.latest   = -100

	def found(self):
                if self.angle == -1:
                        return False
                return True
	def __nonzero__(self):
		if self.angle < -30:
			return False
		return True

	def __str__(self):
		self.latest = time.time()
		return str(self.angle) + ',' + str(self.distance)

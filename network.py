#!/usr/bin/env python

import socket
import sys
import coordinates
import threading
import utils
import time
#import random

class Network:
        def __init__(self, ip, port):
		self.port = port
                self.server_address = (ip, port)
		self.alive = False
		self.latest = -100
		self.load = None
		self.start()

		if self.server_address[0] == '10.56.35.2':
			self.dest = 'roboRIO'
		else:
			self.dest = 'DriverStation'

	def connect(self):
                print("Attempting to connect to "+str(self.server_address[0])+":"+str(self.server_address[1]))
		attempt = 0
		while True:
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.sock.settimeout(2)
			try:
                		self.sock.connect(self.server_address)
				print("Successfully connected")
				self.alive = True
				break
			except:
				if self.server_address[1] == 6969:
					attempt = attempt + 1
					if attempt % 2 == 0:
						self.server_address = ('10.56.35.69', self.port)
					else:
						self.server_address = ('10.56.35.42', self.port)
					dest = "DriverStation on " + self.server_address[0]
				print("Failed to connect! Retrying reconnection to " + self.server_address[0] + ":" + str(self.server_address[1]) + " in 1s...")
				time.sleep(1)

	def start(self):
		def background():
			while self.alive:
				if self.load not None:
					message = self.load
					mlen = utils.msg_len_ba(message)
					try:
						self.sock.send(mlen)
						self.sock.send(message)
						self.sock.send('FD'.decode('hex'))
						self.sock.send('FE'.decode('hex'))
						self.sock.send('FF'.decode('hex'))
						self.sock.send('FE'.decode('hex'))
						self.sock.send('FD'.decode('hex'))
						if "ack" not in self.sock.recv(8)[2:]:
							raise Exception("Did not receive acknowledgement!")
					except Exception as e:
						self.halt()
						print("Connection collapsed with error as following:")
						print(str(e))
					if self.load == message:
						self.load = None
		sender = threading.Thread(target=background)
		sender.daemon = True
		sender.start()

	def send(self, message):
		self.load = message

	def halt(self):
		self.sock.close()
		self.alive = False

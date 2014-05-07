#!/usr/bin/python2

'''

requirements: python-uinput, RPi.GPIO

if you get an error like:
OSError: [Errno 2] No such file or directory

run:
sudo modprobe -i uinput && sudo grep uinput /proc/modules

'''

from time import sleep
import RPi.GPIO as GPIO
import uinput

print("""
   ___       __   __ __       __     
 /'___`\   /'__`\/\ \\\ \    /'_ `\   
/\_\ /\ \ /\ \/\ \ \ \\\ \  /\ \L\ \  
\/_/// /__\ \ \ \ \ \ \\\ \_\/_> _ <_ 
   // /_\ \\\ \ \_\ \ \__ ,__\/\ \L\ \\
  /\______/ \ \____/\/_/\_\_/\ \____/
  \/_____/   \/___/    \/_/   \/___/ 
                      Hackerloop 2014


""")

device = uinput.Device([uinput.KEY_UP, uinput.KEY_DOWN, uinput.KEY_LEFT, uinput.KEY_RIGHT])

GPIO.setmode(GPIO.BCM)

# input port -> output code mapping
inputChannels = (7,8,25,24)
outputCodes = (uinput.KEY_LEFT,uinput.KEY_RIGHT,uinput.KEY_UP,uinput.KEY_DOWN)

if len(inputChannels) != len(outputCodes):
	print("Error: channel/ouput lists len mismatch. fix it, bitch.")
	exit()

# there must be a better way..
inputStatus = [False for i in range(len(inputChannels))]

# init starting channels status
for channel in inputChannels:
	GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

while True:
	# iterate input channels
	for index, channel in enumerate(inputChannels):
		# read channel's value
		value = GPIO.input(channel)
		if value == 1:
			# send key press on status changed
			if inputStatus[index] == False:
				device.emit(outputCodes[index], True)
				print("pressed %d\b" % (index,))
			# update input status
			inputStatus[index] = True
		else:
			# send key release on status changed
			if inputStatus[index] == True:
				device.emit(outputCodes[index], False)
				print("released %d\b" % (index,))
			# update input status
			inputStatus[index] = False
	sleep(0.1)

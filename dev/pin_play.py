#!/usr/bin/python

import RPi.GPIO as gpio
import time

gpio.setmode(gpio.BCM)
gpio.setup(17, gpio.OUT)
gpio.setup(22, gpio.OUT)
gpio.setup(23, gpio.OUT)
gpio.setup(24, gpio.OUT)

i = 0
while (i < 5):
	time.sleep(2)
	gpio.output(17, 1)
	time.sleep(2)
	gpio.output(22, 1)
	time.sleep(2)
	gpio.output(23, 1)
	time.sleep(2)
	gpio.output(24, 1)
	time.sleep(2)
	gpio.output(17, 0)
	time.sleep(2)
	gpio.output(22, 0)
	time.sleep(2)
	gpio.output(23, 0)
	time.sleep(2)
	gpio.output(24, 0)
	time.sleep(2)
	i = i + 1


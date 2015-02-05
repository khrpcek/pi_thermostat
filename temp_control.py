#!/usr/bin/python
#this is the backend for the display. This is what actually controls the temperature and does all of the work
#the gui is just a dumb thing for setting vaules in the DB that this script uses to control the temp
import time
import psycopg2
import RPi.GPIO as gpio

#initialize the gpio pins
gpio.setmode(gpio.BCM)
gpio.setwarnings(False)

#fan relay
gpio.setup(17, gpio.OUT)
#heat relay
gpio.setup(22, gpio.OUT)
#AC relay
gpio.setup(23, gpio.OUT)
#extra relay
gpio.setup(24, gpio.OUT)


#Pulling data from DB and storing it to variables

conn = psycopg2.connect("dbname='thermdb' user='py_local' host='localhost' password='py_local'")
cursor = conn.cursor()
#start forever loop
while True:
	cursor.execute("select in_cur_temp, in_cur_humidity, heat_status, ac_status, fan_status from live_data where id = '1';")
	row = cursor.fetchone()
	cur_temp = round((float(row[0]) * 1.8) + 32,1)
	cur_humidity = row[1]
	heat_status = row[2]
	ac_status = row[3]
	fan_status = row[4]
#	print "Current temp is %s" % (cur_temp)

	cursor.execute("select set_temp, fan_setting, ac_setting, heat_setting from settings where id = '0';")
	row = cursor.fetchone()
	set_temp = row[0] 
	fan_setting = row[1]
	ac_setting = row[2]
	heat_setting = row[3]
#	print "\n"
#	print "Set temp is %s \n" % (set_temp)
#	print "Fan is %s \n" % (fan_setting)
#	print "AC is %s \n" % (ac_setting)
#	print "Heat is %s \n" % (heat_setting)

######
#control part
######

#we need to give the thermostat +/- a certain amount so it isn't always going on and off.

	wobble = 1

	wobble_high_temp = set_temp + wobble
	wobble_low_temp = set_temp - wobble

	#heat mode
	if heat_setting:
		if cur_temp < wobble_low_temp:
#			print "Running furnace"
			if bool(heat_status) is False:
				cursor.execute("insert into heat_log (heat_status) values ('true');")
				cursor.execute("update live_data set heat_status = true where id = 1;")
		elif cur_temp >= wobble_high_temp:
#			print "Above set temp, not running furnace"
			if heat_status:
				cursor.execute("insert into heat_log (heat_status) values ('false');")
				cursor.execute("update live_data set heat_status = false where id = 1;")
#AC mode
	if ac_setting:
		if cur_temp > wobble_high_temp:
			print "Running AC"
		elif cur_temp <= wobble_low_temp:
			print "Below set temp, not running AC"

#sleep for next iteration
	conn.commit()
	time.sleep(60)

conn.close()
#shit to remember
#when using the RPi.GPIO library...
#wire input to right port, output to middle
#setting the gpio pin to false sets the light to red and turns off the connection
#setting true enables the circuit and turns OFF the red light
#we're going to use 
# relay 1 pin 11 gpio 17
# relay 2 pin 15 gpio 22
# relay 3 pin 16 gpio 23
# relay 4 pin 17 gpio 24

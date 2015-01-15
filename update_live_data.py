#!/usr/bin/python

import Adafruit_DHT
import psycopg2

db_host = 'localhost'
db_user = 'py_local'
db_pass = 'py_local'
db = 'thermdb'

sensor = 22
pin = 4

humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

conn = psycopg2.connect("dbname='thermdb' user='py_local' host='localhost' password='py_local'")
cursor = conn.cursor()
cursor.execute("update live_data set in_cur_temp = %s, in_cur_humidity = %s where id = 1;", (temperature,humidity))
cursor.execute("insert into historical_data (in_cur_temp, in_cur_humidity) values (%s, %s);", (temperature,humidity))
conn.commit()
conn.close()


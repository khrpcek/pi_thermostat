#!/usr/bin/python
from flask import Flask
from flask import render_template
from flask import request
import os
import sys
import psycopg2

app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def index():
	
	#db settings and connection
	db_host = 'localhost'
	db_user = 'py_local'
	db_pass = 'py_local'
	db = 'thermdb'

	conn = psycopg2.connect("dbname='thermdb' user='py_local' host='localhost' password='py_local'")
	cursor = conn.cursor()

	#process updates from post data and send it to the settings table in the DB
	#
	#doing some funny chit here because the nature of html is that if a checkbox
	#is false, it doesn't return any post data. So that was causing a 400 error in 
	#flask. What we're doing is setting all the checkboxes to false since we know
	#their names and then cheking for the existence of the post data in request.form.
	#If it exists in request.form, we set the value to true and move on with life

	if request.method == "POST":
		post_set_temp = request.form['set_temp']
		post_fan_setting = False
		if 'fan_setting' in request.form:
			post_fan_setting = True
		post_ac_setting = False
		if 'ac_setting' in request.form:
			post_ac_setting = True
		post_heat_setting = False
		if 'heat_setting' in request.form:
			post_heat_setting = True
		print "set_temp is {} and fan is {} and heat is {} and ac is {}".format(post_set_temp, post_fan_setting, post_heat_setting, post_ac_setting)
		
#make the query like this update settings set (set_temp, fan_setting, ac_setting, heat_setting) = ('72', false, true, false) where id = '0';
		cursor.execute("update settings set (set_temp, fan_setting, ac_setting, heat_setting) = (%s, %s, %s, %s) where id = '0';", (post_set_temp, post_fan_setting, post_ac_setting, post_heat_setting))
		conn.commit()

	#select live data
	cursor.execute("select in_cur_temp, in_cur_humidity from live_data where id = 1;")
	row = cursor.fetchone()
	cur_temp = round((float(row[0]) * 1.8) + 32,1)
	cur_humidity = round(row[1],1)

	#collect user settings/status
	cursor.execute("select set_temp, fan_setting, ac_setting, heat_setting from settings where id = '0';")
	row = cursor.fetchone()
	set_temp = row[0] 
	fan_setting = str(row[1])
	ac_setting = str(row[2])
	heat_setting = str(row[3])
	conn.close()
	#return "Temp is {}*F and humidity is {}% ".format(cur_temp, cur_humidity)
	return render_template('index.html', cur_temp=cur_temp, cur_humidity=cur_humidity, set_temp=set_temp, fan_setting=fan_setting, ac_setting=ac_setting, heat_setting=heat_setting)

@app.route('/update_settings', methods=['POST'])
def update_settings():
	set_temp = request.form['set_temp']
	fan_setting = request.form['fan_setting']
	heat_setting = request.form['heat_setting']
	ac_setting = request.form['ac_setting']

	return "Temp is {} and fan is {} and heat is {} and ac is {}".format(set_temp, fan_setting, heat_setting, ac_setting)

	#return redirect(url_for('index'))


@app.route('/history')
def history():

	return "history"


if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0')

# import sqlite3 as lite
# import sys
# from sensors import read_temp 
# con = lite.connect('sensorsData.db')
# print("reading temp")
# #print(read_temp())
# temp = 2
# with con:
#     cur = con.cursor()
#     cur.execute(INSERT INTO sensor_data VALUES(datetime('now'), temp))
#     print("reading temp")
#     print(read_temp())

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import io
from flask import Flask, render_template, send_file, make_response, request
app = Flask(__name__)
import sqlite3
conn=sqlite3.connect('sensorsData.db')
curs=conn.cursor()
# Retrieve LAST data from database
def getLastData():
	for row in curs.execute("SELECT * FROM sensor_data ORDER BY timestamp DESC LIMIT 1"):
		time = str(row[0])
		temp = row[1]
	#conn.close()
	return time, temp, hum
def getHistData (numSamples):
	curs.execute("SELECT * FROM sensor_data ORDER BY timestamp DESC LIMIT "+str(numSamples))
	data = curs.fetchall()
	dates = []
	temps = []
	for row in reversed(data):
		dates.append(row[0])
		temps.append(row[1])
	return dates, temps
def maxRowsTable():
	for row in curs.execute("select COUNT(temp) from sensor_data"):
		maxNumberRows=row[0]
	return maxNumberRows
# define and initialize global variables
global numSamples
numSamples = maxRowsTable()
    if (numSamples > 101):
numSamples = 100
# main route
@app.route("/")
def index():
	time, temp, hum = getLastData()
	templateData = {
	  	'time'	: time,
		'temp'	: temp,
      		'numSamples'	: numSamples
	}
	return render_template('index.html', **templateData)
@app.route('/', methods=['POST'])
def my_form_post():
    global numSamples
    numSamples = int (request.form['numSamples'])
    numMaxSamples = maxRowsTable()
    if (numSamples > numMaxSamples):
        numSamples = (numMaxSamples-1)
    time, temp, hum = getLastData()
    templateData = {
	  	'time'	: time,
      		'temp'	: temp,
      		'numSamples'	: numSamples
	}
    return render_template('index.html', **templateData)
# @app.route('/plot/temp')
# def plot_temp():
# 	times, temps, hums = getHistData(numSamples)
# 	ys = temps
# 	fig = Figure()
# 	axis = fig.add_subplot(1, 1, 1)
# 	axis.set_title("Temperature [°C]")
# 	axis.set_xlabel("Samples")
# 	axis.grid(True)
# 	xs = range(numSamples)
# 	axis.plot(xs, ys)
# 	canvas = FigureCanvas(fig)
# 	output = io.BytesIO()
# 	canvas.print_png(output)
# 	response = make_response(output.getvalue())
# 	response.mimetype = 'image/png'
# 	return response
if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=False)
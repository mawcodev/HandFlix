"""
File: app.py
Description: The heart of aplication. 
Author: Matthew Conde Oltra
"""
from flask import Flask, render_template, Response
import numpy as np
from cam import VideoStream

app = Flask(__name__)

@app.route('/')
def index():
	"""Video streaming home page."""
	return render_template('index.html')

def gen(camera):
	"""Video streaming generator function"""
	while True:
		frame = camera.hand_pose()
		yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
		#yield(frame)

@app.route('/video_feed')
def video_feed():
	"""Video streaming route. Put this in the src attribute of an img tag."""
	return Response(gen(VideoStream()), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=80, debug=True, threaded=True)
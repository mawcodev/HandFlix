"""
File: app.py
Description: The heart of aplication. 
Author: Matthew Conde Oltra
"""
from flask import Flask, render_template, Response, jsonify
import numpy as np
from cam import VideoStream

app = Flask(__name__)
camera = VideoStream()

@app.route('/')
def index():
	"""Video streaming home page."""
	return render_template('index.html')

@app.route('/video_feed')
def video_feed():
	def generate(camera):
		while True:
			frame = camera.hand_pose()
			yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
	return Response(generate(camera), mimetype='multipart/x-mixed-replace;boundary=frame')

# Return as a json de current gesture detected
@app.route('/gesture')
def gesture():
	return jsonify({"gesture": camera.getGesture()})

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=80, debug=True, threaded=True)
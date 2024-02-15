#BUG in code raspberry pi can't be pinged by a device on network
from flask import Flask, jsonify

app = Flask(__name__)

# test endpoint at "http://{ip-address}:8080/hello"
@app.route('/hello')
def hello_world():
	# prints to terminal
	print('message sent')
	# returns message to request
	return jsonify({'message': 'Hello, world'})

if __name__ == '__main__':
	# app runs on ip '0.0.0.0' which is all networks ip
	# so samething as device ip
	app.run(host='0.0.0.0', port=8080)